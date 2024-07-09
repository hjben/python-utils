import datetime


def check_dict_value_type(check_dict, check_type, dict_keys=None):
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

def convert_string_to_timedelta(string):
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
    if not string:
        raise ValueError('{} is not a valid timedelta string'.format(string))

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


def get_split_index(data, split_n):
    """
        Get even-split indexes for a list-like object.

        Raises
        ------
        TypeError
            If the split_n is not an int.

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
    if type(split_n) != int:
        raise TypeError("Type of target directory name must be <class 'int'>, but {}".format(type(split_n)))

    if isinstance(data, dict):
        return [int(len(list(data.keys())) * (i + 1) / split_n) for i in range(split_n - 1)]
    else:
        return [int(len(data) * (i + 1) / split_n) for i in range(split_n - 1)]