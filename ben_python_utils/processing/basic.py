"""
This module provide some utilities to manipulate with basic data-structures of python.

Functions:
    - check_type_dict_value: check the values' type of a dictionary.
    - check_type_list_element: check the elements' type of a list.
    - convert_type_list_element: convert type of all elements.
    - convert_string_to_timedelta: convert a string into timedelta object.
    - get_split_index: provide even-split indexes for a list-like object.
    - filter_duplicated_word: remove duplicated words in a string.
    - element_count: calculate the element count of an iterable object.
"""
import copy
import datetime


def check_type_dict_value(check_dict: dict, check_type: type, dict_keys=None) -> bool:
    """
    Check type of dictionary values.

    Args:
        check_dict (dict): A dictionary object to check
        check_type (type): Target type to check
        dict_keys (list or hashable, optional): Dictionary key to check. If not given, all keys will be used in the target dictionary. Defaults to None.

    Returns:
        bool: False If any value of dictionary is not matches to the given type
    """
    if dict_keys is None:
        target_key = check_dict.keys()
    elif not isinstance(dict_keys, list):
        target_key = [dict_keys]
    else:
        target_key = dict_keys
    
    for key in target_key:
        if not isinstance(check_dict[key], check_type):
            print("Type of target values must be {}, but some of value has {}".format(check_type, type(check_dict[key])))
            return False
    
    return True
        
def check_type_list_element(check_list: list, check_type: type, index_list=None) -> bool:
    """
    Check type of a list elements.

    Args:
        check_list (list): a list object to check
        check_type (type): Target type to check
        index_list (list or int, optional): Target index list or number to check. Defaults to None.

    Raises:
        ValueError: If the index_list has any invalid index to check_list

    Returns:
        bool: False If any value of list is not matches to the given type
    """
    if index_list is None:
        idx_list = range(len(check_list))
    elif isinstance(index_list, int):
        idx_list = [index_list]
    else:
        idx_list = index_list

    check_idx_list = [idx for idx in index_list if idx >= len(index_list)]
    if len(check_idx_list) > 0:
        raise ValueError(f'Invalid index found in index_list: {str(check_idx_list)}')

    for idx in idx_list:
        if not isinstance(check_list[idx], check_type):
            print("Type of target list elements must be {}, but some of element has {}".format(check_type, type(check_list[idx])))
            return False
        
    return True
        
def convert_type_list_element(target_list: list, convert_type: type) -> bool:
    """
    Convert type of all list elements to given type.

    Args:
        target_list (list): A list object to convert
        convert_type (type): Target type to convert

    Returns:
        bool: False If any value of list is not matches to the given type
    """
    converted_list = copy.deepcopy(target_list)
    for i, element in enumerate(target_list):
        if not isinstance(element, convert_type):
            converted_list[i] = convert_type(element)

    return converted_list

def convert_string_to_timedelta(string: str) -> datetime.timedelta:
    """
    Convert a string into timedelta object.

    Args:
        string (str): a string representation of timedelta

    Raises:
        ValueError: If the input string is not a valid timedelta string

    Returns:
        datetime.timedelta: Converted timedelta object
    """
    # get days
    tmp = string.split('.')
    if len(tmp)==2:
        days = int(tmp[0])
        tmp = tmp[1]
    elif len(tmp)==1:
        days = 0
        tmp = tmp[0]
    else:
        raise ValueError('{} is not a valid timedelta string'.format(string))

    # get total seconds
    tmp = tmp.split(':')
    if len(tmp) != 3:
        raise ValueError('{} is not a valid timedelta string'.format(string))
    total_sec = int(tmp[2]) + int(tmp[1]) * 60 + int(tmp[0]) * 3600

    return datetime.timedelta(days, total_sec)

def get_split_index(data, split_n: int) -> list:
    """
    Get even-split indexes for a list-like object.

    Args:
        data (list-like): Target Data to split
        split_n (int): The number of split

    Returns:
        list: Index list to split the data
    """
    if isinstance(data, dict):
        return [int(len(list(data.keys())) * (i + 1) / split_n) for i in range(split_n - 1)]
    else:
        return [int(len(data) * (i + 1) / split_n) for i in range(split_n - 1)]

def filter_duplicated_word(text: str, sep=' ', reverse=False) -> str:
    """
    Remove duplicated words in a string.

    Args:
        text (str): Target string to remove duplicates
        sep (str, optional): Word seperator. Defaults to ' '.
        reverse (bool, optional): Decide the direction to removing duplicate words, True if remove barkward and False forward. Defaults to False.

    Returns:
        str: String with unique words
    """
    if reverse:
        tmp_list = text.split(sep)[::-1]
        for word in tmp_list:
            word_cnt = tmp_list.count(word)
            if word_cnt > 1:
                for i in range(word_cnt-1):
                    tmp_list.pop(tmp_list.index(word))
                    
        return sep.join(tmp_list[::-1])
    else:
        return sep.join(list(set(text.split(sep))))

def element_count(data) -> dict:
    """
    Calculate the element count of an iterable object.

    Args:
        data (Iterable): Target data to count element

    Raises:
        TypeError: If the data is not an iterable object

    Returns:
        dict: A dicationary with key as an element and value as the count of them
    """
    if not hasattr(data, '__iter__'):
        raise TypeError("{} is not iterable".format(type(data)))
    
    cnt_dict = dict()
    for element in data:
        if element in cnt_dict.keys():
            cnt_dict[element] += 1
        else:
            cnt_dict[element] = 1
        
    return cnt_dict
