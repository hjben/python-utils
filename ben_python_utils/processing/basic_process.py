"""
This module provide some utilities to manipulate with basic data-structures of python.

Functions:
    - check_dict_value_type: check the values' type of a dictionary.
    - convert_string_to_timedelta: convert a string into timedelta object.
    - get_split_index: provide even-split indexes for a list-like object.
    - filter_duplicated_word: remove duplicated words in a string.
    - element_count: calculate the element count of an iterable object.
"""
import datetime


def check_dict_value_type(check_dict: dict, check_type, dict_keys=None):
    """
        Check type of dictionary value.

        Raises
        ------
        TypeError
            If the value of dictionary is not same with the given type.

        Parameters
        ----------
        check_dict: Dictionary
            Dictionary object to check (required)

        check_type: Type object
            Target type to check (required)

        key: Object
            Dictionary key to check
            If not given, all keys will be used in the target dictionary

        Returns
        -------
        None
    """
    if not dict_keys:
        dict_keys = check_dict.keys()

    for key in dict_keys:
        if type(check_dict[key]) != check_type:
            raise TypeError("Type of {} must be <class {}>, but {}".format(key, type, type(check_dict[key])))

def convert_string_to_timedelta(string: str):
    """
        Convert string to time delta.

        Raises
        ------
        TypeError
            If the input is not a valid timedelta string.

        Parameters
        ----------
        string : String
            String representation of time delta (required)

        Returns
        -------
        datetime.timedelta
            Converted timedelta object
    """
    # get days
    tmp = string.split('.')
    if len(tmp) == 2:
        days = int(tmp[0])
        tmp = tmp[1]
    elif len(tmp) == 1:
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

def get_split_index(data, split_n: int):
    """
        Get even-split indexes for a list-like object.

        Parameters
        ----------
        data : List-like objects
            Target Data (required)

        split_n : Integer
            The number of split (required)

        Returns
        -------
        List
            Index list to split data
    """
    if isinstance(data, dict):
        return [int(len(list(data.keys())) * (i + 1) / split_n) for i in range(split_n - 1)]
    else:
        return [int(len(data) * (i + 1) / split_n) for i in range(split_n - 1)]

def filter_duplicated_word(text: str, sep=' ', reverse=False):
    """
        Remove duplicated words in a string.

        Parameters
        ----------
        text : String
            Target string to remove duplicates (required)

        sep : String
            Word seperator. Basic value is ' ' (blank)

        reverse : Boolean
            Decide the direction to removing duplicate words
            True if remove barkward and False if forward

        Returns
        -------
        String
            String with unique words
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

def element_count(data):
    """
        Calculate the element count of an iterable object.

        Raises
        ------
        TypeError
            If the data is not a iterable object.

        Parameters
        ----------
        data : Iterable object
            Target data to count element (required)

        Returns
        -------
        Dictionary
            A dicationary with key as an element and value as the count of them
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
