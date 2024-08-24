"""
This module provide some utilities about Oracle database I/O.

Functions:
    - get_oracle_connection: set connection with a Oracle database.
    - get_dataframe_from_oracle: query OracleDB with given SQL statement.
    - close_connection: close connection from a oracle database.
"""
import copy
import oracledb
import pandas as pd

from ..processing.basic import check_type_dict_value

def get_oracle_connection(oracle_info: dict) -> oracledb.Connection:
    """
    Set connection with an Oracle database.

    Args:
        oracle_info (dict):
            Parameter dictionary for oracle database
            Keys to be included: USER, PASSWORD, ip, PORT, SERVICE and Values must be given by string variable
            
            e.g. {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '3306', SERVICE: 'service'}

    Returns:
        oracledb.Connection: OracleDB connection object
    """
    if not check_type_dict_value(oracle_info, str):
        return None
    
    return oracledb.connect(user=oracle_info['USER'], password=oracle_info['PASSWORD'], dsn=f"{oracle_info['IP']}:{oracle_info['PORT']}/{oracle_info['SERVICE']}")

def get_dataframe_from_oracle(sql: str, conn: oracledb.Connection) -> pd.DataFrame:
    """
    Querys OracleDB with given SQL statement and returns data with pd.DataFrame form.

    Args:
        sql (str): SQL statement to query
        conn (oracledb.Connection): OracleDB connection object

    Returns:
        pd.DataFrame: Result of the query
    """
    cursor = conn.cursor()
    cursor.execute(sql)

    df = pd.DataFrame(cursor.fetchall())

    if df.shape[0]!=0:
        df.columns = [desc[0] for desc in cursor.description]

    cursor.close()

    return df

def set_data_to_oracle(sql: str, conn: oracledb.Connection):
    """
    Update or insert data to a OracleDB with given SQL statement.

    Args:
        sql (str): SQL statement to update or insert
        conn (oracledb.Connection): OracleDB connection object
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.execute('commit')

    cursor.close()

def close_connection(conn_object: oracledb.Connection):
    """
    Close connection from a Oracle database.

    Args:
        conn_object (oracledb.Connection): Connection object to close
    """
    conn_object.close()

def generate_insert_sql(table_name: str, df: pd.DataFrame, col_list=None) -> str:
    """
    Generate a SQL statement of inserting data from a DataFrame.

    Args:
        table_name (str): A table name to insert data
        df (pd.DataFrame): Target data to insert
        col_list (list, optional): Target column list to insert, which is in the df.columns. Defaults to None.

    Raises:
        ValueError: Some values in col_list not exist in column list of df

    Returns:
        str: Insert SQL string
    """
    if col_list is None:
        col_list = list(df.columns)
    else:
        not_exist_list = [col for col in col_list if col not in list(df.columns)]
        if len(not_exist_list) > 0:
            raise ValueError(f"Some values in col_list not exist in column list of df: {','.join(not_exist_list)}")

    sql_list = list()
    base_sql = f"insert into {table_name} ({','.join(col_list)}) values ("
    for idx in df.index:
        row = df.loc[idx]
        copied_sql = copy.deepcopy(base_sql)
        for i, col in enumerate(col_list):
            if i==len(col_list)-1:
                end_str = ');'
            else:
                end_str = ','

            if isinstance(row[col], str):
                copied_sql += "'" + str(row[col]) + "'" + end_str
            else:
                copied_sql += str(row[col]) + end_str

        sql_list.append(copied_sql)

    return '\n'.join(sql_list)

def generate_update_sql(table_name: str, df: pd.DataFrame, filter_col: str , filter_value, col_list=None) -> str:
    """
    Generate a SQL statement of updating data from a DataFrame.

    Args:
        table_name (str): A table name to update data
        df (pd.DataFrame): Target data to update
        filter_col (str): A column name to filter updating data
        filter_value (Object): A column value to filter updating data
        col_list (list, optional): Target column list to update, which is in the df.columns. Defaults to None.

    Raises:
        ValueError: Some values in col_list or filter_col not exist in column list of df

    Returns:
        str: Update SQL string
    """
    if col_list is None:
        col_list = list(df.columns)
    else:
        not_exist_list = [col for col in col_list if col not in list(df.columns)]
        if len(not_exist_list) > 0:
            raise ValueError(f"Some values in col_list not exist in column list of df: {','.join(not_exist_list)}")

    if filter_col not in col_list:
        raise ValueError("filter_col not exists in column list of df")

    sql_list = list()
    base_sql = f"update {table_name} set "
    df = df.loc[df[filter_col]==filter_value]
    for idx in df.index:
        row = df.loc[idx]
        copied_sql = copy.deepcopy(base_sql)
        for i, col in enumerate(col_list):
            if i==len(col_list)-1:
                end_str = ''
            else:
                end_str = ','

            if isinstance(row[col], str):
                copied_sql += col + "='" + str(row[col]) + "'" + end_str
            else:
                copied_sql += col + "=" + str(row[col]) + end_str

        copied_sql += f' where {filter_col}={filter_value};'
        sql_list.append(copied_sql)    

    return '\n'.join(sql_list)

def add_condition_to_sql(sql: str, filter_col, filter_value) -> str:
    """
    Add where statement to a SQL. All contitions are concatenated by AND

    Args:
        sql (str): Target SQL statement to add where contition
        filter_col (str or list): Column names to filter data
        filter_value (Object): Column values to filter data

    Raises:
        ValueError: The number of element of filter_col and filter_value not matches

    Returns:
        str: SQL statement with where contition added
    """
    if not isinstance(filter_col, list):
        filter_col = [filter_col]
    if not isinstance(filter_value, list):
        filter_value = [filter_value]

    if len(filter_col)!=len(filter_value):
        raise ValueError("The number of element of filter_col and filter_value not matches")
    
    sql +=  " where "
    for i, (col, value) in enumerate(zip(filter_col, filter_value)):
        sql += f"{col}={value}"
        if i!=len(filter_col) - 1:
            sql += " and "
    
    return sql

def generate_select_sql(table_name: str, filter_col=None, filter_value=None, col_list=None) -> str:
    """
    Generate a SQL statement of selecting data. Filtering with key is enabled when both filter_col and filter_value is not None.

    Args:
        table_name (str): A table name to delete data
        filter_col (str or list, optional): Column names to filter selecting data. Defaults to None.
        filter_value (Object, optional): Column values to filter selecting data. Defaults to None.
        col_list (str or list, optional): Target column list to extract. Defaults to None.

    Returns:
        str: Select SQL string
    """
    if col_list is None:
        col_sql = '*'
    else:
        if isinstance(col_list, list):
            col_sql = ','.join(col_list)
        else:
            col_sql = col_list
        
    if filter_col is not None and filter_value is not None:
        return add_condition_to_sql(f"select {col_sql} from {table_name}", filter_col, filter_value)
    else:
        return f"select {col_sql} from {table_name}"
    
def generate_delete_sql(table_name: str, filter_col=None, filter_value=None) -> str:
    """
    Generate a SQL statement of deleting data. Filtering with key is enabled when both filter_col and filter_value is not None.

    Args:
        table_name (str): A table name to delete data
        filter_col (str or list, optional): Column names to filter deleting data. Defaults to None.
        filter_value (Object, optional): Column values to filter deleting data. Defaults to None.

    Returns:
        str: Delete SQL string
    """
    if filter_col is not None and filter_value is not None:
        return add_condition_to_sql(f"delete {table_name}", filter_col, filter_value)
    else:
        return f"delete {table_name}"