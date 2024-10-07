from abc import ABC, abstractmethod
from typing import get_type_hints

from lxml import etree

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def root_element(cls) -> str:
        pass

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        parser = etree.XMLParser(strip_cdata=False)
        root = etree.fromstring(formatted_string.encode("utf-8"), parser=parser)
        if root.tag != cls.root_element():
            raise ValueError(
                f"Invalid root element: expected {cls.root_element()}, got {root.tag}"
            )

        data = {}
        type_hints = get_type_hints(cls)
        for elem in root:
            field_type = type_hints.get(elem.tag, str)
            if elem.tag == "code":
                data[elem.tag] = elem.text if elem.text else ""
            else:
                # Parse according to the field type
                value = elem.text.strip() if elem.text else ""
                if field_type == int:
                    data[elem.tag] = int(value)
                elif field_type == float:
                    data[elem.tag] = float(value)
                elif field_type == bool:
                    data[elem.tag] = value.lower() in ("true", "1", "yes")
                else:
                    data[elem.tag] = value

        return cls(**data)

    @classmethod
    def instructions(cls) -> str:
        # Get only the fields defined in the model
        fields = list(cls.__fields__.keys())

        # Preamble with placeholder variables
        preamble = "Placeholders:\n"
        for field in fields:
            preamble += f"{field.upper()} = [value for {field}]\n"

        # Formatting example
        example = f"Formatting example:\n\n<{cls.root_element()}>\n"
        for field in fields:
            if field == "code":
                example += f"  <{field}><![CDATA[{{{field.upper()}}}]]></{field}>\n"
            else:
                example += f"  <{field}>{{{field.upper()}}}</{field}>\n"
        example += f"</{cls.root_element()}>"

        return f"{preamble}\n{example}"

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        root = etree.Element(cls.root_element())
        for name, value in instance.dict().items():
            elem = etree.SubElement(root, name)
            if name == "code":
                elem.text = etree.CDATA(str(value))
            else:
                elem.text = str(value)
        return etree.tostring(root, encoding="unicode", pretty_print=True)


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str
    line_count: int
    average_line_length: float
    is_executable: bool

    @classmethod
    def root_element(cls):
        return "code_file_model"


if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
        line_count=2,
        average_line_length=20.5,
        is_executable=True,
    )
    formatted = CodeFileModel.format(code_file)
    print("Formatted XML:")
    print(formatted)

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
        line_count=3,
        average_line_length=15.33,
        is_executable=False,
    )
    formatted2 = CodeFileModel.format(code_file2)
    parsed2 = CodeFileModel.parse(formatted2)
    assert (
        parsed2 == code_file2
    ), f"Parsing failed for different values. Expected:\n{code_file2}\nGot:\n{parsed2}"
    print("Different values test passed.")

    # Test tolerant parsing
    tolerant_input = """
    <code_file_model>
        <language>  Python  </language>
        <file_path>   src/main.py   </file_path>
        <code><![CDATA[
def hello():
    print('Hello, World!')
        ]]></code>
        <line_count> 2 </line_count>
        <average_line_length> 20.5 </average_line_length>
        <is_executable> True </is_executable>
    </code_file_model>
    """
    parsed_tolerant = CodeFileModel.parse(tolerant_input)
    expected_tolerant = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="\ndef hello():\n    print('Hello, World!')\n        ",
        line_count=2,
        average_line_length=20.5,
        is_executable=True,
    )
    assert (
        parsed_tolerant == expected_tolerant
    ), f"Tolerant parsing failed. Expected:\n{expected_tolerant}\nGot:\n{parsed_tolerant}"
    print("Tolerant parsing test passed.")

    print(CodeFileModel.instructions())

    print("All tests passed successfully!")
