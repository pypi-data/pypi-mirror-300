from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar

from pyparsing import (
    LineEnd,
    ParseException,
    ParserElement,
    Regex,
    SkipTo,
    Suppress,
    Word,
    alphanums,
)

from langroid.pydantic_v1 import BaseModel

T = TypeVar("T", bound="FormattingModel")


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def format_spec(cls) -> tuple[str, ParserElement]:
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
    @abstractmethod
    def field_mappings(cls) -> Dict[str, str]:
        pass

    @classmethod
    def parse(cls: Type[T], text: str) -> T:
        content = text.strip()[len(cls.start_token()) : -len(cls.end_token())].strip()
        try:
            _, parser = cls.format_spec()
            parsed = parser.parseString(content)
            data = {
                field: parsed[token].strip()
                for field, token in cls.field_mappings().items()
            }
            return cls(**data)
        except ParseException as e:
            print(f"Parsing error: {e}")
            raise

    def generate(self) -> str:
        template, _ = self.format_spec()
        for field, token in self.field_mappings().items():
            value = getattr(self, field)
            template = template.replace(f"{{{token}}}", str(value))
        return f"{self.start_token()}\n{template}\n{self.end_token()}"


class MyFormattedModel(FormattingModel):
    name: str
    age: int
    city: str

    @classmethod
    def format_spec(cls) -> tuple[str, ParserElement]:
        template = "name: {NAME}\n{AGE} is the age\nlives in {CITY}"
        name = Suppress("name:") + Word(alphanums + " ")("NAME") + LineEnd()
        age = Word(alphanums)("AGE") + Suppress("is the age") + LineEnd()
        city = Suppress("lives in") + SkipTo(LineEnd())("CITY")
        parser = name + age + city
        return template, parser

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"

    @classmethod
    def field_mappings(cls) -> Dict[str, str]:
        return {"name": "NAME", "age": "AGE", "city": "CITY"}


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def format_spec(cls) -> tuple[str, ParserElement]:
        template = "code_file_model\nfile_path: {FILE_PATH}\n```{LANGUAGE}\n{CODE}\n```"
        file_path = (
            Suppress("code_file_model")
            + LineEnd()
            + Suppress("file_path:")
            + SkipTo(LineEnd())("FILE_PATH")
            + LineEnd()
        )
        code_block = (
            Suppress("```")
            + Word(alphanums)("LANGUAGE")
            + LineEnd()
            + Regex(r"(?s).*?(?=```)").set_parse_action(lambda s, l, t: t[0].strip())(
                "CODE"
            )
            + Suppress("```")
        )
        parser = file_path + code_block
        return template, parser

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"

    @classmethod
    def field_mappings(cls) -> Dict[str, str]:
        return {"file_path": "FILE_PATH", "language": "LANGUAGE", "code": "CODE"}


if __name__ == "__main__":
    # Test MyFormattedModel
    model = MyFormattedModel(name="John", age=30, city="Tokyo")
    generated = model.generate()
    print("Generated MyFormattedModel string:")
    print(generated)
    print()

    parsed = MyFormattedModel.parse(generated)
    print("Parsed MyFormattedModel object:")
    print(parsed)
    print()

    print("MyFormattedModel Round-trip test:")
    assert model == parsed, "MyFormattedModel: Original != Parsed"
    print("Passed!")
    print()

    # Test CodeFileModel
    code_model = CodeFileModel(
        language="python",
        file_path="src/main.py",
        code='def hello():\n    print("Hello, World!")',
    )
    code_generated = code_model.generate()
    print("Generated CodeFileModel string:")
    print(code_generated)
    print()

    code_parsed = CodeFileModel.parse(code_generated)
    print("Parsed CodeFileModel object:")
    print(code_parsed)
    print()

    print("CodeFileModel Round-trip test:")
    assert code_model == code_parsed, "CodeFileModel: Original != Parsed"
    print("Passed!")

    print("\nAll tests passed successfully!")
