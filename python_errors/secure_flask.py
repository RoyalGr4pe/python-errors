from .config import get_logger, get_limiter, get_require_https
from .utils.calculate_type import get_type

from flask_jwt_extended import jwt_required
from functools import wraps
from flask import jsonify, request, redirect


def secure_endpoint(
    method, 
    required_type=None, 
    default_response=None, 
    rate_limit="1 per second", 
    require_jwt=False,
    https_required=get_require_https()
):
    """
    A generic decorator to validate input data types and rate-limit for GET and POST endpoints.

    Parameters
    - method (str): The HTTP method ('GET' or 'POST').
    - required_type (str): Expected type of input data.
    - default_response (tuple): Default response if an exception occurs.
    - rate_limit (list): Custom rate limit for the endpoint.
    - jwt_required (bool): Whether JWT authentication is required for this endpoint.
    """
    def decorator(func):
        limiter = get_limiter()

        # Apply rate limit(s) if specified
        if limiter:
            func = limiter.limit(rate_limit)(func)

        # If JWT authentication is required, apply the jwt_required decorator to the function
        if require_jwt:
            func = jwt_required()(func)

        # Check if the request is secure (HTTPS)
        if https_required:
            if not request.is_secure:
                # If not secure, redirect to the HTTPS version of the URL
                return redirect(request.url.replace("http://", "https://"))
            
        @wraps(func)
        def wrapper(*args, **kwargs):
            if method.upper() == "GET":
                return secure_get_endpoint(required_type, default_response)(func)(*args, **kwargs)
            elif method.upper() == "POST":
                return secure_post_endpoint(required_type, default_response)(func)(*args, **kwargs)
            else:
                return jsonify({"error": "Unsupported HTTP method"}), 405

        return wrapper
    return decorator


def secure_get_endpoint(required_type=None, default_response=None):
    """
    A decorator to validate the input data type for GET endpoints.

    Parameters:
    - required_type (str): Expected type of input data.
    - default_response (tuple): Default response if an exception occurs.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            input_data = request.args.to_dict(flat=True)

            # Validate the input type
            if required_type:
                input_type = get_type(input_data)
                if input_type != required_type:
                    return jsonify({"error": "Invalid input data format"}), 400

            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                if default_response:
                    return jsonify(default_response[0]), default_response[1]
                return jsonify({"error": str(e)}), 500

        return wrapper

    return decorator


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

            # Validate that input_data matches the provided required_type
            if required_type:
                # Get the JSON data from the request
                input_data = request.get_json()
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
