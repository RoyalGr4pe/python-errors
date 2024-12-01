from .handle_traceback import extract_traceback
from .exceptions.arrays import ArrayTypeError, ArrayNotFound, ArraySizeChange
from .exceptions.dicts import DictTypeError, DictNotFound, DictSizeChange
from .config import get_logger

from os.path import basename
import traceback
import sys



def secure_call(exit_on_error=False, rv=None):
    """
    A decorator to handle exceptions in functions, ensuring that errors are logged properly and
    allowing for graceful error handling. The decorator also provides an option to exit the program
    if an error occurs, or return a fallback value.

    Parameters
    - exit_on_error (bool): If True, the program will exit when an exception is raised in the decorated function. Default is False.
    - rv (Any): The value to return in case of an error. If not specified, the function will return None. Default is None.

    Returns
    - rv (Any): The return value of the decorated function or the specified fallback return value (`rv`) in case of an error.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb = extract_traceback(e)
                if tb:
                    logger.error(tb)
                else:
                    # Fallback logging if traceback is unavailable
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)

                if exit_on_error is True:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)

                return rv

        return wrapper

    return decorator



def secure_array_call(exit_on_error=False, rv=None, secure_size=True, secure_type=True):
    """
    A decorator to ensure that the elements in the array passed to a function are of the same type
    and that the size of the array does not change during execution. It raises custom errors if
    these conditions are violated.

    Note: Using `secure_type` on large arrays can significantly slow down execution, so it should be used
    with caution when dealing with large datasets.

    Parameters
    - exit_on_error (bool): If True, the program will exit upon encountering an error. Default is False.
    - rv (Any): The return value to use in case of an error. Default is None.
    - secure_size (bool): If True, raises an error if the size of the array changes during the execution of the function. Default is True.
    - secure_type (bool): If True, raises an error if any elements in the array are of a different type than the first element. Default is True.

    Returns
    - rv (Any): The return value of the decorated function or the specified fallback return value (`rv`) in case of an error.

    Raises
    - ArrayNotFound: If the first argument passed to the decorated function is not a list.
    - ArrayTypeError: If any element in the array does not match the type of the first element in the array.
    - ArraySizeChange: If the size of the array changes during the execution of the function.
    - Various built-in exceptions (e.g., TypeError, ValueError) are logged but not raised unless `exit_on_error` is True, in which case the program exits.

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()  # Call get_logger() dynamically
            try:
                array = None
                for arg in args:
                    if isinstance(arg, list):
                        array = arg
                        break

                tb = traceback.extract_stack()
                file_path, line_no = tb[-2].filename, tb[-2].lineno 

                # Check if the first argument is a list
                if not (args and isinstance(args[0], list)):
                    raise ArrayNotFound(
                        arg=args[0],
                        func_name=func.__name__,
                        file_path=basename(file_path),
                        line_no=line_no
                    )

                array = args[0]

                # Ensure all elements are of the same type
                if secure_type is True:
                    first_elem_type = type(array[0]) if array else None
                    for index, elem in enumerate(array):
                        if type(elem) != first_elem_type:
                            raise ArrayTypeError(
                                func_name=func.__name__,
                                array_value=elem,
                                array_index=index,
                                expected_type=first_elem_type.__name__,
                                file_path=basename(file_path),
                                line_no=line_no
                            )

                # Store the initial length of the array
                initial_len = len(array)

                # Execute the function
                result = func(*args, **kwargs)

                # Check if the array size changed during function execution
                if (secure_size is True) and (len(array) != initial_len):
                    raise ArraySizeChange(
                        func_name=func.__name__,
                        file_path=basename(file_path),
                        line_no=line_no,
                        initial_len=initial_len,
                        final_len=len(array)
                    )

                return result
            
            except ArraySizeChange as e:
                logger.error(e)

            except ArrayNotFound as e:
                logger.error(e)
            
            except ArrayTypeError as e:
                logger.error(e)

            except Exception as e:
                # Extract traceback details
                tb = extract_traceback(e)

                if tb:
                    logger.error(tb)
                else:
                    # Fallback logging if traceback is unavailable
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)

            finally:
                if exit_on_error is True:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)

                return rv

        return wrapper

    return decorator



