import re
from abc import ABC, abstractmethod

from langroid.pydantic_v1 import BaseModel


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
    def _create_regex_pattern(cls) -> str:
        spec = cls.format_spec()
        # Replace {field_name} with (?P<field_name>.*?)
        pattern = re.sub(r"\{(\w+)\}", lambda m: f"(?P<{m.group(1)}>.*?)", spec)
        # Replace newlines with \s* to allow flexible whitespace
        pattern = pattern.replace("\n", r"\s*")
        return f"{re.escape(cls.start_token())}\\s*{pattern}\\s*{re.escape(cls.end_token())}"

    @classmethod
    def parse(cls, text: str) -> "FormattingModel":
        pattern = cls._create_regex_pattern()
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return cls(**{k: v.strip() for k, v in match.groupdict().items()})
        raise ValueError(
            f"Text does not match the expected format. Pattern: {pattern}, Text: {text}"
        )

    def generate(self) -> str:
        content = self.format_spec().format(**self.dict())
        return f"{self.start_token()}\n{content}\n{self.end_token()}"


class PersonModel(FormattingModel):
    name: str
    age: int
    city: str

    @classmethod
    def format_spec(cls) -> str:
        return "name: {name}\nage is {age}\nlives in {city}"

    @classmethod
    def start_token(cls) -> str:
        return "<spec>"

    @classmethod
    def end_token(cls) -> str:
        return "</spec>"


def test_round_trip(model_class, input_string):
    # Parse the input string
    parsed_model = model_class.parse(input_string)
    print(f"Parsed model: {parsed_model}")

    # Generate a string from the parsed model
    generated_string = parsed_model.generate()
    print(f"Generated string:\n{generated_string}")

    # Parse the generated string
    reparsed_model = model_class.parse(generated_string)
    print(f"Reparsed model: {reparsed_model}")

    # Assert that the original parsed model and the reparsed model are equal
    assert (
        parsed_model == reparsed_model
    ), "Round trip failed: original and reparsed models are not equal"

    # Assert that all fields are present and have the correct types
    for field, field_type in model_class.__annotations__.items():
        assert hasattr(parsed_model, field), f"Field {field} is missing"
        assert isinstance(
            getattr(parsed_model, field), field_type
        ), f"Field {field} has incorrect type"

    print("Round trip test passed successfully!")


if __name__ == "__main__":
    # Test case 1: Standard formatting
    test_string1 = """
    <spec>
    name: John Doe
    age is 30
    lives in New York
    </spec>
    """
    test_round_trip(PersonModel, test_string1)

    print("\n" + "=" * 50 + "\n")

    # Test case 2: Varying whitespace
    test_string2 = "<spec>name:   Alice  \nage is    25   \nlives in    Tokyo</spec>"
    test_round_trip(PersonModel, test_string2)

    print("\n" + "=" * 50 + "\n")

    # Test case 3: Multiline values
    test_string3 = """
    <spec>
    name: Bob
    Smith
    age is 40
    lives in San
    Francisco
    </spec>
    """
    test_round_trip(PersonModel, test_string3)

    print("All tests passed successfully!")
