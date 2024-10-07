import re
from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar

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
    @abstractmethod
    def field_mappings(cls) -> Dict[str, str]:
        pass

    @classmethod
    def parse(cls: Type[T], text: str) -> T:
        # Remove start and end tokens
        content = text.strip()[len(cls.start_token()) : -len(cls.end_token())].strip()

        # Create regex pattern from format_spec
        pattern = cls.format_spec()
        for field, token in cls.field_mappings().items():
            pattern = pattern.replace(token, f"(?P<{field}>.*?)")

        # Extract data using regex
        match = re.match(pattern, content, re.DOTALL)
        if not match:
            raise ValueError("Invalid format")

        # Create instance with extracted data
        data = {field: match.group(field).strip() for field in cls.field_mappings()}
        return cls(**data)

    def generate(self) -> str:
        # Start with the format spec
        result = self.format_spec()

        # Replace tokens with actual values
        for field, token in self.field_mappings().items():
            value = getattr(self, field)
            result = result.replace(token, str(value))

        # Wrap with start and end tokens
        return f"{self.start_token()}\n{result}\n{self.end_token()}"


class MyFormattedModel(FormattingModel):
    name: str
    age: int
    city: str

    @classmethod
    def format_spec(cls) -> str:
        return "name: {NAME}\n{AGE} is the age\nlives in {CITY}"

    @classmethod
    def start_token(cls) -> str:
        return "<format>"

    @classmethod
    def end_token(cls) -> str:
        return "</format>"

    @classmethod
    def field_mappings(cls) -> Dict[str, str]:
        return {"name": "{NAME}", "age": "{AGE}", "city": "{CITY}"}


if __name__ == "__main__":
    # Test object to string
    model = MyFormattedModel(name="John", age=30, city="Tokyo")
    generated = model.generate()
    print("Generated string:")
    print(generated)
    print()

    # Test string to object
    parsed = MyFormattedModel.parse(generated)
    print("Parsed object:")
    print(parsed)
    print()

    # Test round-trip
    print("Round-trip test:")
    print("Original == Parsed:", model == parsed)

    # Test with different values
    another_model = MyFormattedModel(name="Alice", age=25, city="New York")
    another_generated = another_model.generate()
    print("\nAnother generated string:")
    print(another_generated)
    print()

    another_parsed = MyFormattedModel.parse(another_generated)
    print("Another parsed object:")
    print(another_parsed)
    print("Another Original == Another Parsed:", another_model == another_parsed)

    # code file model
    class CodeFileModel(FormattingModel):
        language: str
        file_path: str
        code: str

        @classmethod
        def format_spec(cls) -> str:
            return "code_file_model\nfile_path: {FILE_PATH}\n```{LANGUAGE}\n{CODE}\n```"

        @classmethod
        def start_token(cls) -> str:
            return "<format>"

        @classmethod
        def end_token(cls) -> str:
            return "</format>"

        @classmethod
        def field_mappings(cls) -> Dict[str, str]:
            return {
                "file_path": "{FILE_PATH}",
                "language": "{LANGUAGE}",
                "code": "{CODE}",
            }

    print("\nTesting CodeFileModel:")
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
    print("Original == Parsed:", code_model == code_parsed)

    # tolerant format
    #
    class CodeFileModel(FormattingModel):
        language: str
        file_path: str
        code: str

        @classmethod
        def format_spec(cls) -> str:
            return (
                r"code_file_model\s*\n"
                r"file_path:\s*{FILE_PATH}\s*\n"
                r"```\s*{LANGUAGE}\s*\n"
                r"{CODE}\s*"
                r"```"
            )

        @classmethod
        def start_token(cls) -> str:
            return "<format>"

        @classmethod
        def end_token(cls) -> str:
            return "</format>"

        @classmethod
        def field_mappings(cls) -> Dict[str, str]:
            return {
                "file_path": "{FILE_PATH}",
                "language": "{LANGUAGE}",
                "code": "{CODE}",
            }

    print("\nTesting CodeFileModel with various whitespace variations:")

    test_strings = [
        # Standard format
        """<format>
code_file_model
file_path: src/main.py
```python
def hello():
    print("Hello, World!")
```
</format>""",
        # Extra whitespace
        """<format>
code_file_model  
file_path:     src/main.py    
```   python   
def hello():
    print("Hello, World!")
```
</format>""",
        # Extra newlines
        """<format>
code_file_model

file_path: src/main.py

```python

def hello():
    print("Hello, World!")

```

</format>""",
    ]

    for i, test_string in enumerate(test_strings, 1):
        print(f"\nTest {i}:")
        print("Input string:")
        print(test_string)

        parsed = CodeFileModel.parse(test_string)
        print("\nParsed object:")
        print(parsed)

        regenerated = parsed.generate()
        print("\nRegenerated string:")
        print(regenerated)

        reparsed = CodeFileModel.parse(regenerated)
        print("\nRound-trip test:")
        print("Original parsed == Reparsed:", parsed == reparsed)
        print("-" * 50)