def secure_dict_call(exit_on_error=False, rv=None, secure_size=False, secure_types=False, secure_key_type=False, secure_value_type=False):
    """
    A decorator to handle and validate errors for dictionary operations, ensuring the integrity of dictionary operations in terms of key types, value types, size consistency, and handling specific errors like KeyError and ValueError.
    
    Note: Using `secure_types`, `secure_key_type` or `secure_value_type` on large dictionarys can significantly slow down execution, so it should be used with caution when dealing with large datasets.
    
    Parameters
    - exit_on_error (bool): If True, the program will exit when an error occurs. Default is False.
    - rv (Any): The return value to be used when an error occurs. Default is None.
    - secure_size (bool): If True, ensures that the number of keys in the dictionary does not change during the execution of the decorated function.
    - secure_types (bool): If True, validates that the types of the keys and values are consistent throughout the dictionary. This can be further customized using `secure_key_type` and `secure_value_type`.
    - secure_key_type (bool): If True, ensures that all keys in the dictionary are of the same type.
    - secure_value_type (bool): If True, ensures that all values in the dictionary are of the same type.

    Returns
    - rv (Any): The return value of the decorated function, or the specified fallback return value in case of an error.
    
    Raises
    - DictNotFound: If the function arguments do not contain a dictionary.
    - DictTypeError: If the dictionary has keys or values of mixed types.
    - DictSizeChange: If the dictionary's size changes during the function execution.
    - Various built-in exceptions (e.g., KeyError, TypeError, ValueError) are logged but not raised unless `exit_on_error` is True, in which case the program exits.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            
            try:
                dictionary = None
                for arg in args:
                    if isinstance(arg, dict):
                        dictionary = arg
                        break

                tb = traceback.extract_stack()
                file_path, line_no = tb[-2].filename, tb[-2].lineno
                
                # Check if the any of the arguments are dicts
                if dictionary is None:
                    raise DictNotFound(
                        arg=args[0],
                        func_name=func.__name__,
                        file_path=basename(file_path),
                        line_no=line_no
                    )

                # Store the initial length of the array
                initial_len = len(dictionary.keys())

                # Proceed with the function execution
                result = func(*args, **kwargs)

                if secure_types is True:
                    secure_key_type, secure_value_type = True, True

                # Ensure all elements are of the same type
                if (secure_key_type is True) or (secure_value_type is True):
                    key_type = None
                    value_type = None

                    for key, value in dictionary.items():
                        if key_type is None or value_type is None:
                            key_type, value_type = type(key), type(value)
                            continue

                        if (secure_key_type is True) and (type(key) != key_type):
                            secure_key = True
                            secure_value = False
                            expected_type = key_type.__name__

                        elif (secure_value_type is True) and (type(value) != value_type):
                            secure_key = False
                            secure_value = True
                            expected_type = value_type.__name__

                        raise DictTypeError(
                            func_name=func.__name__,
                            key=key,
                            value=value,
                            expected_type=expected_type,
                            file_path=basename(file_path),
                            line_no=line_no,
                            secure_key=secure_key,
                            secure_value=secure_value
                        )

                # Check if the array size changed during function execution
                if (secure_size is True) and (len(dictionary.keys()) != initial_len):
                    raise DictSizeChange(
                        func_name=func.__name__,
                        file_path=basename(file_path),
                        line_no=line_no,
                        initial_len=initial_len,
                        final_len=len(dictionary.keys())
                    )

                return result
            
            except KeyError as e:
                # Catch KeyError specifically
                tb = extract_traceback(e)
                logger.error(tb)
                
                if exit_on_error:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)
                
                return rv  # Return the fallback value

            except TypeError as e:
                # Handle TypeError
                tb = extract_traceback(e)
                logger.error(tb)

                if exit_on_error:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)

                return rv

            except ValueError as e:
                # Handle ValueError
                tb = extract_traceback(e)
                logger.error(tb)

                if exit_on_error:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)

                return rv
            
            except DictSizeChange as e:
                logger.error(e)
            
            except DictTypeError as e:
                logger.error(e)

            except Exception as e:
                # Extract traceback details
                tb = extract_traceback(e)
                print(e)

                if tb:
                    logger.error(tb)
                else:
                    # Fallback logging if traceback is unavailable
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            
            finally:
                if exit_on_error:
                    logger.error("Exiting program due to error.")
                    sys.exit(1)

                return rv

        return wrapper
    
    return decorator