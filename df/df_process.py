import os
import pandas as pd


def get_all_duplicated(df, column_list):
    return df[df.duplicated(column_list) | df.duplicated(column_list, keep='last')]


def merge_df(root_dir):
    return pd.concat(
        [pd.read_csv(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('csv') > -1] +
        [pd.read_excel(root_dir + file) for file in os.listdir(root_dir) if file.split('.')[-1].find('xls') > -1]
    )
