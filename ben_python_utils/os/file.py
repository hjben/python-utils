import os

def create_folder_if_not(path):
    """
        Create folder with path if the path not exists.

        Parameters
        ----------
        path : String
            Target path to check and create

        Returns
        -------
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)