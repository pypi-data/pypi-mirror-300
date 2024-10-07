from abc import abstractmethod
from typing import Any, Dict, List

from pyparsing import (
    LineEnd,
    Literal,
    ParserElement,
)

from langroid.agent.tool_message import ToolMessage


class GenericTool(ToolMessage):
    """
    Abstract class for a tool whose format is defined by a grammar,
    and not necessarily JSON-based.
    Especially useful for tools where we need an LLM to return code.
    Most LLMs, especially weaker ones, have significant issues
    (related to unescaped newlines, quotes, etc) when returning code within JSON.
    """

    @classmethod
    @abstractmethod
    def define_grammar(cls):
        """Define the grammar for the specific tool."""
        pass

    @classmethod
    def create_parser(cls):
        """Create a parser based on the defined grammar."""
        grammar = cls.define_grammar()
        # Use the grammar to create and return a parser
        return grammar

    @classmethod
    def parse(cls, string) -> Dict[str, Any]:
        parser = cls.create_parser()
        try:
            result = parser.parseString(string, parseAll=True)
            return {
                name: result[name]
                for name in result.keys()
                if name and not name.startswith("_")
            }
        except Exception as e:
            print(f"Parsing failed: {e}")
            return {}

    @classmethod
    def instructions(cls) -> str:
        preamble = "Preamble:\n"
        for field, field_info in cls.__dict__["__fields__"].items():
            preamble += (
                f"<{field}> denotes the value of the `{field}` field "
                f"(type: {field_info.type_})\n"
            )

        parser = cls.create_parser()

        def format_element(element):
            if isinstance(element, Literal):
                return element.match
            elif hasattr(element, "resultsName") and element.resultsName:
                return f"<{element.resultsName}>"
            elif isinstance(element, LineEnd):
                return "\n"
            return ""

        def traverse_parser(parser_element):
            if isinstance(parser_element, ParserElement):
                if hasattr(parser_element, "exprs"):
                    return "".join(
                        traverse_parser(expr) for expr in parser_element.exprs
                    )
                else:
                    return format_element(parser_element)
            return str(parser_element)

        template = traverse_parser(parser)

        return f"{preamble}\nFormatted Example:\n{template.strip()}"

    @classmethod
    def parse(cls, string) -> Dict[str, Any]:
        parser = cls.create_parser()
        try:
            result = parser.parseString(string, parseAll=True)
            return {
                name: result[name]
                for name in result.keys()
                if name and not name.startswith("_")
            }
        except Exception as e:
            print(f"Parsing failed: {e}")
            return {}

    @classmethod
    def format(cls, instance) -> str:
        parser = cls.create_parser()

        def format_element(element):
            if isinstance(element, Literal):
                return element.match
            elif hasattr(element, "resultsName") and element.resultsName:
                return getattr(instance, element.resultsName, "")
            elif isinstance(element, LineEnd):
                return "\n"
            return ""

        def traverse_parser(parser_element):
            if isinstance(parser_element, ParserElement):
                if hasattr(parser_element, "exprs"):
                    return "".join(
                        traverse_parser(expr) for expr in parser_element.exprs
                    )
                else:
                    return format_element(parser_element)
            return str(parser_element)

        formatted_string = traverse_parser(parser)

        return formatted_string.strip()

    @classmethod
    def from_string(cls, input_string: str) -> "CodeFileTool":
        """Parse a string into a CodeFileTool object, using the TEMPLATE."""
        parsed_data = cls.parse(input_string)
        if parsed_data:
            return cls(**parsed_data)
        raise ValueError("Invalid input string format")

    @classmethod
    def to_string(cls, instance) -> str:
        """Convert a CodeFileTool object to a string, using the TEMPLATE."""
        return cls.format(instance)

    @classmethod
    def find_candidates(cls, input_str: str) -> List[str]:
        """
        Find all possible (top-level) candidates for
        CodeFileTool in the input string.
        """
        parser = cls.create_parser()
        candidates = []

        for tokens, start, end in parser.scanString(input_str):
            candidates.append(input_str[start:end])

        return candidates

    def __str__(self):
        return self.to_string()

    # def __repr__(self) -> str:
    #     class_name = self.__class__.__name__
    #     attributes = []
    #     for key, value in self.__dict__.items():
    #         if not key.startswith('_'):  # Skip private attributes
    #             if isinstance(value, str):
    #                 # Escape quotes and newlines in string values
    #                 value_repr = f"'{value.replace('\\', '\\\\').replace(\"'\", \"\\'\").replace('\\n', '\\n')}'"
    #             else:
    #                 value_repr = repr(value)
    #             attributes.append(f"{key}={value_repr}")
    #     return f"{class_name}({', '.join(attributes)})"
