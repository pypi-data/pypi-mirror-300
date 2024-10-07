import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def spec(cls):
        pass

    @classmethod
    @abstractmethod
    def root_element(cls) -> str:
        pass

    @classmethod
    def format(cls, instance: "FormattingModel") -> str:
        root = ET.Element(cls.root_element())
        for field, field_type in cls.spec().items():
            value = getattr(instance, field)
            elem = ET.SubElement(root, field)
            if field_type == "cdata":
                elem.text = f"<![CDATA[{value}]]>"
            else:
                elem.text = value
        return ET.tostring(root, encoding="unicode", method="xml")

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        root = ET.fromstring(formatted_string)
        if root.tag != cls.root_element():
            raise ValueError(
                f"Invalid root element: expected {cls.root_element()}, got {root.tag}"
            )

        data = {}
        for field, field_type in cls.spec().items():
            elem = root.find(field)
            if elem is None:
                raise ValueError(f"Missing field: {field}")
            if field_type == "cdata":
                # Extract CDATA content
                cdata_start = elem.text.find("<![CDATA[")
                cdata_end = elem.text.rfind("]]>")
                if cdata_start != -1 and cdata_end != -1:
                    data[field] = elem.text[cdata_start + 9 : cdata_end]
                else:
                    data[field] = elem.text
            else:
                data[field] = elem.text.strip() if elem.text else ""

        return cls(**data)


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def spec(cls):
        return {"language": "text", "file_path": "text", "code": "cdata"}

    @classmethod
    def root_element(cls):
        return "code_file_model"


# Test cases
if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
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
    </code_file_model>
    """
    parsed_tolerant = CodeFileModel.parse(tolerant_input)
    expected_tolerant = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="\ndef hello():\n    print('Hello, World!')\n        ",
    )
    assert (
        parsed_tolerant == expected_tolerant
    ), f"Tolerant parsing failed. Expected:\n{expected_tolerant}\nGot:\n{parsed_tolerant}"
    print("Tolerant parsing test passed.")

    print("All tests passed successfully!")
