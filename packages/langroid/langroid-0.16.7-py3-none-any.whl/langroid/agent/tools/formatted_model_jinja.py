import re
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from jinja2 import BaseLoader, Environment

from langroid.pydantic_v1 import BaseModel

T = TypeVar("T", bound="FormattingModel")


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def format_spec(cls) -> str:
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
    def parse(cls: Type[T], text: str) -> T:
        content = text.strip()[len(cls.start_token()) : -len(cls.end_token())].strip()
        pattern = cls.format_spec()
        for field in cls.__fields__:
            pattern = pattern.replace(f"{{{{{field}}}}}", f"(?P<{field}>.*?)")
        pattern = pattern.replace("\n", "\\n")

        match = re.match(pattern, content, re.DOTALL)
        if not match:
            raise ValueError("Failed to parse the input string")

        parsed_data = {k: v.strip() for k, v in match.groupdict().items()}
        return cls(**parsed_data)

    def generate(self) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.format_spec())
        content = template.render(**self.dict())
        return f"{self.start_token()}\n{content}\n{self.end_token()}"


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def format_spec(cls) -> str:
        return (
            "code_file_model\nfile_path: {{file_path}}\n```{{language}}\n{{code}}\n```"
        )

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"


if __name__ == "__main__":
    # Test CodeFileModel
    code_model = CodeFileModel(
        language="python",
        file_path="src/main.py",
        code='def hello():\n    print("Hello, World!")',
    )

    print("Original CodeFileModel:")
    print(code_model)
    print()

    generated = code_model.generate()
    print("Generated string:")
    print(generated)
    print()

    parsed = CodeFileModel.parse(generated)
    print("Parsed CodeFileModel:")
    print(parsed)
    print()

    print("Round-trip test:")
    assert (
        code_model == parsed
    ), "Round-trip test failed: original and parsed models are not equal"
    print("Passed!")

    # Test with different values
    another_model = CodeFileModel(
        language="javascript",
        file_path="src/app.js",
        code="function greet(name) {\n    console.log(`Hello, ${name}!`);\n}",
    )

    print("\nAnother CodeFileModel:")
    print(another_model)
    print()

    another_generated = another_model.generate()
    print("Another generated string:")
    print(another_generated)
    print()

    another_parsed = CodeFileModel.parse(another_generated)
    print("Another parsed CodeFileModel:")
    print(another_parsed)
    print()

    print("Another round-trip test:")
    assert (
        another_model == another_parsed
    ), "Another round-trip test failed: original and parsed models are not equal"
    print("Passed!")

    # Test error handling
    print("\nTesting error handling:")
    try:
        CodeFileModel.parse("Invalid format string")
        assert False, "Should have raised a ValueError"
    except ValueError as e:
        print(f"Correctly raised ValueError: {e}")

    print("\nAll tests passed successfully!")
