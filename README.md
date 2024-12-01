# Python Errors

**Python Errors** is a Python library designed to handle and manage exceptions effectively, ensuring that critical errors in your code are caught, logged, and handled in a structured way. It provides decorators to help you capture errors in your functions, log them properly, and control the flow of execution.

## Features
- **Structured Error Handling**: Log detailed error information including traceback, function name, and line number.
- **Customizable Error Responses**: Choose whether to return fallback values or exit the program on error.
- **Flexible Decorators**: Use decorators that cater to different data structures (lists, dictionaries, etc.) and their specific errors.
  
## Installation

You can install **Python Errors** using `pip`:

```bash
pip install python-errors
```

## Usage
To use the decorators in this library, simply import them and apply them to the functions you want to protect. You can customize the behavior of each decorator using parameters.

### Decorators



#### `@secure_call(exit_on_error=False, rv=None)`

This decorator catches any general exceptions in the wrapped function. You can choose to return a fallback value or exit the program if an error occurs.

#### Parameters:
- `exit_on_error (bool)`: If `True`, the program will exit upon encountering an error.
- `rv (Any)`: The value to return if an error occurs. If not specified, the function will return `None`.

#### Example:
```python
from python_errors import secure_call

@secure_call(exit_on_error=True, rv="Fallback Value")
def risky_function():
    # Some code that may raise an exception
    print(1 / 0)  # This will raise ZeroDivisionError

risky_function()  # Program will exit due to the exception, or return 'Fallback Value'
```



#### `@secure_array_call(exit_on_error=False, rv=None, secure_size=True, secure_type=True)`

This decorator ensures that the elements of the array are of the same type and that the array size does not change during execution. It’s particularly useful when working with lists.

#### Parameters:
- `exit_on_error (bool)`: If `True`, exit the program if an error occurs.
- `rv (Any)`: The value to return if an error occurs.
- `secure_size (bool)`: Ensures the size of the array doesn’t change during execution.
- `secure_type (bool)`: Ensures all elements in the array are of the same type.

#### Example:
```python
from python_errors import secure_array_call

@secure_array_call(exit_on_error=True, rv="Fallback Value", secure_size=True, secure_type=True)
def process_array(arr):
    # Some operation on the array
    arr.append(5)  # This will cause an error if secure_size=True and the array size changes

process_array([1, 2, 3])  # Will exit the program if the array size changes
```



#### `@secure_dict_call(exit_on_error=False, rv=None, secure_size=False, secure_types=False, secure_key_type=False, secure_value_type=False)`

This decorator ensures that dictionary operations are secure by validating various conditions, such as the size of the dictionary, the types of its keys and values, and whether the dictionary is modified during execution.

#### Parameters:
- `exit_on_error (bool)`: If `True`, exit the program if an error occurs.
- `rv (Any)`: The value to return if an error occurs.
- `secure_size (bool)`: Ensures the size of the dictionary doesn’t change during execution.
- `secure_types (bool)`: Ensures that the types of the keys and values are consistent.
- `secure_key_type (bool)`: Ensures the keys in the dictionary are of the same type.
- `secure_value_type (bool)`: Ensures the values in the dictionary are of the same type.

#### Example:
```python
from python_errors import secure_dict_call

@secure_dict_call(exit_on_error=True, rv="Fallback Value", secure_size=True, secure_types=True, secure_key_type=True, secure_value_type=True)
def process_dict(d):
    # Some operation on the dictionary
    d["new_key"] = 10  # This will raise an error if the dictionary size changes and secure_size=True

process_dict({"item-1": 1, "item-2": 2, "item-3": 3})  # Will exit the program if the dictionary size changes
```