from abc import ABC, abstractmethod
from typing import ClassVar

from parse import parse

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    START_TOKEN: ClassVar[str] = "<format>"
    END_TOKEN: ClassVar[str] = "</format>"

    @classmethod
    @abstractmethod
    def format_spec(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parse_spec(cls) -> str:
        pass

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        template = f"{cls.START_TOKEN}\n{{content}}\n{cls.END_TOKEN}"
        spec_template = cls.format_spec()
        formatted_content = spec_template.format(**instance.dict())
        return template.format(content=formatted_content)

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        outer_template = f"{cls.START_TOKEN}\n{{content}}\n{cls.END_TOKEN}"
        outer_parsed = parse(outer_template, formatted_string, case_sensitive=False)
        if not outer_parsed:
            raise ValueError("Invalid outer format")

        content = outer_parsed["content"]
        parse_template = cls.parse_spec()
        parsed = parse(parse_template, content, case_sensitive=False)
        if not parsed:
            raise ValueError(
                f"Failed to parse content:\n{content}\nusing spec:\n{parse_template}"
            )

        return cls(**parsed.named)


class PersonModel(FormattingModel):
    name: str
    age: int
    city: str

    START_TOKEN: ClassVar[str] = "<person>"
    END_TOKEN: ClassVar[str] = "</person>"

    @classmethod
    def format_spec(cls):
        return "name: {name}\n{age} is the age\nlives in {city}"

    @classmethod
    def parse_spec(cls):
        return "name: {name:S}\n{age:d} is the age\nlives in {city:S}"


# Tests
if __name__ == "__main__":
    # Test instance
    person = PersonModel(name="John Doe", age=30, city="New York")

    # Test formatting
    formatted_string = PersonModel.format(person)
    print("Formatted string:")
    print(formatted_string)
    assert formatted_string == (
        "<person>\n"
        "name: John Doe\n"
        "30 is the age\n"
        "lives in New York\n"
        "</person>"
    )

    # Test parsing
    parsed_person = PersonModel.parse(formatted_string)
    print("\nParsed person:", parsed_person)
    assert parsed_person == person

    # Test round trip
    round_trip_person = PersonModel.parse(PersonModel.format(person))
    assert round_trip_person == person

    # Test parsing with extra whitespace and different casing
    extra_whitespace_string = """
    <PERSON>
        Name:    John Doe   
        30    IS THE AGE  
        Lives    in    New York   
    </person>
    """
    parsed_extra_whitespace = PersonModel.parse(extra_whitespace_string)
    assert parsed_extra_whitespace == person

    print("All tests passed!")
