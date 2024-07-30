"""
This module provide some utilities about file I/O.

Functions:
    - is_hidden: check if a file is hidden or not.
    - extract_directory: extract directory list in a directory.
    - extract_file: extract file list in a directory.
    - expand_relative_path: expand relative path and convert into absolute path.
    - safe_rmtree: remove folder with exception handling.
"""
import os
import shutil


def is_hidden(file_name: str) -> bool:
    """
    Get boolean if a file is hidden or not, with linux based OS.

    Parameters
    ----------
    file_name : String
        Target file (required)

    Returns
    -------
    Boolean
        True if a file is hidden, False elsewhere
    """
    return True if file_name.startswith('.') else False

def extract_directory(root_dir: str) -> list:
    """
    Get directory list in a directory.

    Parameters
    ----------
    root_dir : String
        Target directory (required)

    Returns
    -------
    List
        Extracted directory list
    """
    return [file for file in os.listdir(root_dir) if os.path.isdir(root_dir + file)]

def extract_file(root_dir: str) -> list:
    """
    Get file list in a directory.

    Parameters
    ----------
    root_dir : String
        Target directory (required)

    Returns
    -------
    List
        Extracted file list
    """
    return [file for file in os.listdir(root_dir) if os.path.isfile(root_dir + file)]

def expand_relative_path(path: str) -> str:
    """
    Expand relative path and convert into absolute path.

    Parameters
    ----------
    path : String
        Path to expand (required)

    Returns
    -------
    String
        Normalized absolute path
    """
    if path.startswith("~"):
        path = os.path.expanduser(path)

    elif path.startswith(os.path.pardir):
        path = os.path.join(os.path.abspath(os.path.pardir), path[len(os.path.pardir)+1:])

    elif path.startswith(os.path.curdir):
        path = os.path.join(os.path.abspath(os.path.curdir), path[len(os.path.curdir)+1:])
    
    return os.path.normcase(path)

def safe_rmtree(path: str):
    """
    Remove folder with exception handling.

    Parameters
    ----------
    path : String
        Target directory (required)

    Returns
    -------
    None
    """
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print(f"Folder not found: {path}")