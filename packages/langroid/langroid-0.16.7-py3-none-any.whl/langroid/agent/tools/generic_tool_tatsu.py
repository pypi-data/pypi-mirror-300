from abc import abstractmethod
from typing import List

import tatsu

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
    def tool_grammar(cls) -> str:
        """Define the grammar for the `tool` rule"""
        pass

    @classmethod
    def grammar(cls) -> str:
        """
        Full grammar, including templates for rendering.
        """
        base_grammar = """
            @@grammar :: CombinedGrammar
            @@whitespace :: /[ \\t]+/
            @@nameguard :: False

            start
                =
                "<spec>" ws?
                request:word ws?
                tool
                ws? "</spec>"
            {:
                "<spec> " {{request}} {{tool}} " </spec>"
            :}
                ;

            ws = /[\\s]+/ ;

            word = /[^\\s<>/]+/ ;
        """
        full_grammar = base_grammar + "\n" + cls.tool_grammar()
        return full_grammar

    @classmethod
    def parse(cls, s: str):
        """
        Parses a string `s` using the grammar and returns an instance of the subclass.
        """
        # Build the parser using the provided grammar with model generation
        parser = tatsu.compile(cls.grammar(), asmodel=True)

        # Parse the input string to get a model object
        model = parser.parse(s)

        # Convert the model to a dict, filtering only the expected fields
        data = {k: getattr(model, k) for k in cls.__fields__ if hasattr(model, k)}

        # Create an instance of the subclass with the parsed data
        model_instance = cls(**data)
        return model_instance

    def format(self) -> str:
        """
        Generates a string representation of the instance based on the grammar.
        """
        # Build the parser using the provided grammar with model generation
        parser = tatsu.compile(self.grammar(), asmodel=True)

        # Create a model instance
        model_class = parser.model()
        model = model_class()

        # Set attributes from the instance, excluding fields not in the grammar
        for field in self.__fields__:
            if field == "purpose":
                continue  # Exclude 'purpose' from rendering
            setattr(model, field, getattr(self, field))

        # Render the model back to text using the grammar's templates
        generated_string = model.render()
        return generated_string

    @classmethod
    def instructions(cls) -> str:
        """
        Generates instructions for formatting an instance, including placeholders
        and an example output with placeholders.
        """

        def generate_placeholders(field, prefix=""):
            placeholders = {}
            if hasattr(field.type_, "__fields__"):
                # Nested model
                for sub_field_name, sub_field in field.type_.__fields__.items():
                    placeholders.update(
                        generate_placeholders(
                            sub_field, prefix=f"{prefix}{field.name}."
                        )
                    )
            elif isinstance(field.type_, type) and issubclass(field.type_, list):
                # List field
                placeholders[field.name] = (
                    f"[<{field.name}_item1>,<{field.name}_item2>,...]"
                )
            else:
                placeholders[field.name] = f"<{prefix}{field.name}>"
            return placeholders

        # Generate placeholders for all fields
        placeholders = {}
        for field_name, field in cls.__fields__.items():
            placeholders.update(generate_placeholders(field))

        # Build the preamble
        preamble_lines = ["Placeholders for formatting:"]
        for field_name, placeholder in placeholders.items():
            field_type = cls.__fields__[field_name].type_.__name__
            preamble_lines.append(
                f"- `{placeholder}`: placeholder for `{field_name}` field (type: `{field_type}`)"
            )
        preamble = "\n".join(preamble_lines)

        # Create a placeholder instance
        placeholder_values = {}
        for field_name in cls.__fields__:
            placeholder_values[field_name] = placeholders[field_name]
        placeholder_instance = cls(**placeholder_values)

        # Generate an example output with placeholders
        parser = tatsu.compile(cls.grammar())
        ast = placeholder_instance.to_ast()
        # Use the placeholders in the AST
        for key, value in ast.items():
            ast[key] = placeholders.get(key, value)
        example_output = parser.render(ast)

        # Combine preamble and example output
        instructions = f"{preamble}\n\nExample format:\n\n{example_output}"
        return instructions

    @classmethod
    def from_ast(cls, ast):
        """
        Converts an AST into a model instance.
        """
        # Since TatSu produces dicts, we can convert the AST dict to the model
        return cls(**ast)

    def to_ast(self):
        """
        Converts the model instance into an AST (dict).
        """
        # Since TatSu expects dicts for rendering, we can use the model's dict
        return self.dict()

    @classmethod
    def from_string(cls, input_string: str) -> "CodeFileTool":
        """Parse a string into a CodeFileTool object, using the TEMPLATE."""
        parsed_data = cls.parse(input_string)
        if parsed_data:
            return cls(**parsed_data)
        raise ValueError("Invalid input string format")

    def to_string(self) -> str:
        """Convert a CodeFileTool object to a string, using the TEMPLATE."""
        return self.format()

    @classmethod
    def find_candidates(cls, s: str) -> List[str]:
        """
        Finds all substrings in `s` that start with start_marker and end with end_marker.
        """
        start = "<spec>"  # TODO get from TOOL_BEGIN, TOOL_END
        end = "</spec>"
        candidates = []
        start_len = len(start)
        end_len = len(end)
        index = 0
        while index < len(s):
            start_index = s.find(start, index)
            if start_index == -1:
                break
            end_index = s.find(end, start_index + start_len)
            if end_index == -1:
                break
            candidate = s[start_index : end_index + end_len]
            # Attempt to parse the candidate to ensure it's valid
            try:
                cls.parse(candidate)
                candidates.append(candidate)
            except tatsu.exceptions.ParseException:
                # Ignore invalid candidates
                pass
            index = end_index + end_len
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


if __name__ == "__main__":
    # Example subclass

    class MyTool(GenericTool):
        request: str = "my_tool"
        purpose: str = "do something"
        value: int

        @classmethod
        def tool_grammar(cls) -> str:
            return """
                tool = "value:" value:number
                {:
                    "value:" {{value}}
                :}
                    ;
    
                number = /\\d+/
                ;
            """

    my_tool = MyTool(value=42)

    # Generate the string from the instance using the grammar
    generated_string = my_tool.format()
    print("Formatted string:", generated_string)

    # Parse the string back into an instance using the grammar
    parsed_instance = MyTool.parse(generated_string)
    print("Parsed instance:", parsed_instance)
    print("Parsed value:", parsed_instance.value)

    # Extended example
    class ExtendedModel(GrammarBasedModel):
        request: str
        user_id: int
        action: str
        details: str

        @classmethod
        def rest_grammar(cls) -> str:
            return """
                rest = user_id:number ws action:word ws details:text ;

                number = /\d+/ ;
                text = /.+/ ;
            """

    input_string_ext = "<spec> user_update 42 delete Account deletion</spec>"
    extended_instance = ExtendedModel.parse(input_string_ext)
    print("Parsed extended instance:", extended_instance)

    generated_string_ext = extended_instance.generate()
    print("Generated extended string:", generated_string_ext)
