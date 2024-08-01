"""
This module provide some utilities about Oracle database I/O.

Functions:
    - get_oracle_connection: set connection with a Oracle database.
    - get_dataframe_from_oracle: query OracleDB with given SQL statement.
    - close_connection: close connection from a oracle database.
"""
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

    return df

def close_connection(conn_object: oracledb.Connection):
    """
    Close connection from a Oracle database.

    Args:
        conn_object (oracledb.Connection): Connection object to close
    """
    conn_object.close()