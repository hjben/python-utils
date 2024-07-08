from pyhive import hive

def get_hive_connection(param_dict, hive_config):
    """
        Set connection for hive database.

        Parameters
        ----------
        param_dict : Dictionary
            Parameter dictionary for hive database (required)
            Keys to be included: user, password, ip, port and Values must be given by string variable
            
            e.g.
            {'user': 'user', 'password': 'password', 'ip': '127.0.0.1', 'port': '10000'}

        hive_config : Dictionary
            Configuration dictionary of hive database

        Returns
        -------
        pyhive.hive.Connection
            Hive connection object
    """
    for name, value in param_dict.items():
        if type(param_dict[name]) != str:
            raise TypeError("Type of {} must be <class 'str'>, but {}".format(name, type(value)))
        
    return hive.Connection(host=param_dict['ip'], port=param_dict['port'], username=param_dict['user'], password=param_dict['password'], auth='LDAP', configuration=hive_config)
