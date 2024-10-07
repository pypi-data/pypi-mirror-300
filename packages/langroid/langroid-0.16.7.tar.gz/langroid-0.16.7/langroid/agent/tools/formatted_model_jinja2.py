from abc import ABC, abstractmethod
from typing import Type, TypeVar

from jinja2 import BaseLoader, Environment
from parse import parse as str_parse
from parse import with_pattern

from langroid.pydantic_v1 import BaseModel

T = TypeVar("T", bound="FormattingModel")


@with_pattern(r"[\s\S]*?")
def _match_multiline(text):
    return text.strip()


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
    def parse(cls: Type[T], text: str) -> T:
        content = text.strip()[len(cls.start_token()) : -len(cls.end_token())].strip()
        result = str_parse(
            cls.parse_spec(),
            content,
            dict(multiline=_match_multiline),
            case_sensitive=False,
        )
        if result is None:
            raise ValueError(
                f"Failed to parse the input string using spec: {cls.parse_spec()}\nInput: {content}"
            )
        return cls(**result.named)

    def generate(self) -> str:
        env = Environment(loader=BaseLoader(), trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(self.format_spec())
        content = template.render(**self.dict())
        return f"{self.start_token()}\n{content.strip()}\n{self.end_token()}"


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def format_spec(cls) -> str:
        return (
            "code_file_model\n"
            "file_path: {{- file_path -}}\n"
            "```{{- language -}}\n"
            "{{ code }}"
            "```"
        )

    @classmethod
    def parse_spec(cls) -> str:
        return "code_file_model\n" "file_path:{:s}\n" "```{:s}\n" "{:multiline}" "```"

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"


# Test code
if __name__ == "__main__":
    # Test with extra whitespace
    test_string = """
    <format>
        code_file_model
        file_path:     src/main.py    
        ```   python   
        def hello():
            print("Hello, World!")
        
        ```
    </format>
    """

    parsed = CodeFileModel.parse(test_string)
    print("Parsed model:")
    print(parsed)

    generated = parsed.generate()
    print("\nGenerated string:")
    print(generated)

    reparsed = CodeFileModel.parse(generated)
    print("\nReparsed model:")
    print(reparsed)

    print("\nRound trip test:")
    assert parsed == reparsed, "Round trip test failed"
    print("Passed!")

    # Test with different values and whitespace
    another_test = """
    <format>
    code_file_model
    file_path:src/app.js
    ``` javascript
    function greet(name) {
        console.log(`Hello, ${name}!`);
    }
    ```
    </format>
    """

    another_parsed = CodeFileModel.parse(another_test)
    print("\nAnother parsed model:")
    print(another_parsed)

    another_generated = another_parsed.generate()
    print("\nAnother generated string:")
    print(another_generated)

    print("\nAnother round trip test:")
    assert another_parsed == CodeFileModel.parse(
        another_generated
    ), "Another round trip test failed"
    print("Passed!")
