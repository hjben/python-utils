import os
import pandas as pd


def get_all_duplicate(df, column_list):
    """
    Get all duplicated rows.
    Extract all rows that the return value of 'DataFrame.duplicated' is true.

    Raises
    ------
    ValueError
        If the input DataFrame is empty.

    Parameters
    ----------
    df : DataFrame
        Base dataframe (required)
    column_list : List
        Target column to extract duplicates (required)

    Returns
    -------
    DataFrame
        DataFrame with the rows that the target columns are duplicated.
    """
    if not df:
        raise ValueError('DataFrame is empty')

    return df[df.duplicated(column_list) | df.duplicated(column_list, keep='last')]


def merge_df(root_dir):
    """
    Load and merge all xls(xlsm, xlsx) or csv files in a directory.
    Folders in the directory will be ignored.
    
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
    DataFrame
        Merged DataFrame
    """
    if type(root_dir) != str:
        raise TypeError("Type of target directory name must be <class 'str'>, but {}".format(type(root_dir)))
    
    return pd.concat(
        [pd.read_csv(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('csv') > -1] +
        [pd.read_excel(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('xls') > -1]
    )


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


def convert_str_columns_to_datetime(df, columns, datetime_format):
    """
        Convert a str-formatted DataFrame column to datetime type

        Raises
        ------
        TypeError
            If the df is not a DataFrame.
            If the type of columns is not a str or list.

        Parameters
        ----------
        df : DataFrame
            Target DataFrame (required)

        columns : String or List
            Target column(s) of DataFrame (required)

        datetime_format : String
            Datetime format to convert (required)

        Returns
        -------
        DataFrame
            Column-converted DataFrame
    """
    if type(df) != pd.core.frame.DataFrame:
        raise TypeError("Type of target df name must be <class 'pandas.core.frame.DataFrame'>, but {}".format(type(df)))

    if type(columns) == str:
        columns = [columns]
    elif type(columns) != list:
        raise TypeError("Type of target column name must be <class 'str'> or <class 'list'>, but {}".format(type(df)))

    for column in columns:
        df.loc[:, column] = pd.to_datetime(df[column], format=datetime_format)

    return df
