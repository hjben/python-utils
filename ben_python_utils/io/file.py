"""
This module provide some utilities about file I/O.

Functions:
    - is_hidden: check if a file is hidden or not.
    - extract_directory: extract directory list in a directory.
    - extract_file: extract file list in a directory.
    - expand_relative_path: expand relative path and convert into absolute path.
    - check_file_extension: check extension in a file path.
    - safe_rmtree: remove folder with exception handling.
"""
import os
import shutil


def is_hidden(file_name: str) -> bool:
    """
    Get boolean if a file is hidden or not, with linux based OS.

    Args:
        file_name (str): Target file

    Returns:
        bool: True if a file is hidden, False elsewhere
    """
    return True if file_name.startswith('.') else False

def extract_directory(root_dir: str) -> list:
    """
    Get directory list in a directory.

    Args:
        root_dir (str): Target directory

    Returns:
        list: Extracted directory list
    """
    return [file for file in os.listdir(root_dir) if os.path.isdir(root_dir + file)]

def extract_file(root_dir: str) -> list:
    """
    Get file list in a directory.

    Args:
        root_dir (str): Target directory

    Returns:
        list: Extracted file list
    """
    return [file for file in os.listdir(root_dir) if os.path.isfile(root_dir + file)]

def expand_relative_path(path: str) -> str:
    """
    Expand relative path and convert into absolute path.

    Args:
        path (str): Path to expand

    Returns:
        str: Normalized absolute path
    """
    if path.startswith("~"):
        path = os.path.expanduser(path)

    elif path.startswith(os.path.pardir):
        path = os.path.join(os.path.abspath(os.path.pardir), path[len(os.path.pardir)+1:])

    elif path.startswith(os.path.curdir):
        path = os.path.join(os.path.abspath(os.path.curdir), path[len(os.path.curdir)+1:])
    
    return os.path.normcase(path)

def check_file_extension(file_path: str, ext_list) -> bool:
    """
    Check extension form in a given file path.

    Args:
        file_path (str): File path to check extension
        ext_list (str or Iterable): An extension string or list with only lowercase the target file path must have

    Returns:
        bool: True if the path ends with the given extensions
    """
    if isinstance(ext_list, str):
        ext_list = [ext_list]

    if any([file_path.lower().endswith(f'.{ext}') for ext in ext_list]):
        return True
    else:
        return False

def safe_rmtree(path: str):
    """
    Remove folder with exception handling.

    Args:
        path (str): Target directory
    """
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print(f"Folder not found: {path}")