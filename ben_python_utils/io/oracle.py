import oracledb
import pandas as pd

from ..processing.basic_process import check_dict_value_type

def get_oracle_connection(oracle_info: dict):
    """
        Set connection for oracle database.

        Parameters
        ----------
        oracle_info : Dictionary
            Parameter dictionary for oracle database (required)
            Keys to be included: USER, PASSWORD, ip, PORT, SERVICE and Values must be given by string variable
            
            e.g.
            {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '3306', SERVICE: 'service'}

        Returns
        -------
        oracledb.connect
            OracleDB connection object
    """
    check_dict_value_type(oracle_info, str)
    
    return oracledb.connect(user=oracle_info['USER'], password=oracle_info['PASSWORD'], dsn=f"{oracle_info['IP']}:{oracle_info['PORT']}/{oracle_info['SERVICE']}")

def get_dataframe_from_oracle(sql, conn):
        """
        Querys OracleDB with given SQL statement and returns data with pd.DataFrame form.

        Parameters
        ----------
        sql : String
            SQL statement to query (required)

        conn: oracledb.connect
            OracleDB connection object
            
        Returns:
        -------
        pd.DataFrame
            Result of query
        """
        if type(sql) != str:
            raise TypeError("Type of sql statement must be <class 'str'>, but {}".format(type(sql)))

        cursor = conn.cursor()
        cursor.execute(sql)

        df = pd.DataFrame(cursor.fetchall())

        if df.shape[0]!=0:
            df.columns = [desc[0] for desc in cursor.description]

        return df

def close_connection(conn_object):
    """
        Close connection for oracle database.

        Parameters
        ----------
        conn_object : Object
            Connection object to close (required)

        Returns
        -------
        None
    """
    conn_object.close()