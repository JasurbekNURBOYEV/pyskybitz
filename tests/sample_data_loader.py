"""Tools to load sample data."""
import os
from pathlib import Path

DIRECTORY = Path(__file__).parent
DATA_DIRECTORY = os.path.join(DIRECTORY, "data")


def load_sample_data(file_name: str, as_bytes: bool = False) -> str:
    """
    Read data file and return its content.

    :param file_name: Name of file.
    :param as_bytes: Whether to return file content as bytes or not.
    :return: Content of file as string.
    """
    path = os.path.join(DATA_DIRECTORY, file_name)
    with open(path, ["r", "rb"][as_bytes]) as file:
        file_content = file.read()
    return file_content
