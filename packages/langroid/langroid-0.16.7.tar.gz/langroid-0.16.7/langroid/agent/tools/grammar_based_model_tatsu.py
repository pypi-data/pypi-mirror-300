from abc import ABC, abstractmethod
from typing import ClassVar, Dict

from tatsu import compile as compile_grammar
from tatsu.model import ModelBuilder

from langroid.pydantic_v1 import BaseModel


class GrammarBasedModel(BaseModel, ABC):
    grammar: ClassVar[str]
    start_token: ClassVar[str]
    end_token: ClassVar[str]
    field_mappings: ClassVar[Dict[str, str]]

    @classmethod
    @abstractmethod
    def get_grammar(cls) -> str:
        pass

    @classmethod
    def parse(cls, text: str) -> "GrammarBasedModel":
        parser = compile_grammar(cls.get_grammar())
        ast = parser.parse(text, start="start")
        model_dict = {
            field: getattr(ast, rule) for field, rule in cls.field_mappings.items()
        }
        return cls(**model_dict)

    def generate(self) -> str:
        grammar = compile_grammar(self.get_grammar())
        model_builder = ModelBuilder()
        for field, rule in self.field_mappings.items():
            setattr(model_builder, rule, getattr(self, field))
        ast = model_builder.start()
        return f"{self.start_token}\n{grammar.parse(str(ast), start='start')}\n{self.end_token}"


class PersonSpec(GrammarBasedModel):
    name: str
    age: int
    city: str

    grammar = """
        start = name_line age_line city_line;
        name_line = 'name:' /\s*/ name:/.+/ EOL;
        age_line = 'age is' /\s*/ age:/\d+/ EOL;
        city_line = 'lives in' /\s*/ city:/.+/ EOL;
        EOL = /\r?\n/;
    """
    start_token = "<spec>"
    end_token = "</spec>"
    field_mappings = {"name": "name", "age": "age", "city": "city"}

    @classmethod
    def get_grammar(cls):
        return cls.grammar


if __name__ == "__main__":
    # Test parsing
    input_str = """<spec>
name: John Doe
age is 30
lives in New York
</spec>"""
    person = PersonSpec.parse(input_str)
    print("Parsed person:", person)

    # Test generation
    generated_str = person.generate()
    print("\nGenerated string:")
    print(generated_str)

    # Test round-trip
    round_trip_person = PersonSpec.parse(generated_str)
    print("\nRound-trip parsed person:", round_trip_person)

    assert person == round_trip_person, "Round-trip parsing failed"
    print("\nRound-trip test passed!")
