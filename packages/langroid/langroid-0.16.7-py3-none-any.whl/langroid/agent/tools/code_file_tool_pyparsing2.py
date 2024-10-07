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

from typing import Callable, List, Tuple, Type

from pyparsing import (
    Literal,
    Optional,
    SkipTo,
    White,
    Word,
    alphanums,
    lineEnd,
    printables,
)

from langroid.agent.tool_message import ToolMessage
from langroid.agent.tools.generic_tool import GenericTool
from langroid.utils.constants import TOOL, TOOL_END

CODE_FENCE_START = "`" * 3
CODE_FENCE_END = "`" * 3


class CodeFileTool(GenericTool):
    """
    Used by LLM to specify contents of a code file.
    """

    request: str = "code_file_tool"
    purpose: str = """
    To specify the <contents> of a code file at <file_path>,
    containing code in a specific <language>.
    """
    file_path: str
    contents: str
    language: str

    @classmethod
    def define_grammar(cls):
        TOOL_START = Literal(TOOL + ":")
        CODE_FENCE = Literal("```")

        file_path = SkipTo(lineEnd)("file_path")
        language = Word(alphanums)("language")
        contents = SkipTo(lineEnd + CODE_FENCE)("contents")

        grammar = (
            TOOL_START
            + Optional(White())
            + Optional(Word(printables), default=cls.default_value("request"))(
                "request"
            )
            + lineEnd
            + Optional(White())
            + file_path
            + lineEnd
            + CODE_FENCE
            + Optional(White())
            + language
            + lineEnd
            + contents
            + lineEnd
            + CODE_FENCE
            + lineEnd
            + Optional(White())
            + Literal(TOOL_END)
            + Optional(White())
        )
        return grammar

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

    def __repr__(self):
        return f"""CodeFileTool(
            file_path='{self.file_path}', 
            language='{self.language}',
            contents='{self.contents}')
            """


if __name__ == "__main__":
    # Informal test to print instructions for CodeFileTool
    print("Testing CodeFileTool instructions:")
    print("-" * 50)

    instructions = CodeFileTool.instructions()
    print(instructions)

    print("-" * 50)
    print("End of instructions test")

    # You can add more informal tests here if needed
    # For example, testing the parse method:
    print("\nTesting CodeFileTool parse method:")
    print("-" * 50)

    test_input = """TOOL: code_file_tool
    src/main.py
    ```python
    def hello_world():
        print("Hello, World!")
    
    if __name__ == "__main__":
        hello_world()
    ```
    TOOL_END"""

    parsed_result = CodeFileTool.parse(test_input)
    print("Parsed result:")
    for key, value in parsed_result.items():
        print(f"{key}: {value}")

    print("-" * 50)
    print("End of parse test")

    # Test format method
    print("\nTesting CodeFileTool format method:")
    print("-" * 50)
    test_instance = CodeFileTool(
        request="code_file_tool",
        file_path="tests/test_file.py",
        language="python",
        contents="""
def test_function():
    assert 1 + 1 == 2

if __name__ == "__main__":
    test_function()
""",
    )
    formatted_output = CodeFileTool.format(test_instance)
    print("Formatted output:")
    print(formatted_output)
    print("-" * 50)
    print("End of format test")

    # Additional test: Round-trip (parse -> format -> parse)
    print("\nTesting CodeFileTool round-trip (parse -> format -> parse):")
    print("-" * 50)
    initial_parse = CodeFileTool.parse(test_input)
    initial_instance = CodeFileTool(**initial_parse)
    formatted_output = CodeFileTool.format(initial_instance)
    final_parse = CodeFileTool.parse(formatted_output)

    print("Initial parse:")
    print(initial_parse)
    print("\nFormatted output:")
    print(formatted_output)
    print("\nFinal parse:")
    print(final_parse)

    if initial_parse == final_parse:
        print("\nRound-trip test passed: Initial and final parses match.")
    else:
        print("\nRound-trip test failed: Initial and final parses do not match.")
    print("-" * 50)
    print("End of round-trip test")
