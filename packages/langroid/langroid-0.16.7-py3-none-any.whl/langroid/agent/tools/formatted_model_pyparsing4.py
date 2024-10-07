from abc import ABC, abstractmethod
from typing import List, Tuple

from pyparsing import (
    LineEnd,
    Literal,
    Optional,
    SkipTo,
    Suppress,
    White,
)

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def spec(cls) -> List[Tuple[str, str, dict]]:
        pass

    @classmethod
    def format_spec(cls):
        format_str = ""
        for literal, field, options in cls.spec():
            if field:
                if options.get("multiline", False):
                    format_str += f"{{{field}}}\n"
                else:
                    format_str += f"{{{field}}}"
            else:
                format_str += literal
        return format_str

    @classmethod
    def parse_spec(cls):
        parser = None
        for literal, field, options in cls.spec():
            if literal:
                element = Suppress(Optional(White())) + Literal(literal)
            else:
                if options.get("multiline", False):
                    end_marker = Suppress(Optional(White())) + Literal(
                        options.get("end_marker", "```")
                    )
                    element = SkipTo(end_marker).setParseAction(
                        lambda s, l, t: t[0].strip()
                    )
                else:
                    element = SkipTo(LineEnd()).setParseAction(
                        lambda s, l, t: t[0].strip()
                    )
                if field:
                    element = element.setResultsName(field)
                    if "parse_action" in options:
                        element = element.setParseAction(options["parse_action"])
            parser = element if parser is None else parser + element
        return parser

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        spec = cls.format_spec()
        formatted = spec.format(**instance.dict())
        return f"{cls.start_token()}\n{formatted.rstrip()}\n{cls.end_token()}"

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        lines = formatted_string.strip().split("\n")
        if lines[0] != cls.start_token() or lines[-1] != cls.end_token():
            raise ValueError("Invalid start or end token")
        content = "\n".join(lines[1:-1])

        spec = cls.parse_spec()
        parsed = spec.parseString(content, parseAll=True)
        return cls(**parsed.asDict())


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def spec(cls):
        return [
            ("code_file_model\n", "", {}),
            ("", "file_path", {"single_line": True}),
            ("\n```", "", {}),
            ("", "language", {"single_line": True}),
            ("\n", "", {}),
            (
                "",
                "code",
                {
                    "multiline": True,
                    "end_marker": "```",
                    "parse_action": lambda s, l, t: t[0].rstrip(),
                },
            ),
            ("\n```", "", {}),
        ]


if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
    )
    formatted = CodeFileModel.format(code_file)
    expected_format = """<format>
code_file_model
src/main.py
```Python
def hello():
    print('Hello, World!')
```
</format>"""

    # Compare ignoring whitespace
    assert "".join(formatted.split()) == "".join(
        expected_format.split()
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
        language="JavaScript",
        file_path="src/app.js",
        code="function greet() {\n  console.log('Hello, World!');\n}",
    )
    formatted2 = CodeFileModel.format(code_file2)
    parsed2 = CodeFileModel.parse(formatted2)
    assert (
        parsed2 == code_file2
    ), f"Parsing failed for different values. Expected:\n{code_file2}\nGot:\n{parsed2}"
    print("Different values test passed.")

    print("All tests passed successfully!")

# Test cases
if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
    )
    formatted = CodeFileModel.format(code_file)
    expected_format = """<format>
code_file_model
src/main.py
```Python
def hello():
    print('Hello, World!')
```
</format>"""
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
        language="JavaScript",
        file_path="src/app.js",
        code="function greet() {\n  console.log('Hello, World!');\n}",
    )
    formatted2 = CodeFileModel.format(code_file2)
    parsed2 = CodeFileModel.parse(formatted2)
    assert (
        parsed2 == code_file2
    ), f"Parsing failed for different values. Expected:\n{code_file2}\nGot:\n{parsed2}"
    print("Different values test passed.")

    print("All tests passed successfully!")
