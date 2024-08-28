"""
This module provide some utilities about Oracle database I/O.

Functions:
    - get_oracle_connection: set connection with a Oracle database.
    - get_dataframe_from_database: query database with given SQL statement.
    - set_data_to_oracle: insert or update data to OracleDB with given SQL statement.
    - close_connection: close connection from a oracle database.
"""
import oracledb
import pymysql
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

def get_mysql_connection(mysql_info: dict) -> pymysql.Connection:
    if not check_type_dict_value(mysql_info, str):
        return None
    
    return pymysql.connect(host=mysql_info['IP'], port=mysql_info['PORT'], user=mysql_info['USER'], password=mysql_info['PASSWORD'], db=mysql_info['DATABASE'], charset='utf8', cursorclass=pymysql.cursors.DictCursor)

def get_dataframe_from_database(sql: str, conn) -> pd.DataFrame:
    """
    Querys database with given SQL statement and returns data with pd.DataFrame form.

    Args:
        sql (str): SQL statement to query
        conn (oracleDB.Connection or pymysql.Connection): A connection object of DB

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
    Update or insert data to OracleDB with given SQL statement.

    Args:
        sql (str): SQL statement to update or insert
        conn (oracledb.Connection): OracleDB connection object
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.execute('commit')

    cursor.close()

def set_data_to_mysql(sql:str, conn: pymysql.Connection):
    """
    Update or insert data to MySQL with given SQL statement.

    Args:
        sql (str): SQL statement to update or insert
        conn (pymysql.Connection): MySQL connection object
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    cursor.close()

def close_connection(conn_object):
    """
    Close connection from a database.

    Args:
        conn_object (oracledb.Connection or pymysql.Connection): Connection object to close
    """
    conn_object.close()
