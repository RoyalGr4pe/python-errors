from .handle_traceback import extract_traceback
from .exceptions import ArrayTypeError, ArrayNotFound, ArraySizeChange
from .config import get_logger

from os.path import basename
import traceback
import sys


def secure_call(exit_on_error=False, rv=None):
    """
    A decorator to handle exceptions in functions.

    Parameters
    - exit_on_error (bool): Exit on error if True.
    - rv (Any): Return value if an error occurs.

    Returns
    - Decorated function.
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
    A decorator to ensure that the array elements have the same type and
    that the size of the array does not change during execution.
    Note: secure_type should only be used on small arrays as this could significantly slow down execution on large arrays.

    Parameters
    - exit_on_error (bool): Exit on error if True.
    - rv (Any): Return value if an error occurs.
    - secure_size (bool): Error out if size of array changes during execution.
    - secure_type (bool): Error if any elements in the array do not match the first element.

    Returns
    - Decorated function.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()  # Call get_logger() dynamically
            try:
                tb = traceback.extract_stack()
                file_path, line_no = tb[-2].filename, tb[-2].lineno 
                print(args[0])
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
                print(e)
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

