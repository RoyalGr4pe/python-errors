from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_jwt_extended import JWTManager

import logging
import sys
import os

_LOGGER = None
_LIMITER = None
_JWT_MANAGER = None
_REQUIRE_HTTPS = None

def setup_security(
    app=None,
    require_https=True,
    # Logging
    allow_logging=True,
    logger_name="LOGS", 
    log_file="logs", 
    log_level=logging.DEBUG, 
    log_to_console=True,
    delete_logs_on_start=False,
    # JWT Security
    jwt_secret_key=None,
    # Rate Limiting
    rate_limit=False,
    limits=["1 per second"],
    storage_uri = None,
    storage_options = None,
):
    """
    Set up security for the Flask app, including logging, rate limiting, and JWT handling.

    Parameters:
    - app: Flask application instance.
    - logger_name: Name of the logger.
    - log_file: Path to the log file.
    - log_level: Logging level.
    - log_to_console: Whether to log to console.
    - delete_logs_on_start: Whether to delete existing logs on start.
    - jwt_secret_key: Secret key for JWT authentication.
    - rate_limit: Flag which determine whether or not to rate limit the endpoint
    - limits: The value for which to rate limit to
    """

    # Initialize rate limiter
    if rate_limit:
        global _LIMITER
        _LIMITER = Limiter(get_remote_address, app=app, default_limits=limits, storage_uri=storage_uri, storage_options=storage_options)

    # Delete logs on start if required
    if delete_logs_on_start:
        delete_previous_logs_on_start(log_file)

    # Delete logs on start if required
    if require_https:
        global _REQUIRE_HTTPS
        _REQUIRE_HTTPS = require_https

    # Setup logging
    if allow_logging:
        global _LOGGER
        _LOGGER = setup_logger(logger_name, log_file, log_level, log_to_console)

    # Set up JWT manager
    if jwt_secret_key:
        global _JWT_MANAGER
        _JWT_MANAGER = JWTManager(app)
        app.config['JWT_SECRET_KEY'] = jwt_secret_key



def setup_logger(name, filename, log_level, log_to_console):
    """
    Set up a logger with specified configurations.

    Parameters:
    - name (str): Name of the logger.
    - filename (str): File where logs will be saved.
    - log_level (int): Logging level.
    - log_to_console (bool): Log messages to the console.

    Returns:
    - Logger instance.
    """
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)

    # Logger set up
    FORMAT = f"[{name}] | [%(asctime)s] | [%(levelname)s] | %(message)s"
    formatter = logging.Formatter(FORMAT)

    # Create or get logger instance
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if not logger.handlers:
        # FileHandler to log messages to a file
        file_handler = logging.FileHandler(f'logs/{filename}.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Optional StreamHandler to log to console
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger


def get_logger():
    if _LOGGER is None:
        raise Exception("Logger is not initialized. Call `setup_security` first.")
    return _LOGGER


def get_limiter():
    if _LIMITER is None:
        raise Exception("Limiter is not initialized. Call `setup_security` first.")
    return _LIMITER


def get_require_https():
    if _REQUIRE_HTTPS is None:
        raise Exception("_REQUIRE_HTTPS is not initialized. Call `setup_security` first.")
    return _REQUIRE_HTTPS


def delete_previous_logs_on_start(filename):
    try:
        with open(f"logs/{filename}.log", "r+") as file:
            file.seek(0)
            file.truncate()
    except FileNotFoundError:
        return