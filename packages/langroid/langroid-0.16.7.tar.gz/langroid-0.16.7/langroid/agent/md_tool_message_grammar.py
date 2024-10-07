"""
Subclass of `ToolMessage`, specialized for markdown-formatted structured messages.
Helpful when LLM is producing code as part of a tool-message -- code within JSON
tends to cause all kinds of issues, especially with weaker LLMs.
An LLM more reliably generates code within fenced blocks in a markdown doc.
"""

import re
import textwrap
from random import choice
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union

from langroid.agent.tool_message import ToolMessage
from langroid.language_models.base import LLMFunctionSpec
from langroid.pydantic_v1 import BaseModel, Extra


class FileContents(BaseModel):
    file_path: str
    contents: str


T = TypeVar("T", bound="MdToolMessage")

from lark import Lark

md_tool_message_grammar = """
    start: section+

    section: header content

    header: "#" WS WORD

    content: primitive
           | list
           | file_contents
           | list_file_contents

    primitive: value

    list: list_item+
    list_item: "-" WS value

    file_contents: "file_path:" WS FILEPATH NEWLINE CODE_BLOCK
    list_file_contents: file_contents+

    CODE_BLOCK: /```[^`]*```/
    FILEPATH: /[^\\n]+/
    WORD: /[a-zA-Z_]+/
    value: /[^\\n]+/

    %import common.WS
    %import common.NEWLINE
"""

parser = Lark(md_tool_message_grammar, start="start", parser="lalr")


def apply_grammar(markdown_content: str):
    tree = parser.parse(markdown_content)
    return tree


@classmethod
def from_markdown(cls: Type[T], markdown_content: str) -> T:
    """
    Parse markdown content and create an instance of the MdToolMessage subclass.
    """
    tree = apply_grammar(markdown_content)
    parsed_data = cls._extract_data_from_tree(tree)
    return cls(**parsed_data)


@classmethod
def _extract_data_from_tree(cls, tree):
    parsed_data = {}
    for section in tree.children:
        key = section.children[0].children[1].value.lower()
        value = cls._parse_content(section.children[1])
        parsed_data[key] = value
    return parsed_data


@classmethod
def _parse_content(cls, content):
    if content.data == "primitive":
        return cls._parse_primitive(content.children[0].value)
    elif content.data == "list":
        return [item.children[1].value for item in content.children]
    elif content.data == "file_contents":
        return cls._parse_file_contents(content)
    elif content.data == "list_file_contents":
        return [cls._parse_file_contents(fc) for fc in content.children]


@classmethod
def _parse_file_contents(cls, file_contents):
    file_path = file_contents.children[1].value
    content = file_contents.children[2].value.strip("`").strip()
    return FileContents(file_path=file_path, contents=content)


