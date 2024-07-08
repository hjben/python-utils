import os


def is_hidden(file_name):
    """
    Get boolean if a file (or a directory) is hidden or not, with linux based OS.

    Raises
    ------
    TypeError
        If the input data is not a string.

    Parameters
    ----------
    file_name : String
        Target file (required)

    Returns
    -------
    Boolean
        True if a file is hidden, False elsewhere
    """
    if type(file_name) != str:
        raise TypeError("Type of file name must be <class 'str'>, but {}".format(type(file_name)))

    return True if file_name.startswith('.') else False


def extract_directory(root_dir):
    """
    Get directory list in a directory.

    Raises
    ------
    TypeError
        If the input data is not a string.

    Parameters
    ----------
    root_dir : String
        Target directory (required)

    Returns
    -------
    List
        Extracted directory list
    """
    if type(root_dir) != str:
        raise TypeError("Type of target directory name must be <class 'str'>, but {}".format(type(root_dir)))

    return [file for file in os.listdir(root_dir) if os.path.isdir(root_dir + file)]


def extract_file(root_dir):
    """
    Get file list in a directory.

    Raises
    ------
    TypeError
        If the input data is not a string.

    Parameters
    ----------
    root_dir : String
        Target directory (required)

    Returns
    -------
    List
        Extracted file list
    """
    if type(root_dir) != str:
        raise TypeError("Type of target directory name must be <class 'str'>, but {}".format(type(root_dir)))

    return [file for file in os.listdir(root_dir) if os.path.isfile(root_dir + file)]
