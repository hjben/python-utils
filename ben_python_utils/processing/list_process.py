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