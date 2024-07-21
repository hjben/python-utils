import os
import time
import requests
import pandas as pd
from pyhive import hive

from ..processing.basic_process import check_dict_value_type

def get_hdfs_url(hadoop_info, hdfs_dir_path: str, op: str):
    """
        Create URL of HDFS api form with composing informations.

        Parameters
        ----------
        hadoop_info : Dictionary
            Parameter dictionary for hadoop information (required)
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g.
            {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path : String
            Data path to upload (required)

        op : String
            Target operation to HDFS (required)

            e.g.
            CREATE, LISTSTATUS, OPEN, ...

        Returns
        -------
        String
            Composed string with URL form
    """
    return f"http://{hadoop_info['IP']}:{hadoop_info['PORT']}/webhdfs/v1{hdfs_dir_path}?op={op}&user.name={hadoop_info['USER']}&doas={hadoop_info['USER']}"

def upload_hdfs_file(hadoop_info: dict, hdfs_dir_path: str, upload_data):
    """
        Upload a file to HDFS system.

        Parameters
        ----------
        hadoop_info : Dictionary
            Parameter dictionary for hadoop information (required)
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g.
            {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path : String
            Data path to upload (required)

        upload_data : Object
            Target data to upload (required)

        Returns
        -------
        String
            Response string
    """
    check_dict_value_type(hadoop_info, str)
    url = get_hdfs_url(hdfs_dir_path + upload_data, 'CREATE') + "&overwrite=true"
    response = requests.put(url, data=open(upload_data, 'rb').read(), auth=(hadoop_info['USER'], hadoop_info['PASSWORD']), headers={'content-type': 'application/octet-stream'})

    try:
        print(response.json())
    except:
        print(response.text)

    return response.text

def download_hdfs_file(hadoop_info: dict, hdfs_dir_path: str, local_dir_path: str):
    """
        Download files from HDFS system.

        Parameters
        ----------
        hadoop_info : Dictionary
            Parameter dictionary for hadoop information (required)
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g.
            {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path : String
            Target HDFS data path to download (required)

        local_dir_path : String
            Local data path to save (required)

        Returns
        -------
        None
    """
    # create target folder
    target_file_path = os.path.join(local_dir_path, hdfs_dir_path.split('/')[-1])
    os.makedirs(target_file_path, exist_ok=True)

    with requests.Session() as s:
        s.auth = (hadoop_info['USER'], hadoop_info['PW'])

        # file search
        for file in s.get(get_hdfs_url(hdfs_dir_path, 'LISTSTATUS')).json()['FileStatuses']['FileStatus']:
            save_path = os.path.join(target_file_path, file['pathSuffix'])

            if file['type']!='FILE':
                download_hdfs_file(hadoop_info, f"{hdfs_dir_path}/{file['pathSuffix']}", local_dir_path)

            if os.path.exists(save_path):
                continue

            try:
                # file save to local
                file_save_path = f"{hdfs_dir_path}/{file['pathSuffix']}"
                with open(file_save_path, 'wb') as f:
                    f.write(s.get(get_hdfs_url(file_save_path, "OPEN")).content)

                print(f"Downloaded: {file_save_path}")
                time.sleep(1.0)
            except Exception as e:
                print(e)

def get_hive_connection(hive_info: dict, hive_config: dict):
    """
        Set connection for hive database.

        Parameters
        ----------
        hive_info : Dictionary
            Parameter dictionary for hive database information (required)
            Keys to be included: user, PASSWORD, IP, port and Values must be given by string variable
            
            e.g.
            {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '10000'}

        hive_config : Dictionary
            Configuration dictionary of hive database (required)

            e.g.
            {"tez.am.resource.memory.mb": "8192",
            "tez.am.java.opts": "-Xmx6400m",
            "hive.tez.container.size": "8192",
            "hive.tez.java.opts": "-Xmx6400m",
            "tez.runtime.io.sort.mb": "3200",
            "tez.task.launch.cmd.opts": "-Xmx6400m",
            "mapreduce.reduce.shuffle.memory.limit.percent": "0.15",
            "mapreduce.input.fileinputformat.split.minsize": "256000000",
            "hive.auto.convert.join.noconditionaltask.size": "600",
            "tez.am.max.allowed.time-sec.for-read-error": "600",
            "hive.execution.engine": "tez"}

        Returns
        -------
        pyhive.hive.Connection
            Hive connection object
    """
    check_dict_value_type(hive_info, str)
    check_dict_value_type(hive_config, str)
        
    return hive.Connection(host=hive_info['IP'], port=hive_info['PORT'], username=hive_info['USER'], password=hive_info['PASSWORD'], auth='LDAP', configuration=hive_config)

def get_dataframe_from_hive(hive_ql: str, conn):
    """
    Querys OracleDB with given SQL statement and returns data with pd.DataFrame form.

    Parameters
    ----------
    hive_ql : String
        HiveQL statement to query (required)

    conn: hive.Connection
        Hive connection object
        
    Returns:
    -------
    pd.DataFrame
        Result of query
    """
    return pd.read_sql(hive_ql, conn)
