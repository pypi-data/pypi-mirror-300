from abc import ABC, abstractmethod

from lark import Lark, Transformer, v_args

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def format_spec(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parse_spec(cls) -> str:
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

        parser = Lark(cls.parse_spec(), start="start", parser="lalr")

        @v_args(inline=True)
        class TreeToDict(Transformer):
            def start(self, _, file_path, code_block):
                return {
                    "file_path": file_path,
                    "language": code_block.children[1],
                    "code": code_block.children[3],
                }

            def file_path(self, path):
                return path.value

            def language(self, lang):
                return lang.value

            def code(self, code):
                return code.value.strip()

        tree = parser.parse(content)
        data = TreeToDict().transform(tree)
        return cls(**data)


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def format_spec(cls):
        return "code_file_model\n{file_path}\n```{language}\n{code}\n```"

    @classmethod
    def parse_spec(cls):
        return """
            start: "code_file_model" NEWLINE file_path NEWLINE code_block
            file_path: /[^\\n]+/
            code_block: "```" language NEWLINE code "```"
            language: /[^\\n]+/
            code: /.+?(?=\\n```)/s
            NEWLINE: "\\n"
            %import common.WS
            %ignore WS
        """

    @classmethod
    def start_token(cls):
        return "<format>"

    @classmethod
    def end_token(cls):
        return "</format>"


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

    # Test tolerant parsing
    tolerant_input = """<format>
code_file_model
   src/main.py   

```  Python  
def hello():
    print('Hello, World!')
```
</format>"""
    parsed_tolerant = CodeFileModel.parse(tolerant_input)
    expected_tolerant = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
    )
    assert (
        parsed_tolerant == expected_tolerant
    ), f"Tolerant parsing failed. Expected:\n{expected_tolerant}\nGot:\n{parsed_tolerant}"
    print("Tolerant parsing test passed.")

    print("All tests passed successfully!")
