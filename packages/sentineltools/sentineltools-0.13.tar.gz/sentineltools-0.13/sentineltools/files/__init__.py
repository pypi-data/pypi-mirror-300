from datetime import datetime
import json
import os


def read_file(file_path: str) -> str:
    """
    Reads the content of a text file.

    :param file_path: Path to the file
    :returns: Content of the file as a string
    """
    with open(file_path, "r") as file:
        content = file.read()
    return content


def write_file(file_path: str, content: str) -> None:
    """
    Writes the given content to a text file.

    :param file_path: Path to the file
    :param content: Content to write to the file
    """
    with open(file_path, "w") as file:
        file.write(content)


def read_file_binary(file_path: str) -> bytes:
    """
    Reads the content of a file in binary mode.

    :param file_path: Path to the file
    :returns: Content of the file as bytes
    """
    with open(file_path, "rb") as file:
        content = file.read()
    return content


def write_file_binary(file_path: str, content: bytes) -> None:
    """
    Writes the given content to a file in binary mode.

    :param file_path: Path to the file
    :param content: Content to write to the file as bytes
    """
    with open(file_path, "wb") as file:
        file.write(content)


def read_json(file_path: str) -> dict:
    """
    Reads and parses a JSON file.

    :param file_path: Path to the JSON file
    :returns: Parsed JSON content as a dictionary, or None if parsing fails
    """
    with open(file_path, "r") as file:
        content = file.read()
        try:
            json_content = json.loads(content)
        except:
            json_content = None
    return json_content


def write_json(file_path: str, content: dict, indent: int = 4) -> bool:
    """
    Serializes a dictionary to a JSON file.

    :param file_path: Path to the JSON file
    :param content: Dictionary to serialize and write
    :param indent: Indentation level for the JSON file
    :returns: True if writing was successful, False otherwise
    """
    with open(file_path, "w") as file:
        try:
            json_content = json.dumps(content, indent=indent)
            success = True
        except:
            json_content = "{}"
            success = False
        file.write(json_content)
    return success


def get_file_size(file_path: str) -> int:
    """
    Gets the size of the file in bytes.

    :param file_path: Path to the file
    :returns: Size of the file in bytes
    """
    return os.path.getsize(file_path)


def get_file_creation_date(file_path: str) -> str:
    """
    Gets the creation date of the file.

    :param file_path: Path to the file
    :returns: Creation date of the file as a string in the format YYYY-MM-DD HH:MM:SS
    """
    timestamp = os.path.getctime(file_path)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def get_file_modification_date(file_path: str) -> str:
    """
    Gets the last modification date of the file.

    :param file_path: Path to the file
    :returns: Last modification date of the file as a string in the format YYYY-MM-DD HH:MM:SS
    """
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def is_file_empty(file_path: str) -> bool:
    """
    Checks if the file is empty.

    :param file_path: Path to the file
    :returns: True if the file is empty, False otherwise
    """
    return os.path.getsize(file_path) == 0


def rename_file(old_name: str, new_name: str) -> None:
    """
    Renames a file.

    :param old_name: Current name of the file
    :param new_name: New name for the file
    """
    os.rename(old_name, new_name)


def file_exists(file_path: str) -> bool:
    """
    Checks if the file exists.

    :param file_path: Path to the file
    :returns: True if the file exists, False otherwise
    """
    return os.path.exists(file_path)
