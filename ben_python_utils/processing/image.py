"""
This module provide some utilities to handle an image format.

Functions:
    - extract_dcm_meta: extract given meta information from a dicom file.
    - dcm_to_png: convert a dicom format file to a png image.
"""
import cv2
import pydicom
import SimpleITK as sitk

from PIL import Image
from .basic import check_type_list_element

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
    if not check_type_list_element(meta_list, str) or not check_type_list_element(additional_meta_list, str):
        raise TypeError("The all element types of (additional_)meta_list variable must be <class 'str'>")
    
    try:
        dcm = pydicom.dcmread(dcm_path, force=True)
        try:
            meta_dict = {meta.strip(): dcm[meta.strip()].value for meta in meta_list}
        except KeyError:
            return None

        if additional_meta_list is not None and type(additional_meta_list)==list:
            for additional_meta in additional_meta_list:
                additional_meta = additional_meta.strip()
                try:
                    meta_dict[additional_meta] = dcm[additional_meta].value
                except KeyError:
                    meta_dict[additional_meta] = None
    except (RuntimeError, pydicom.errors.InvaliddicomError):
        return None

    return meta_dict

def dcm_to_png(input_path: str, output_path: str):
    """
        Convert a dicom image to png and save it.
        Some preprocessing logics could be added in this function.

        Parameters
        ----------
        input_path : String
            Dicom file path to convert (required)

        input_path : String
            PNG file path to save (required)

        Returns
        -------
        None
    """
    try:
        sitk_img = sitk.GetArrayFromImage(sitk.ReadImage(input_path, imageIO='GDCMImageIO'))
    except RuntimeError:
        print(f"File can't be read: {input_path}")
        return None

    if len(sitk_img.shape)==4:
        sitk_img = sitk_img[:, :, :, 0]

    pixel_array = sitk_img[0, :, :]

    ### could add any preprocessing procedures below
    # 

    png_img = Image.fromarray(pixel_array)
    png_img.save(output_path)
