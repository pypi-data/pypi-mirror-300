from parse import parse

# Define the format string
format_string = """
name:{:s}
{:d} is the age
lives in {:s}
"""


def parse_person_info(input_string):
    # Remove leading/trailing whitespace and split into lines
    lines = input_string.strip().split("\n")

    # Join the lines with a single newline
    normalized_input = "\n".join(line.strip() for line in lines if line.strip())

    # Parse the normalized input
    result = parse(format_string, normalized_input)

    if result:
        name, age, city = result
        return f"Name: {name.strip()}, Age: {age}, City: {city.strip()}"
    else:
        return "Parsing failed"


# Test cases and assertions
if __name__ == "__main__":
    # Test case 1: Standard format
    input1 = """
    name: Beck
    30 is the age
    lives in Tokyo
    """
    assert (
        parse_person_info(input1) == "Name: Beck, Age: 30, City: Tokyo"
    ), "Test case 1 failed"

    # Test case 2: Extra whitespace
    input2 = """
    name:    Beck    
      30     is    the    age  
    lives    in    Tokyo
    """
    assert (
        parse_person_info(input2) == "Name: Beck, Age: 30, City: Tokyo"
    ), "Test case 2 failed"

    # Test case 3: Extra newlines
    input3 = """
    name:Beck


    30 is the age

    lives in Tokyo
    """
    assert (
        parse_person_info(input3) == "Name: Beck, Age: 30, City: Tokyo"
    ), "Test case 3 failed"

    # Test case 4: Minimal whitespace
    input4 = "name:John\n25 is the age\nlives in NewYork"
    assert (
        parse_person_info(input4) == "Name: John, Age: 25, City: NewYork"
    ), "Test case 4 failed"

    # Test case 5: Different name, age, city
    input5 = """
    name: Alice Johnson
    42 is the age
    lives in San Francisco
    """
    assert (
        parse_person_info(input5) == "Name: Alice Johnson, Age: 42, City: San Francisco"
    ), "Test case 5 failed"

    # Test case 6: Invalid format (should return "Parsing failed")
    input6 = """
    name: Invalid
    not a number is the age
    lives in Nowhere
    """
    assert parse_person_info(input6) == "Parsing failed", "Test case 6 failed"

    print("All tests passed successfully!")
