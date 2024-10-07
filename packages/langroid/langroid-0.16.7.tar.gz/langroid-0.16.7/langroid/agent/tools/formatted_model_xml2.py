import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any, Dict
from xml.dom import minidom

from langroid.pydantic_v1 import BaseModel


class FormattingModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def format_spec(cls):
        pass

    @classmethod
    @abstractmethod
    def parse_spec(cls) -> Dict[str, str]:
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
    def format(cls, instance: "FormattingModel") -> str:
        spec = cls.format_spec()
        formatted = spec(**instance.dict())
        return f"{cls.start_token()}\n{formatted}\n{cls.end_token()}"

    @classmethod
    def parse(cls, formatted_string: str) -> "FormattingModel":
        content = formatted_string.strip()
        start_token = cls.start_token().strip()
        end_token = cls.end_token().strip()

        if not content.lower().startswith(
            start_token.lower()
        ) or not content.lower().endswith(end_token.lower()):
            raise ValueError("Invalid start or end token")

        content = content[len(start_token) :].strip()
        content = content[: -len(end_token)].strip()

        spec = cls.parse_spec()
        parsed = cls._parse_xml(content, spec)
        return cls(**parsed)

    @staticmethod
    def _parse_xml(content: str, spec: Dict[str, str]) -> Dict[str, Any]:
        root = ET.fromstring(content)
        result = {}
        for field, xpath in spec.items():
            element = root.find(xpath)
            if element is not None:
                if field == "code":
                    result[field] = element.text.strip() if element.text else ""
                else:
                    result[field] = element.text.strip() if element.text else ""
            else:
                raise ValueError(f"Required field '{field}' not found in XML")
        return result


class CodeFileModel(FormattingModel):
    language: str
    file_path: str
    code: str

    @classmethod
    def format_spec(cls):
        def xml_formatter(file_path: str, language: str, code: str) -> str:
            root = ET.Element("code_file_model")

            file_path_elem = ET.SubElement(root, "file_path")
            file_path_elem.text = file_path

            language_elem = ET.SubElement(root, "language")
            language_elem.text = language

            code_elem = ET.SubElement(root, "code")
            code_elem.text = f"\n{code}\n"

            xml_str = ET.tostring(root, encoding="unicode")
            pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

            # Remove the XML declaration
            pretty_xml = "\n".join(pretty_xml.split("\n")[1:])

            return pretty_xml.strip()

        return xml_formatter

    @classmethod
    def parse_spec(cls) -> Dict[str, str]:
        return {
            "file_path": ".//file_path",
            "language": ".//language",
            "code": ".//code",
        }

    @classmethod
    def start_token(cls):
        return "<format>"

    @classmethod
    def end_token(cls):
        return "</format>"


# Test cases
if __name__ == "__main__":
    # Test formatting
    code_file = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
    )
    formatted = CodeFileModel.format(code_file)
    print("Formatted output:")
    print(formatted)
    print("Formatting test passed.")

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
    tolerant_input = """<format>
  <code_file_model>
    <file_path>  src/main.py  </file_path>
    <language>  Python  </language>
    <code>
def hello():
    print('Hello, World!')
    </code>
  </code_file_model>
</format>"""
    parsed_tolerant = CodeFileModel.parse(tolerant_input)
    expected_tolerant = CodeFileModel(
        language="Python",
        file_path="src/main.py",
        code="def hello():\n    print('Hello, World!')",
    )
    assert (
        parsed_tolerant == expected_tolerant
    ), f"Tolerant parsing failed. Expected:\n{expected_tolerant}\nGot:\n{parsed_tolerant}"
    print("Tolerant parsing test passed.")

    print("All tests passed successfully!")
