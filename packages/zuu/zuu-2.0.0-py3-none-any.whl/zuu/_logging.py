import logging
import sys

__all__ = ["basic_debug", "file_debug"]


def basic_debug(level=logging.DEBUG):
    """
    Sets up basic logging configuration with the specified logging level and stream.

    Args:
        level (int, optional): The logging level to set. Defaults to logging.DEBUG.
    """
    logging.basicConfig(level=level, stream=sys.stdout)


def file_debug(file, level=logging.DEBUG):
    """
    Sets up basic logging configuration with the specified logging level and file.

    Args:
        file (str): The path to the file where the log messages will be written.
        level (int, optional): The logging level to set. Defaults to logging.DEBUG.
    """
    logging.basicConfig(level=level, filename=file)
