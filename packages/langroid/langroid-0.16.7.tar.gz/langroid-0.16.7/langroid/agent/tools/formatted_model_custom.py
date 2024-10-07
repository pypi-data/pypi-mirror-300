from abc import ABC, abstractmethod
from typing import List, Tuple

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def format_spec(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parse_spec(cls) -> List[Tuple[str, str, str]]:
        pass

    @classmethod
    @abstractmethod
    def start_token(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def end_token(cls) -> str:
        pass

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        spec = cls.format_spec()
        formatted = spec.format(**instance.dict())
        return f"{cls.start_token()}\n{formatted}\n{cls.end_token()}"

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        lines = formatted_string.strip().split("\n")
        if lines[0] != cls.start_token() or lines[-1] != cls.end_token():
            raise ValueError("Invalid start or end token")
        content = "\n".join(lines[1:-1])

        parsed_data = {}
        for field, start, end in cls.parse_spec():
            start_index = content.find(start)
            if start_index == -1:
                raise ValueError(f"Could not find start of {field}")
            end_index = content.find(end, start_index + len(start))
            if end_index == -1:
                raise ValueError(f"Could not find end of {field}")
            value = content[start_index + len(start) : end_index].strip()
            parsed_data[field] = value

        return cls(**parsed_data)


class CodeFileModel(FormattingModel):
    file_path: str
    language: str
    code: str

    @classmethod
    def format_spec(cls):
        return "file_path: {file_path}\nlanguage: {language}\n```\n{code}\n```"

    @classmethod
    def parse_spec(cls):
        return [
            ("file_path", "file_path:", "\n"),
            ("language", "language:", "\n"),
            ("code", "```\n", "\n```"),
        ]

    @classmethod
    def start_token(cls):
        return "<code_file>"

    @classmethod
    def end_token(cls):
        return "</code_file>"


# Test cases
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

    print("All tests passed successfully!")
