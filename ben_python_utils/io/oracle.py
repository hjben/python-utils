import oracledb
import pandas as pd

from file import check_dict_value_type

def get_oracle_connection(param_dict):
    """
        Set connection for oracle database.

        Parameters
        ----------
        param_dict : Dictionary
            Parameter dictionary for oracle database (required)
            Keys to be included: user, password, ip, port, service and Values must be given by string variable
            
            e.g.
            {'user': 'user', 'password': 'password', 'ip': '127.0.0.1', 'port': '3306', service: 'service'}

        Returns
        -------
        oracledb.connect
            OracleDB connection object
    """
    for name, value in param_dict.items():
        if type(param_dict[name]) != str:
            raise TypeError("Type of {} must be <class 'str'>, but {}".format(name, type(value)))
    
    return oracledb.connect(user=param_dict['user'], password=param_dict['password'], dsn=f"{param_dict['ip']}:{param_dict['port']}/{param_dict['service']}")

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