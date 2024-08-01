"""
This module provide some utilities about Hadoop Ecosystem I/O.

Functions:
    - get_hdfs_url: create an URL of HDFS api form.
    - extract_directory: extract directory list in a directory.
    - upload_hdfs_file: upload a file into HDFS system.
    - download_hdfs_file: download files from HDFS system.
    - get_hive_connection: set connection with a Hive database.
    - get_dataframe_from_hive: query Hive DB with given HiveQL statement.
"""
import os
import time
import requests
import pandas as pd
from pyhive import hive

from ..processing.basic import check_type_dict_value

def get_hdfs_url(hadoop_info: dict, hdfs_dir_path: str, op: str) -> str:
    """
    Create URL of HDFS api form with composing informations.

    Args:
        hadoop_info (dict):
            Parameter dictionary for hadoop information
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g. {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path (str): Data path to upload
        op (str):
            Target operation to HDFS 

            e.g. CREATE, LISTSTATUS, OPEN, ...

    Returns:
        str: Composed string with URL form
    """
    return f"http://{hadoop_info['IP']}:{hadoop_info['PORT']}/webhdfs/v1{hdfs_dir_path}?op={op}&user.name={hadoop_info['USER']}&doas={hadoop_info['USER']}"

def upload_hdfs_file(hadoop_info: dict, hdfs_dir_path: str, upload_data: object) -> str:
    """
    Upload a file into HDFS system.

    Args:
        hadoop_info (dict):
            Parameter dictionary for hadoop information 
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g. {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path (str): Data path to upload
        upload_data (object): Target data to upload

    Returns:
        str: Response string
    """
    if not check_type_dict_value(hadoop_info, str):
        return None
    
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

    Args:
        hadoop_info (dict):
            Parameter dictionary for hadoop information
            Keys to be included: USER, PASSWORD, IP, PORT and Values must be given by string variable
            
            e.g. {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '8020'}

        hdfs_dir_path (str): Target HDFS data path to download
        local_dir_path (str): Local data path to save
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

def get_hive_connection(hive_info: dict, hive_config: dict) -> hive.Connection:
    """
    Set connection with a Hive database.

    Args:
        hive_info (dict):
            Parameter dictionary for hive database information
            Keys to be included: user, PASSWORD, IP, port and Values must be given by string variable
            
            e.g. {'USER': 'user', 'PASSWORD': 'password', 'IP': '127.0.0.1', 'PORT': '10000'}

        hive_config (dict):
            Configuration dictionary of hive database

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

    Returns:
        hive.Connection: Hive connection object
    """
    if not check_type_dict_value(hive_info, str) or not check_type_dict_value(hive_config, str):
        return None
    
    return hive.Connection(host=hive_info['IP'], port=hive_info['PORT'], username=hive_info['USER'], password=hive_info['PASSWORD'], auth='LDAP', configuration=hive_config)

def get_dataframe_from_hive(hive_ql: str, conn: hive.Connection) -> pd.DataFrame:
    """
    Querys Hive datadase with given HiveQL statement and returns data with pd.DataFrame form.

    Args:
        hive_ql (str): HiveQL statement to query
        conn (hive.Connection): Hive connection object

    Returns:
        pd.DataFrame: Result of query
    """
    return pd.read_sql(hive_ql, conn)
