import logging
import sys
import os

_LOGGER = None

def setup_errors(
    logger_name="LOGS", 
    log_file="logs", 
    log_level=logging.DEBUG, 
    log_to_console=True,
    delete_logs_on_start=False
):
    
    if delete_logs_on_start is True:
        delete_previous_logs_on_start(log_file)

    global _LOGGER
    _LOGGER = setup_logger(logger_name, log_file, log_level, log_to_console)


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
    """
    Retrieve the global logger instance.

    Returns:
    - Logger instance or raises an exception if not initialized.
    """
    if _LOGGER is None:
        raise Exception("Logger is not initialized. Call `setup_errors` first.")
    return _LOGGER


def delete_previous_logs_on_start(filename):
    try:
        with open(f"logs/{filename}.log", "r+") as file:
            file.seek(0)
            file.truncate()
    except FileNotFoundError:
        return