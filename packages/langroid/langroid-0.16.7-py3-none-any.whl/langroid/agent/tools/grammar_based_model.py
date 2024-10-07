from abc import ABC, abstractmethod

from lark import Lark, Token, Tree
from lark.reconstruct import Reconstructor

from langroid.pydantic_v1 import BaseModel


class GrammarBasedModel(BaseModel, ABC):
    _parse_tree: Tree = None  # Store the parse tree
    _parser: Lark = None  # Store the parser instance

    @classmethod
    @abstractmethod
    def get_grammar(cls) -> str:
        """
        Subclasses must implement this method to return their grammar as a string.
        """
        pass

    @classmethod
    def get_token_field_mapping(cls):
        """
        Returns a mapping from token types to model field names. Subclasses can override this
        if their token types and field names differ.
        """
        return {}

    @classmethod
    def parse(cls, text: str):
        """
        Parse the input text using the grammar to create an instance of the model.
        """
        parser = Lark(cls.get_grammar(), parser="lalr", propagate_positions=True)
        tree = parser.parse(text)
        model_instance = cls.from_tree(tree)
        model_instance._parse_tree = tree  # Store the parse tree in the instance
        model_instance._parser = parser  # Store the parser in the instance
        return model_instance

    @classmethod
    def from_tree(cls, tree: Tree):
        """
        Convert a parse tree into a model instance.
        """
        data = cls.tree_to_dict(tree)
        return cls(**data)

    @classmethod
    def tree_to_dict(cls, tree: Tree):
        """
        Recursively convert a parse tree into a dictionary of field values.
        """
        data = {}
        token_field_mapping = cls.get_token_field_mapping()
        for child in tree.children:
            if isinstance(child, Tree):
                data.update(cls.tree_to_dict(child))
            elif isinstance(child, Token):
                token_type = child.type
                field_name = token_field_mapping.get(token_type, token_type.lower())
                data[field_name] = child.value
        return data

    def generate(self) -> str:
        """
        Generate a string representation of the model instance using the grammar.
        """
        if self._parse_tree is None or self._parser is None:
            raise ValueError("Cannot generate text without parsing first.")
        # Update the parse tree with current model data
        self.update_tree_with_model_data(self._parse_tree)
        reconstructor = Reconstructor(self._parser)
        text = reconstructor.reconstruct(self._parse_tree)
        return text

    def update_tree_with_model_data(self, tree: Tree):
        """
        Update the parse tree with the current model data.
        """
        token_field_mapping = self.get_token_field_mapping()
        reverse_mapping = {v: k for k, v in token_field_mapping.items()}
        for idx, child in enumerate(tree.children):
            if isinstance(child, Tree):
                self.update_tree_with_model_data(child)
            elif isinstance(child, Token):
                field_name = token_field_mapping.get(child.type, child.type.lower())
                if hasattr(self, field_name):
                    new_value = getattr(self, field_name)
                    tree.children[idx] = Token(child.type, str(new_value))


# Example subclass
class MyModel(GrammarBasedModel):
    name: str
    age: int

    @classmethod
    def get_grammar(cls):
        return """
            start: "name:" NAME "age:" NUMBER
            %import common.CNAME -> NAME
            %import common.INT -> NUMBER
            %import common.WS
            %ignore WS
            """

    @classmethod
    def get_token_field_mapping(cls):
        return {
            "NAME": "name",
            "NUMBER": "age",
        }


# Usage example
if __name__ == "__main__":
    text = "name: Alice age: 30"
    model = MyModel.parse(text)
    print("Parsed Model:", model)

    # Generate string from the model
    generated_text = model.generate()
    print("Generated Text:", generated_text)

    # Modify the model
    model.age = 31
    model.name = "Bob"

    # Generate updated string
    updated_text = model.generate()
    print("Updated Generated Text:", updated_text)
