import os
import pandas as pd


def get_all_duplicate(df, column_list):
    """
    Get all duplicated rows.
    Extract all rows that the return value of 'DataFrame.duplicated' is true.

    Raises
    ------
    ValueError
        If the DataFrame is empty.

    Parameters
    ----------
    df : DataFrame
        Base dataframe (required)
    column_list: List
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
