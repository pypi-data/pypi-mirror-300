from datetime import datetime

from parse import compile


class PersonFormatter:
    # Define the grammar/template as a class attribute
    GRAMMAR = """
Name: {name}
Age: {age:d}
Birthday: {birthday}
Hobbies: {hobbies}
"""

    @classmethod
    def parse(cls, string):
        parser = compile(cls.GRAMMAR)
        result = parser.parse(string)
        if result:
            return {
                "name": result["name"],
                "age": result["age"],
                "birthday": datetime.strptime(result["birthday"], "%Y-%m-%d").date(),
                "hobbies": [hobby.strip() for hobby in result["hobbies"].split(",")],
            }
        return None

    @classmethod
    def format(cls, data):
        hobbies_str = ", ".join(data["hobbies"])
        return cls.GRAMMAR.format(
            name=data["name"],
            age=data["age"],
            birthday=data["birthday"].strftime("%Y-%m-%d"),
            hobbies=hobbies_str,
        )


# Example usage
if __name__ == "__main__":
    # Parsing
    input_string = """
Name: John Doe
Age: 30
Birthday: 1993-05-15
Hobbies: reading, swimming, coding
"""
    parsed_data = PersonFormatter.parse(input_string)
    print("Parsed data:", parsed_data)

    # Formatting
    person_data = {
        "name": "Jane Smith",
        "age": 25,
        "birthday": datetime(1998, 8, 22).date(),
        "hobbies": ["painting", "yoga", "traveling"],
    }
    formatted_string = PersonFormatter.format(person_data)
    print("\nFormatted string:")
    print(formatted_string)

    # Demonstrating bidirectional conversion
    print("\nBidirectional conversion:")
    original_string = """
Name: Alice Johnson
Age: 35
Birthday: 1988-12-01
Hobbies: gardening, photography, cooking
"""
    print("Original:")
    print(original_string)
    parsed = PersonFormatter.parse(original_string)
    print("Parsed:", parsed)
    reformatted = PersonFormatter.format(parsed)
    print("Reformatted:")
    print(reformatted)
