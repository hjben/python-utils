"""
This module include some utilities about OS resources.

Functions:
    - memory_check: check the memory usage.
"""
import os
import psutil


def memory_check():
    """
        Check the memory usage.
        Prints general RAM usage percent and current RAM usage as KB.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    # general RAM usage
    print(f"memory_usage_percent: {dict(psutil.virtual_memory()._asdict())['percent']}%")

    # current process RAM usage: current_process_memory_usage_as_KB
    print(f"Current memory KB   : {psutil.Process(os.getpid()).memory_info()[0] / 2. ** 20: 9.3f} KB")
