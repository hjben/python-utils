"""
This module include some utilities about OS resources.

Functions:
    - cpu_check: check the CPU usage.
    - memory_check: check the memory usage.
"""
import os
import psutil


def cpu_check():
    """
    Check the CPU usage.
    Prints the number of CPU core and general CPU usage percent.
    """
    # show CPU core count
    print(f"# of cores: {psutil.cpu_count(logical=False)}")

    # general CPU usage
    print(f"CPU_usage_percent: {psutil.cpu_percent()}%")


def memory_check():
    """
    Check the memory usage.
    Prints general RAM usage percent and current RAM usage as KB.
    """
    # general RAM usage
    print(f"memory_usage_percent: {dict(psutil.virtual_memory()._asdict())['percent']}%")

    # current process RAM usage: current_process_memory_usage_as_KB
    print(f"Current memory KB   : {psutil.Process(os.getpid()).memory_info()[0] / 2. ** 20: 9.3f} KB")
