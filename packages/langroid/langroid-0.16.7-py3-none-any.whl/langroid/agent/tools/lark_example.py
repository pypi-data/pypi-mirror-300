from typing import ClassVar

from lark import Lark, Transformer, Tree

from langroid.pydantic_v1 import BaseModel


class Person(BaseModel):
    name: str
    age: int
    city: str

    # Class variable to hold the grammar
    grammar: ClassVar[
        str
    ] = """
    start: "START Person" "\n" field ("---" "\n" field)* "END Person"
    field: NAME "=" VALUE
    NAME: "name" | "age" | "city"
    VALUE: /[^\n]+/

    %import common.WS
    %ignore WS
    """

    @classmethod
    def from_string(cls, string: str) -> "Person":
        parser = Lark(cls.grammar, parser="lalr", transformer=PersonTransformer())
        result = parser.parse(string)
        return cls(**result)

    def to_string(self) -> str:
        parser = Lark(self.grammar, parser="lalr")
        tree = Tree(
            "start",
            [
                Tree("field", [Tree("NAME", [name]), Tree("VALUE", [str(value)])])
                for name, value in self.dict().items()
            ],
        )
        return parser.serialize(tree)


class PersonTransformer(Transformer):
    def start(self, items):
        return dict(items)

    def field(self, items):
        name, value = items
        if name == "age":
            value = int(value)
        return name, value


# Example usage:
if __name__ == "__main__":
    # Create a Person instance
    p = Person(name="John Doe", age=30, city="New York")

    # Convert to string
    s = p.to_string()
    print("To string:")
    print(s)
    print()

    # Parse from string
    p2 = Person.from_string(s)
    print("Parsed from string:")
    print(p2)

    # Demonstrate that they're equal
    print("\nAre equal:", p == p2)
