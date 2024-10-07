from typing import get_type_hints

from lxml import etree

from langroid.agent.tool_message import ToolMessage


class XmlToolMessage(ToolMessage):
    """
    Abstract class for tools formatted using XML instead of JSON.
    """

    request: str
    purpose: str

    _allow_llm_use = True

    class Config(ToolMessage.Config):
        root_element = "tool"

    @classmethod
    def parse(cls, formatted_string: str) -> "XmlToolMessage":
        parser = etree.XMLParser(strip_cdata=False)
        root = etree.fromstring(formatted_string.encode("utf-8"), parser=parser)
        if root.tag != cls.Config.root_element:
            raise ValueError(
                f"Invalid root element: expected {cls.Config.root_element}, got {root.tag}"
            )

        data = {}
        type_hints = get_type_hints(cls)
        exclude_fields = cls.Config.schema_extra.get("exclude", set())
        for elem in root:
            if elem.tag not in exclude_fields:
                field_type = type_hints.get(elem.tag, str)
                if elem.tag == "code":
                    data[elem.tag] = elem.text if elem.text else ""
                else:
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
        fields = [
            f
            for f in cls.__fields__.keys()
            if f not in cls.Config.schema_extra.get("exclude", set())
        ]

        preamble = "Placeholders:\n"
        for field in fields:
            preamble += f"{field.upper()} = [value for {field}]\n"

        example = f"Formatting example:\n\n<{cls.Config.root_element}>\n"
        for field in fields:
            if field == "code":
                example += f"  <{field}><![CDATA[{{{field.upper()}}}]]></{field}>\n"
            else:
                example += f"  <{field}>{{{field.upper()}}}</{field}>\n"
        example += f"</{cls.Config.root_element}>"

        return f"{preamble}\n{example}"

    @classmethod
    def format(cls, instance: "XmlToolMessage") -> str:
        root = etree.Element(cls.Config.root_element)
        exclude_fields = cls.Config.schema_extra.get("exclude", set())
        for name, value in instance.dict().items():
            if name not in exclude_fields:
                elem = etree.SubElement(root, name)
                if name == "code":
                    elem.text = etree.CDATA(str(value))
                else:
                    elem.text = str(value)
        return etree.tostring(root, encoding="unicode", pretty_print=True)

    @classmethod
    def find_candidates(cls, text: str) -> str:
        root_tag = cls.Config.root_element
        opening_tag = f"<{root_tag}>"
        closing_tag = f"</{root_tag}>"

        candidates = []
        start = 0
        while True:
            start = text.find(opening_tag, start)
            if start == -1:
                break
            end = text.find(closing_tag, start)
            if end == -1:
                # For the last candidate, allow missing closing tag
                candidates.append(text[start:])
                break
            candidates.append(text[start : end + len(closing_tag)])
            start = end + len(closing_tag)

        return "\n".join(candidates)
