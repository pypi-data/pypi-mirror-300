from parse import parse

# Define the parse specification
parse_spec = """
<format>
name{:s}{:>}{}\n
age{:s}{:>}{}\n
</format>
"""


def parse_info(input_string):
    print(f"Input string:\n{input_string}")  # Debug print
    result = parse(parse_spec, input_string, case_sensitive=False)
    print(f"Parse result: {result}")  # Debug print
    if result:
        name = result[1].strip()  # The actual name value is in the second group
        age = result[3].strip()  # The actual age value is in the fourth group
        return name, age
    else:
        return None


if __name__ == "__main__":
    # Test case 1: Standard format
    input_string1 = """
<format>
name      beck
age   30
</format>
"""
    print("\nTest case 1:")
    result1 = parse_info(input_string1)
    print(f"Test 1 result: {result1}")
    assert result1 == (
        "beck",
        "30",
    ), f"Test 1 failed. Expected ('beck', '30'), got {result1}"

    # Additional test cases...

    print("All tests passed successfully!")
