"""
This module provide some utilities to manipulate with pandas dataframe.

Functions:
    - check_df: check if the dataframe has the DataFrame type.
    - check_column: Check if the input columns have a valid type.
    - get_all_duplicate: get all duplicated rows.
    - merge_df: load and merge all xls(xlsm, xlsx) or csv files in a directory.
    - element_count: calculate the element count of an iterable object.
    - convert_str_column_to_datetime: convert a string-formatted DataFrame column into datetime type.
    - generate_dummy: generate dummies from some columns.
    - drop_column: drop some columns from a DataFrame.
"""
import os
import pandas as pd


def check_df(df):
    """
    Check if the input dataframe has a valid type

    Raises
    ------
    ValueError
         If the df is not a DataFrame.

    Parameters
    ----------
    df : DataFrame
        Target dataframe (required)

    Returns
    -------
    None
    """
    if type(df) != pd.core.frame.DataFrame:
        raise TypeError("Type of target df name must be <class 'pandas.core.frame.DataFrame'>, but {}".format(type(df)))


def check_column(columns):
    """
    Check if the input columns have valid type

    Raises
    ------
    ValueError
         If the type of columns is not a str or list.

    Parameters
    ----------
    columns : String or List
        Target column(s) of dataframe (required)

    Returns
    -------
    List
        Columns list
    """
    if type(columns)==str:
        columns = [columns]
    elif type(columns)!=list:
        raise TypeError("Type of target column name must be <class 'str'> or <class 'list'>, but {}".format(type(columns)))

    return columns


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
        DataFrame with the rows that the target columns are duplicated
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
        Merged dataframe
    """
    if type(root_dir) != str:
        raise TypeError("Type of target directory name must be <class 'str'>, but {}".format(type(root_dir)))
    
    return pd.concat(
        [pd.read_csv(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('csv') > -1] +
        [pd.read_excel(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('xls') > -1]
    )


def convert_str_column_to_datetime(df, columns, datetime_format):
    """
        Convert a string-formatted DataFrame column into datetime type.

        Raises
        ------
        TypeError
            If the df is not a dataframe.
            If the type of columns is not a str or list.

        Parameters
        ----------
        df : DataFrame
            Target dataframe (required)

        columns : String or List
            Target column(s) of dataframe (required)

        datetime_format : String
            Datetime format to convert (required)

        Returns
        -------
        DataFrame
            Column-converted dataframe
    """
    check_df(df)
    for column in check_column(columns):
        df.loc[:, column] = pd.to_datetime(df[column], format=datetime_format)

    return df


def generate_dummy(df, columns):
    """
        Generate dummy from some columns.

        Raises
        ------
        TypeError
            If the df is not a dataframe.
            If the type of columns is not a str or list.

        Parameters
        ----------
        df : DataFrame
            Target dataframe (required)

        columns : String or List
            Target column(s) of dataframe to generate (required)

        Returns
        -------
        DataFrame
            Dataframe with dummy columns only
    """
    check_df(df)
    dummy_df = pd.DataFrame()
    for column in check_column(columns):
        dummy_df = pd.concat([dummy_df, pd.get_dummies(df[column], drop_first=True)], axis=1)

    return dummy_df


def drop_column(df, columns):
    """
        Drop some columns from a DataFrame

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
            Target column(s) of DataFrame to drop (required)

        Returns
        -------
        DataFrame
            Column-dropped DataFrame
    """
    check_df(df)
    for column in check_column(columns):
        if column in df.columns:
            df = df.drop(column, axis=1)

    return df
