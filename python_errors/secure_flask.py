from .config import get_logger
from .handle_traceback import extract_traceback
from .exceptions.except_flask import EndpointError
from .utils.calculate_type import get_type

from functools import wraps
from flask import jsonify, request


def secure_post_endpoint(required_type=None, default_response=None):
    """
    A decorator to validate the input data type for POST endpoints.
    This checks if the input data is of the expected type, allowing nested structures.

    Parameters:
    - required_type (str): Expected type of input data.
    - default_response (tuple): Default response if an exception occurs.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            # Get the JSON data from the request
            input_data = request.get_json()

            # Validate that input_data matches the provided required_type
            if required_type:
                input_type = get_type(input_data)
                if input_type != required_type:
                    return jsonify({"error": "Invalid input data format"}), 400

            try:
                # Call the original function
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                # Handle exceptions and return the default response if provided
                if default_response:
                    return jsonify(default_response[0]), default_response[1]
                else:
                    return jsonify({"error": str(e)}), 500

        return wrapper
    return decorator