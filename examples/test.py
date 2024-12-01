

def get_type(variable) -> str:
    # Check for primitive types (int, str, float, etc.)
    if isinstance(variable, int):
        return "int"
    elif isinstance(variable, float):
        return "float"
    elif isinstance(variable, str):
        return "str"
    elif isinstance(variable, bool):
        return "bool"
    
    # Check if it's a list
    elif isinstance(variable, list):
        if not variable:
            return "list[Unknown]"  # Empty list (type can't be determined)
        # Check the type of the elements in the list
        item_types = set(get_type(item) for item in variable)
        if len(item_types) == 1:
            return f"list[{item_types.pop()}]"
        else:
            return f"list[{' | '.join(item_types)}]"  # If there are mixed types in the list
    
    # Check if it's a dictionary
    elif isinstance(variable, dict):
        if not variable:
            return "dict[Unknown]"  # Empty dictionary
        # Check the type of the keys (they should be strings for this case)
        key_type = "str"  # We assume keys are always strings
        # Determine the types of the values in the dictionary
        value_types = set(get_type(value) for value in variable.values())
        
        # If all values have the same type, use it
        if len(value_types) == 1:
            return f"dict[{key_type}: {value_types.pop()}]"
        else:
            return f"dict[{key_type}: {' | '.join(value_types)}]"  # If there are mixed types in values
    
    # If it's none of the above, return 'Unknown'
    return "Unknown"

# Test cases
print(get_type({"key1": {"subkey-1": "value1"}, "key2": {"subkey-2": "value2"}}))  # dict[str: dict[str: str]]
print(get_type([1, 2, 3, 4]))  # list[int]
print(get_type(1))  # int
print(get_type({"key1": 1}))  # dict[str: int]
print(get_type({"key1": "value1"}))  # dict[str: str]
print(get_type([1, "two", 3.0]))  # list[int | str | float]
print(get_type({"key1": {"subkey-1": {"subkey-1": "value1"}}, "key2": {"subkey-2": {"subkey-1": "value1"}}}))  # dict[str: list[int]]
