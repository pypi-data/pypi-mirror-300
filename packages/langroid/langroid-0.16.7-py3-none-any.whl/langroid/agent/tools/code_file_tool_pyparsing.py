""""
Non-JSON Tool for LLM to specify contents of a code file.

Why Non-JSON?  Because there are numerous issues with even the best LLMs trying
to return code within JSON strings (e.g. unescaped newlines, quotes, etc.),
and the problem is even worse with weak LLMs. Json repair methods exist, but
can't deal with all possible cases.

E.g. see this study from Aider: https://aider.chat/2024/08/14/code-in-json.html

Note: We express the formatting rules with a template since it has several benefits:
    - all of the formatting rules are in one place, 
    - we get a parser for free, and don't have to write parsing code,
    - we get a formatting example generator for free, and don't have to write
        example generation code.
    - consistency between the parser and the example generator is guaranteed.        
"""

from typing import Any, Callable, Dict, List, Tuple, Type

from pyparsing import (
    LineEnd,
    Literal,
    Optional,
    ParserElement,
    SkipTo,
    White,
    Word,
    alphanums,
    lineEnd,
    printables,
)

from langroid.agent.tool_message import ToolMessage
from langroid.utils.constants import TOOL, TOOL_END

CODE_FENCE_START = "`" * 3
CODE_FENCE_END = "`" * 3


class CodeFileTool(ToolMessage):
    """
    Used by LLM to specify contents of a code file.
    """

    request: str = "code_file_tool"
    purpose: str = """
        To specify the contents of a code file.
        """
    file_path: str
    contents: str
    language: str

    @classmethod
    def create_parser(cls):
        TOOL_START = Literal(TOOL + ":")
        CODE_FENCE = Literal("```")

        file_path = SkipTo(lineEnd)("file_path")
        language = Word(alphanums)("language")
        contents = SkipTo(CODE_FENCE)("contents")

        parser = (
            TOOL_START
            + Optional(Word(printables), default=cls.default_value("request"))(
                "request"
            )
            + lineEnd
            + file_path
            + lineEnd
            + CODE_FENCE
            + Optional(White())  # Allow space after ```
            + language
            + lineEnd
            + contents
            + CODE_FENCE
            + lineEnd  # Add this line to expect a newline after the closing fence
            + Literal(TOOL_END)
        )
        return parser

    @classmethod
    def parse(cls, string) -> Dict[str, Any]:
        parser = cls.create_parser()
        try:
            result = parser.parseString(string, parseAll=True)
            return {
                "request": result["request"],
                "file_path": result["file_path"].strip(),
                "language": result["language"],
                "contents": result["contents"].strip(),
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
            elif element.resultsName:
                if element.resultsName == "request":
                    return instance.request
                elif element.resultsName == "file_path":
                    return instance.file_path
                elif element.resultsName == "language":
                    return instance.language
                elif element.resultsName == "contents":
                    return f"{instance.contents}\n"  # Add newline after contents
            elif isinstance(element, LineEnd):
                return "\n"
            return ""

        def traverse_parser(parser_element):
            if isinstance(parser_element, ParserElement):
                if isinstance(parser_element, SkipTo):
                    return format_element(parser_element)
                elif hasattr(parser_element, "exprs"):
                    return "".join(
                        traverse_parser(expr) for expr in parser_element.exprs
                    )
                else:
                    return format_element(parser_element)
            return str(parser_element)

        formatted_string = traverse_parser(parser)

        return formatted_string.strip()

    @classmethod
    def create(cls, get_directory: Callable[[], str]) -> Type["CodeFileTool"]:
        """
        Create a subclass of CodeFileTool with a static method get_directory,
        which returns the current directory path, so that all file paths are
        interpreted as relative to the current directory.
        """

        class SubCodeFileTool(cls):
            get_directory: Callable[[], str] = staticmethod(get_directory)

        return SubCodeFileTool

    @classmethod
    def examples(cls) -> List[ToolMessage | Tuple[str, ToolMessage]]:
        return [
            cls(
                file_path="src/lib.rs",
                language="rust",
                contents="""
                    // function to add two numbers
                    pub fn add(a: i32, b: i32) -> i32 {
                        a + b
                    }
                    """,
            )
        ]

    @classmethod
    def find_candidates(cls, input_str: str) -> List[str]:
        """
        Find all possible (top-level) candidates for
        CodeFileTool in the input string.
        """
        # Use parse.findall to find all instances of the CodeFileTool pattern
        parser = compile(cls.get_template())
        matches = list(parser.findall(input_str))
        candidates = [match.fixed for match in matches]
        return candidates

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

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return f"""CodeFileTool(
            file_path='{self.file_path}', 
            language='{self.language}',
            contents='{self.contents}')
            """
