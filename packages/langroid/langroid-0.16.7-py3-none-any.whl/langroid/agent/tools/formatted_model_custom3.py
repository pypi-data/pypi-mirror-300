from abc import ABC
from typing import Dict, List

from langroid.pydantic_v1 import BaseModel, Field


class FormatMetadata(BaseModel):
    prefix: str = ""
    suffix: str = ""
    multiline: bool = False


class FormattingModel(BaseModel, ABC):
    @classmethod
    def format_spec(cls) -> str:
        lines = []
        for name, field in cls.__fields__.items():
            metadata: FormatMetadata = field.field_info.extra.get(
                "format_metadata", FormatMetadata()
            )
            if metadata.multiline:
                lines.append(f"{metadata.prefix}{{{name}}}{metadata.suffix}")
            else:
                lines.append(f"{metadata.prefix}{{{name}}}{metadata.suffix}")
        return "\n".join(lines)

    @classmethod
    def parse_spec(cls) -> Dict[str, FormatMetadata]:
        return {
            name: field.field_info.extra.get("format_metadata", FormatMetadata())
            for name, field in cls.__fields__.items()
        }

    @classmethod
    def start_token(cls) -> str:
        return getattr(cls.Config, "start_token", "<format>")

    @classmethod
    def end_token(cls) -> str:
        return getattr(cls.Config, "end_token", "</format>")

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        spec = cls.format_spec()
        formatted = spec.format(**instance.dict())
        return f"{cls.start_token()}\n{formatted}\n{cls.end_token()}"

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        lines = formatted_string.strip().split("\n")
        if lines[0] != cls.start_token():
            raise ValueError("Invalid start token")

        content = "\n".join(lines[1:])
        if content.endswith(cls.end_token()):
            content = content[: -len(cls.end_token())].strip()

        parsed_data = {}
        parse_spec = cls.parse_spec()
        field_names = list(parse_spec.keys())

        for i, (field, metadata) in enumerate(parse_spec.items()):
            is_last_field = i == len(field_names) - 1
            if metadata.multiline:
                start = f"{metadata.prefix}"
                end = f"{metadata.suffix}"
                start_index = content.find(start)
                if start_index == -1:
                    raise ValueError(f"Could not find start of {field}")
                start_index += len(start)
                if is_last_field:
                    end_index = content.find(end, start_index)
                    if end_index == -1:
                        end_index = len(content)
                    value = content[start_index:end_index].strip()
                else:
                    end_index = content.find(end, start_index)
                    if end_index == -1:
                        raise ValueError(f"Could not find end of {field}")
                    value = content[start_index:end_index].strip()
            else:
                line_start = f"{metadata.prefix}"
                line_end = metadata.suffix or "\n"
                start_index = content.find(line_start)
                if start_index == -1:
                    raise ValueError(f"Could not find {field}")
                start_index += len(line_start)
                if is_last_field:
                    end_index = content.find(line_end, start_index)
                    if end_index == -1:
                        end_index = len(content)
                    value = content[start_index:end_index].strip()
                else:
                    end_index = content.find(line_end, start_index)
                    if end_index == -1:
                        raise ValueError(f"Could not find end of {field}")
                    value = content[start_index:end_index].strip()

            parsed_data[field] = value
            content = content[
                end_index + len(end if metadata.multiline else line_end) :
            ].strip()

        return cls(**parsed_data)

    @staticmethod
    def find_all_candidates(string: str, begin_token: str, end_token: str) -> List[str]:
        candidates = []
        start = 0
        while True:
            start_index = string.find(begin_token, start)
            if start_index == -1:
                break

            end_index = string.find(end_token, start_index + len(begin_token))
            if end_index == -1:
                # If no end token is found, assume it extends to the end of the string
                candidates.append(string[start_index:])
                break

            # Check if there's a nested begin token before the end token
            next_start = string.find(
                begin_token, start_index + len(begin_token), end_index
            )
            if next_start != -1:
                # If there's a nested begin token, continue searching from there
                start = next_start
                continue

            candidates.append(string[start_index : end_index + len(end_token)])
            start = end_index + len(end_token)

        return candidates


