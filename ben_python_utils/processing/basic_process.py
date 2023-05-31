import datetime


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