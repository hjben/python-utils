"""
This module provide some utilities to handle an image format.

Functions:
    - draw_rectangle_box: Add a rectangle box in a image.
    - extract_dcm_meta: extract given meta information from a dicom file.
    - xray_normalize: add normalizing to a xray(grayscale) image.
    - dcm_to_png: convert a dicom format file to a png image.
"""
import cv2
import pydicom
import SimpleITK as sitk

import numpy as np

from PIL import Image
from .basic import check_type_list_element

def draw_rectangle_box(img: np.ndarray, xmin: int, ymin: int, xmax: int, ymax: int, color=(0, 0, 255), thickness=2, comment_text=None) -> np.ndarray:
    """
        Add a rectangle box and comment text in a image.

        Parameters
        ----------
        img : np.ndarray
            Image array to add (required)

        xmin, ymin, xmax, ymax : int
            2-dimentional coordinate values of two spot, minimum and maximum of rectangle (required)

        color : tuple
            The color of rectangle and text by BGR tuple form (required)

        thickness : int
            The line thickness of the rectangle (required)

        comment_text : str
            A comment string added to the rectangle with same color

        Returns
        -------
        np.ndarray
            Image array with rectangle
    """
    img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness)
    if comment_text is not None:
        img = cv2.putText(img, str(comment_text), (xmin, ymin), cv2.FONT_ITALIC, 1, color, 2)
    
    return img

def extract_dcm_meta(dcm_path: str, meta_list: list, additional_meta_list=None) -> dict:
    """
        Load a dicom image and extract given meta information.

        Raises
        ------
        ValueError
            If meta_list or additional_meta_list have non-string type element

        Parameters
        ----------
        dcm_path : String
            Dicom file path to extract meta information (required)

        meta_list : List
            metadata key list to extract, not allowing None value (required)

        additional_meta_list : List
            additaion metadata key list to extract, allowing None value

        Returns
        -------
        Dictionary
            A key-value set of dicom meta
    """
    if not check_type_list_element(meta_list, str):
        raise TypeError("The all element types of meta_list variable must be <class 'str'>")
    
    try:
        dcm = pydicom.dcmread(dcm_path, force=True)
        try:
            meta_dict = {meta.strip(): dcm[meta.strip()].value for meta in meta_list}
        except KeyError:
            return None

        if isinstance(additional_meta_list, list) and not check_type_list_element(additional_meta_list, str):
            for additional_meta in additional_meta_list:
                additional_meta = additional_meta.strip()
                try:
                    meta_dict[additional_meta] = dcm[additional_meta].value
                except KeyError:
                    meta_dict[additional_meta] = None
    except (RuntimeError, pydicom.errors.InvaliddicomError):
        return None

    return meta_dict

def xray_normalize(img: np.ndarray) -> np.ndarray:
    """
        Apply normalizing process to a xray(grayscale) image.

        Parameters
        ----------
        img : np.ndarray
            image array to normalize (required)

        Returns
        -------
        np.ndarray
            Normalized image array
    """
    img = np.clip(img, 0, np.percentile(img, 99))
    img -= img.min()
    img /= (img.max() - img.min())
    img *= 255
    img = img.astype(np.uint8)

    return img

def dcm_to_png(dcm_path: str, png_path: str):
    """
        Convert a dicom image to png and save it.
        Some preprocessing logics could be added in this function.

        Parameters
        ----------
        dcm_path : String
            Dicom file path to convert (required)

        png_path : String
            PNG file path to save (required)

        Returns
        -------
        None
    """
    try:
        sitk_img = sitk.GetArrayFromImage(sitk.ReadImage(dcm_path, imageIO='GDCMImageIO'))
    except RuntimeError:
        print(f"File can't be read: {dcm_path}")
        return None

    if len(sitk_img.shape)==4:
        sitk_img = sitk_img[:, :, :, 0]

    pixel_array = sitk_img[0, :, :]

    ### could add any preprocessing procedures below
    # pixel_array = xray_normalize(pixel_array)

    png_img = Image.fromarray(pixel_array)
    png_img.save(png_path)

