"""
This module provide some utilities to manipulate with pandas dataframe.

Functions:
    - check_df: check if the dataframe has the DataFrame type.
    - check_column: Check if the input columns have a valid type.
    - get_all_duplicate: get all duplicated rows.
    - load_dir: load and merge all xls(xlsm, xlsx) or csv files in a directory.
    - element_count: calculate the element count of an iterable object.
    - convert_str_column_to_datetime: convert a string-formatted DataFrame column into datetime type.
    - generate_dummy: generate dummies from some columns.
    - drop_column: drop some columns from a DataFrame.
"""
import os
import pandas as pd

def check_df(df: pd.DataFrame):
    """
    Check if the input dataframe has a valid type.

    Args:
        df (pd.DataFrame): Target dataframe to check

    Raises:
        TypeError: If the df is not a DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Type of target df name must be <class 'pandas.core.frame.DataFrame'>, but {}".format(type(df)))


def check_column(columns) -> list:
    """
    Check if the input columns have string or list type.

    Args:
        columns (str or list): Target column(s) of a DataFrame

    Raises:
        TypeError: If the type of columns is not a str or list

    Returns:
        list: A list of columns
    """
    if isinstance(columns, str):
        columns = [columns]
    elif not isinstance(columns, list):
        raise TypeError("Type of target column name must be <class 'str'> or <class 'list'>, but {}".format(type(columns)))

    return columns


def get_all_duplicate(df: pd.DataFrame, column_list: list) -> pd.DataFrame:
    """
    Get all duplicated rows.
    Extract all rows that the return value of 'DataFrame.duplicated' is true.

    Args:
        df (pd.DataFrame): Target DataFrame
        column_list (list): Target column(s) in the DataFrame to extract duplicates

    Raises:
        ValueError: If the input DataFrame is empty

    Returns:
        pd.DataFrame: DataFrame with the rows that the target columns are duplicated
    """
    if len(df)==0:
        raise ValueError('DataFrame is empty')

    return df[df.duplicated(column_list) | df.duplicated(column_list, keep='last')]


def load_dir(root_dir: str) -> pd.DataFrame:
    """
    Load and merge all xls(xlsm, xlsx) or csv files in a directory.
    Folders in the directory will be ignored.

    Args:
        root_dir (str): Target directory to load

    Returns:
        pd.DataFrame: A merged DataFrame
    """
    return pd.concat(
        [pd.read_csv(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('csv') > -1] +
        [pd.read_excel(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('xls') > -1]
    )


def convert_str_column_to_datetime(df: pd.DataFrame, columns, datetime_format: str) -> pd.DataFrame:
    """
    Convert a string-formatted DataFrame column into datetime type.

    Args:
        df (pd.DataFrame): Target dataframe
        columns (list or str): Target column(s) in the DataFrame to convert
        datetime_format (str): Datetime format string to convert

    Returns:
        pd.DataFrame: A DataFrame with column-converted
    """
    check_df(df)
    for column in check_column(columns):
        df.loc[:, column] = pd.to_datetime(df[column], format=datetime_format)

    return df


def generate_dummy(df: pd.DataFrame, columns) -> pd.DataFrame:
    """
    Generate dummy from some columns.

    Args:
        df (pd.DataFrame): Target DataFrame
        columns (list or str): Target column(s) in the DataFrame to generate

    Returns:
        pd.DataFrame: A DataFrame with dummy columns only
    """
    check_df(df)
    dummy_df = pd.DataFrame()
    for column in check_column(columns):
        dummy_df = pd.concat([dummy_df, pd.get_dummies(df[column], drop_first=True)], axis=1)

    return dummy_df


def drop_column(df: pd.DataFrame, columns) -> pd.DataFrame:
    """
    Drop some columns from a DataFrame.

    Args:
        df (pd.DataFrame): Target DataFrame
        columns (list or str): Target column(s) of DataFrame to drop

    Returns:
        pd.DataFrame: A DataFrame with some column-dropped
    """
    check_df(df)
    for column in check_column(columns):
        if column in df.columns:
            df = df.drop(column, axis=1)

    return df
