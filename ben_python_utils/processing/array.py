"""
This module provide some utilities to manipulate with numpy array.

Functions:
    - describe_array: print out summary informations.
"""
import numpy as np

def describe_array(arr:np.ndarray, name=None):
    """
    Describe summary informations of an array.

    Args:
        arr (np.ndarray): Target array to describe
        name (str, optional): Array name. Defaults to None.
    """
    if name is not None:
        print(f"========{name}========")

    print(f"Type: {type(arr)}")
    print(f"Shape: {arr.shape}")
    print(f"Min: {arr.min()}")
    print(f"Max: {arr.max()}")
    print(f"Values: \n{arr}")