class CodeFileModel(FormattingModel):
    file_path: str = Field(..., format_metadata=FormatMetadata(prefix="file_path: "))
    language: str = Field(..., format_metadata=FormatMetadata(prefix="language: "))
    code: str = Field(
        ...,
        format_metadata=FormatMetadata(prefix="```\n", suffix="\n```", multiline=True),
    )

    class Config:
        start_token = "<code_file>"
        end_token = "</code_file>"


if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        file_path="src/main.py",
        language="python",
        code="def main():\n    print('Hello, World!')",
    )
    formatted = CodeFileModel.format(code_file)
    expected_format = """<code_file>
file_path: src/main.py
language: python
```
def main():
    print('Hello, World!')
```
</code_file>"""
    assert (
        formatted == expected_format
    ), f"Formatting failed. Expected:\n{expected_format}\nGot:\n{formatted}"
    print("Formatting test passed.")

    # Test parsing
    parsed = CodeFileModel.parse(formatted)
    assert (
        parsed == code_file
    ), f"Parsing failed. Expected:\n{code_file}\nGot:\n{parsed}"
    print("Parsing test passed.")

    # Test round-trip
    round_trip = CodeFileModel.parse(CodeFileModel.format(code_file))
    assert (
        round_trip == code_file
    ), f"Round-trip failed. Expected:\n{code_file}\nGot:\n{round_trip}"
    print("Round-trip test passed.")

    # Test with different values
    code_file2 = CodeFileModel(
        file_path="src/app.js",
        language="javascript",
        code="function greet() {\n  console.log('Hello, World!');\n}",
    )
    formatted2 = CodeFileModel.format(code_file2)
    parsed2 = CodeFileModel.parse(formatted2)
    assert (
        parsed2 == code_file2
    ), f"Parsing failed for different values. Expected:\n{code_file2}\nGot:\n{parsed2}"
    print("Different values test passed.")

    # Test tolerant parsing
    tolerant_input = """<code_file>
file_path:    src/main.py   
language:   python  
```
def main():
    print('Hello, World!')
```
</code_file>"""
    parsed_tolerant = CodeFileModel.parse(tolerant_input)
    expected_tolerant = CodeFileModel(
        file_path="src/main.py",
        language="python",
        code="def main():\n    print('Hello, World!')",
    )
    assert (
        parsed_tolerant == expected_tolerant
    ), f"Tolerant parsing failed. Expected:\n{expected_tolerant}\nGot:\n{parsed_tolerant}"
    print("Tolerant parsing test passed.")

    # Test tolerant parsing without end token and last field suffix
    tolerant_input_no_end = """<code_file>
file_path: src/main.py
language: python
```
def main():
    print('Hello, World!')"""
    parsed_tolerant_no_end = CodeFileModel.parse(tolerant_input_no_end)
    expected_tolerant_no_end = CodeFileModel(
        file_path="src/main.py",
        language="python",
        code="def main():\n    print('Hello, World!')",
    )
    assert (
        parsed_tolerant_no_end == expected_tolerant_no_end
    ), f"Tolerant parsing without end token failed. Expected:\n{expected_tolerant_no_end}\nGot:\n{parsed_tolerant_no_end}"
    print("Tolerant parsing without end token test passed.")

    # Test find_all_candidates method
    test_string = """
    Some text before
    <code_file>
    file_path: src/main.py
    language: python
    ```
    def main():
        print('Hello, World!')
    ```
    </code_file>
    Some text in between
    <code_file>
    file_path: src/helper.py
    language: python
    ```
    def helper():
        return 'Helper function'
    ```
    </code_file>
    <code_file>
    file_path: src/incomplete.py
    language: python
    ```
    def incomplete():
        print('No end token')
    Some text after
    """

    candidates = FormattingModel.find_all_candidates(
        test_string, "<code_file>", "</code_file>"
    )
    assert len(candidates) == 3, f"Expected 3 candidates, got {len(candidates)}"
    assert candidates[0].startswith("<code_file>") and candidates[0].endswith(
        "</code_file>"
    ), "First candidate is incorrect"
    assert candidates[1].startswith("<code_file>") and candidates[1].endswith(
        "</code_file>"
    ), "Second candidate is incorrect"
    assert candidates[2].startswith("<code_file>") and not candidates[2].endswith(
        "</code_file>"
    ), "Third candidate is incorrect"
    print("find_all_candidates test passed.")

    print("All tests passed successfully!")