class MdToolMessage(ToolMessage):
    """
    Subclass of ToolMessage, with LLM instructions to generate markdown rather than
    json format.

    Limited to simple tool messages where each field is:
    - of type str, int, float, bool, FileContents, or list of these

    The corresponding markdown format would look like:

    ```md
    # request
    <request>

    # purpose
    <purpose>

    # <field1>
    <value1>

    # <field2>
    <value2>

    # <list_field>
    - item1
    - item2
    - item3


    # <list_of_file_contents_field_name>
    file_path:<file_path1>
    <contents1> (ensure code is in a fenced block, e.g. ```rust ... ```)
    file_path:<file_path2>
    <contents2>
    ...
    ```

    Attributes:
        request (str): name of agent method to map to. This is the method that
            would handle the LLM's generated tool call.
        purpose (str): purpose of agent method, expressed in general terms.
            (This is used when auto-generating the tool instruction to the LLM)
    """

    request: str
    purpose: str
    id: str = ""  # placeholder for OpenAI-API tool_call_id

    _allow_llm_use: bool = True  # allow an LLM to use (i.e. generate) this tool?

    # model_config = ConfigDict(extra=Extra.allow)

    class Config:
        # This is NOT inherited from ToolMessage.Config, so we do it here again
        extra = Extra.allow
        arbitrary_types_allowed = False
        validate_all = True
        validate_assignment = True
        # do not include these fields in the generated schema
        # since we don't require the LLM to specify them
        schema_extra = {"exclude": {"purpose", "id"}}

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for name, field in cls.__fields__.items():
            if name not in ["request", "purpose", "id"]:
                if field.type_ not in [
                    str,
                    int,
                    float,
                    bool,
                    FileContents,
                    List[str],
                    List[int],
                    List[float],
                    List[bool],
                    List[FileContents],
                ]:
                    raise ValueError(
                        f"""
                        Field '{name}' must be of type str, int, float, bool, 
                        or list of these, 
                        FileContents, or list of these
                        """
                    )

    @classmethod
    def examples(cls) -> List["ToolMessage" | Tuple[str, "ToolMessage"]]:
        """
        Examples to use in few-shot demos with markdown formatting instructions.
        Each example can be either:
        - just an MdToolMessage instance, e.g. MyTool(param1=1, param2="hello"), or
        - a tuple (description, MdToolMessage instance), where the description is
            a natural language "thought" that leads to the tool usage,
            e.g. ("I want to find the square of 5",  SquareTool(num=5))
            In some scenarios, including such a description can significantly
            enhance reliability of tool use.
        Returns:
        """
        return []

    @classmethod
    def usage_examples(cls, random: bool = False) -> str:
        """
        Instruction to the LLM showing examples of how to use the tool-message.

        Args:
            random (bool): whether to pick a random example from the list of examples.
                Set to `true` when using this to illustrate a dialog between LLM and
                user.
                (if false, use ALL examples)
        Returns:
            str: examples of how to use the tool/function-call
        """
        # pick a random example of the fields
        if len(cls.examples()) == 0:
            return ""
        if random:
            examples = [choice(cls.examples())]
        else:
            examples = cls.examples()
        examples_jsons = [
            (
                f"EXAMPLE {i}: (THOUGHT: {ex[0]}) => \n{ex[1].format_example()}"
                if isinstance(ex, tuple)
                else f"EXAMPLE {i}:\n {ex.format_example()}"
            )
            for i, ex in enumerate(examples, 1)
        ]
        return "\n\n".join(examples_jsons)

    def tree_to_markdown(tree):
        markdown = []
        for section in tree.children:
            header = section.children[0].children[1].value
            content = section.children[1]
            markdown.append(f"# {header}")
            markdown.append(cls._content_to_markdown(content))
        return "\n\n".join(markdown)

    @classmethod
    def _content_to_markdown(cls, content):
        if content.data == "primitive":
            return content.children[0].value
        elif content.data == "list":
            return "\n".join(f"- {item.children[1].value}" for item in content.children)
        elif content.data == "file_contents":
            return cls._file_contents_to_markdown(content)
        elif content.data == "list_file_contents":
            return "\n\n".join(
                cls._file_contents_to_markdown(fc) for fc in content.children
            )

    @classmethod
    def _file_contents_to_markdown(cls, file_contents):
        file_path = file_contents.children[1].value
        content = file_contents.children[2].value.strip("`").strip()
        return f"file_path: {file_path}\n{content}"

    def to_markdown(self) -> str:
        tree = apply_grammar(self.format_example())
        return tree_to_markdown(tree)

    def format_example(self) -> str:
        """
        Override json_example to use our new to_markdown method
        """
        return self.to_markdown()

    @classmethod
    def format_instructions(cls) -> str:
        fields = cls.__fields__
        excluded_fields = cls.Config.schema_extra.get("exclude", set())

        instructions = [
            cls._field_instruction(name, field)
            for name, field in fields.items()
            if name not in excluded_fields
        ]
        all_instructions = "\n\n".join(instructions)

        examples_str = ""
        if cls.examples():
            examples_str = "# Examples\n\n" + cls.usage_examples()

        return f"{all_instructions}\n\n{examples_str}"

    @classmethod
    def _field_instruction(cls, name: str, field: Any) -> str:
        field_type = field.outer_type_

        if field_type in (str, int, float, bool):
            return cls._primitive_instruction(name, field_type)
        elif field_type == FileContents:
            return cls._file_contents_instruction(name)
        elif field_type == List[str]:
            return cls._list_primitive_instruction(name, str)
        elif field_type == List[int]:
            return cls._list_primitive_instruction(name, int)
        elif field_type == List[float]:
            return cls._list_primitive_instruction(name, float)
        elif field_type == List[bool]:
            return cls._list_primitive_instruction(name, bool)
        elif field_type == List[FileContents]:
            return cls._list_file_contents_instruction(name)

        raise ValueError(f"Unsupported field type: {field_type}")

    @staticmethod
    def _primitive_instruction(name: str, field_type: Type[Any]) -> str:
        type_name = field_type.__name__
        return f"# {name}\n<{name}> ({type_name}, required)"

    @staticmethod
    def _list_primitive_instruction(name: str, item_type: Type[Any]) -> str:
        type_name = item_type.__name__
        return f"# {name}\n- <{name}1> ({type_name})\n- <{name}2> ({type_name})\n..."

    @staticmethod
    def _file_contents_instruction(name: str) -> str:
        return (
            f"# {name}\n"
            f"file_path: <file_path> (string)\n"
            f"<contents> "
            f"(string, ensure code is within code-fence, e.g. ```python ... ```)"
        )

    @staticmethod
    def _list_file_contents_instruction(name: str) -> str:
        return (
            f"# {name}\n"
            f"file_path: <file_path1> (string)\n"
            f"<contents1> "
            f"(string, ensure code is within code-fence, e.g. ```python ... ```)\n\n"
            f"file_path: <file_path2> (string)\n"
            f"<contents2> "
            f"(string, ensure code is within code-fence, e.g. ```python ... ```)\n"
            f"..."
        )

    @staticmethod
    def json_group_instructions() -> str:
        """Template for instructions for a group of tools.
        Works with GPT4 but override this for weaker LLMs if needed.
        """
        return textwrap.dedent(
            """
            === ALL AVAILABLE TOOLS and THEIR JSON FORMAT INSTRUCTIONS ===
            You have access to the following TOOLS to accomplish your task:

            {json_instructions}
            
            When one of the above TOOLs is applicable, you must express your 
            request as "TOOL:" followed by the request in the above JSON format.
            """
        )

    @classmethod
    def llm_function_schema(
        cls,
        request: bool = False,
        defaults: bool = True,
    ) -> LLMFunctionSpec:
        raise NotImplementedError(
            """
            The MdToolMessage class cannot be used with OpenAI function/tools.
            In your ChatAgentConfig, set `use_functions_api=False` and `use_tools=True`
            """
        )

    @classmethod
    def from_markdown(cls: Type[T], markdown_content: str) -> T:
        """
        Parse markdown content and create an instance of the MdToolMessage subclass.
        """
        parsed_data = cls._parse_markdown(markdown_content)
        return cls(**parsed_data)

    @classmethod
    def _parse_markdown(cls, markdown_content: str) -> Dict[str, Any]:
        sections = re.split(r"\n# ", markdown_content)
        parsed_data = {}

        for section in sections:
            if not section.strip():
                continue
            lines = section.strip().split("\n")
            key = lines[0].lower()
            value = cls._parse_section_value(lines[1:])
            parsed_data[key] = value

        return parsed_data

    @classmethod
    def _parse_section_value(cls, lines: List[str]) -> Any:
        if not lines:
            return None

        if lines[0].startswith("- "):
            return [line.strip("- ").strip() for line in lines]

        if "file_path:" in lines[0]:
            return cls._parse_file_contents(lines)

        if len(lines) == 1:
            return cls._parse_primitive(lines[0])

        return "\n".join(lines)

    @staticmethod
    def _parse_file_contents(lines: List[str]) -> FileContents | List[FileContents]:
        file_contents_list = []
        current_file = None

        for line in lines:
            if line.startswith("file_path:"):
                if current_file:
                    file_contents_list.append(FileContents(**current_file))
                current_file = {"file_path": line.split(":", 1)[1].strip()}
            elif current_file:
                current_file["contents"] = (
                    current_file.get("contents", "") + line + "\n"
                )
                current_file["contents"] = current_file["contents"].strip()
                lines = current_file["contents"].split("\n")
                # if first , last line contain backticks, discard them
                if lines and "```" in lines[0]:
                    lines = lines[1:]
                if lines and "```" in lines[-1]:
                    lines = lines[:-1]
                current_file["contents"] = "\n".join(lines)

        if current_file:
            file_contents_list.append(FileContents(**current_file))

        return (
            file_contents_list if len(file_contents_list) > 1 else file_contents_list[0]
        )

    @staticmethod
    def _parse_primitive(value: str) -> Union[str, int, float, bool]:
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
