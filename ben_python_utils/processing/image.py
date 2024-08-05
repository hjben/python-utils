"""
This module provide some utilities to handle an image format.

Functions:
    - draw_rectangle_box: Add a rectangle box in a image.
    - extract_dcm_meta: extract given meta information from a dicom file.
    - xray_normalize: add normalizing to a xray(grayscale) image.
    - dcm_to_img: convert a dicom format file to a image-format file.
    - show_dcm_image: Describe plot to show a dcm image.
"""
import os
import cv2
import pydicom
import SimpleITK as sitk

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from .basic import check_type_list_element
from ..io.file import check_file_extension

def draw_rectangle_box(img: np.ndarray, xmin: int, ymin: int, xmax: int, ymax: int, color=(0, 0, 255), thickness=2, comment_text=None) -> np.ndarray:
    """
    Add a rectangle box and comment text in a image.

    Args:
        img (np.ndarray): Image array to add
        xmin, ymin, xmax, ymax (int): 2-dimentional coordinate values of two spot, minimum and maximum of rectangle
        color (tuple, optional): The color of rectangle and text by BGR tuple form. Defaults to (0, 0, 255).
        thickness (int, optional): The line thickness of the rectangle. Defaults to 2.
        comment_text (str, optional): A comment string added to the rectangle with same color. Defaults to None.

    Returns:
        np.ndarray: Image array with rectangle
    """
    img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness)
    if comment_text is not None:
        img = cv2.putText(img, str(comment_text), (xmin, ymin), cv2.FONT_ITALIC, 1, color, 2)
    
    return img

def extract_dcm_meta(dcm_path: str, meta_list: list, additional_meta_list=None) -> dict:
    """
    Load a dicom image and extract given meta information.

    Args:
        dcm_path (str): Dicom file path to extract meta information
        meta_list (list): Metadata key list to extract, not allowing None value
        additional_meta_list (list, optional): Additional metadata key list to extract, allowing None value. Defaults to None.

    Raises:
        TypeError: If meta_list or additional_meta_list have non-string type element

    Returns:
        dict: A key-value set of dicom meta
    """
    if not check_type_list_element(meta_list, str):
        raise TypeError("The all element types of meta_list variable must be <class 'str'>")
    
    if not check_file_extension(dcm_path, ['dcm', 'dicom']):
        raise ValueError("dcm_path has wrong extension of dicom format")
    
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

    Args:
        img (np.ndarray): image array to normalize

    Returns:
        np.ndarray: normalized image array
        
    """
    img = np.clip(img, 0, np.percentile(img, 99))
    img -= img.min()
    img /= (img.max() - img.min())
    img *= 255
    img = img.astype(np.uint8)

    return img

def dcm_to_img(dcm_path: str, img_path: str, target_ext='png', series_idx_range=(None, None)):
    """
    Convert a dicom to image-format file and save it.
    Some preprocessing logics could be added in this function.

    Args:
        dcm_path (str): Dicom file path to convert
        img_path (str): Target image file path to save
        target_ext (str, optional): Image extension to save. Defaults to 'png'.
        series_idx_range (tuple, optional): The range of target series index to convert. Defaults to (None, None).

    Raises:
        ValueError: If dcm_path or img_path have wrong extension format
    """
    if not check_file_extension(dcm_path, ['dcm', 'dicom']):
        raise ValueError("dcm_path has wrong extension of dicom format")
    
    try:
        sitk_img = sitk.GetArrayFromImage(sitk.ReadImage(dcm_path, imageIO='GDCMImageIO'))
    except RuntimeError:
        print(f"DCM file could't be read: {dcm_path}")
        return None

    if len(sitk_img.shape)==4:
        sitk_img = sitk_img[:, :, :, 0]
    
    if series_idx_range[0] is None:
        series_idx_range = (1, series_idx_range[1])
    if series_idx_range[1] is None:
        series_idx_range = (series_idx_range[0], sitk_img.shape[0])

    ext_split = img_path.split(os.path.sep)[-1].split('.')
    if len(ext_split)==1:
        img_name = ext_split[0]
        ext_to_save = target_ext
    else:
        if ext_split[0]=='': # hidden data path
            img_name = '.'.join(ext_split[:2])
            if len(ext_split)==2:
                ext_to_save = target_ext
            else:
                ext_to_save = ext_split[-1]
        else:
            img_name = ext_split[0]
            ext_to_save = ext_split[-1]

    if not check_file_extension('.'.join([img_name, ext_to_save]), target_ext):
        raise ValueError(f"img_path has wrong extension of image format: {ext_to_save}")
    
    for series in range(series_idx_range[0]-1, series_idx_range[1]):
        pixel_array = sitk_img[series, :, :]

        ### could add any preprocessing procedures below
        # pixel_array = xray_normalize(pixel_array)

        Image.fromarray(pixel_array).save(os.path.join(os.path.sep.join(img_path.split(os.path.sep)[:-1]), img_name + f"_{series}.{ext_to_save}"))

def show_dcm_img(dcm_path: str, series_idx_range=(None, None), fig_size=None, num_col=1):
    """
    Describe plot to show a dcm image.

    Args:
        dcm_path (str): Target dicom file path to graph
        series_idx_range (tuple, optional): The range of target series index to show. Defaults to (None, None).
        fig_size (tuple, optional): Ths size of total graph, which is a composed tuple of (weight, height). Defaults to None.
        num_col (int, optional): The number of columns in the graph. Defaults to 1.

    Raises:
        ValueError: The second element of series_idx_range is smaller than first one
        TypeError: If fig_size is not a tuple type
    """
    sitk_img = sitk.GetArrayFromImage(sitk.ReadImage(dcm_path))

    print("[Descriptions]")
    for meta, value in extract_dcm_meta(dcm_path, ['PatientID', 'Modality', 'Studydate'], ['StudyDescription', 'SeriesDescription', 'BodyPartExamined']).items():
        print(f"{meta}: {value}")
    
    if series_idx_range[0] is None:
        series_idx_range = (1, series_idx_range[1])
    if series_idx_range[1] is None:
        series_idx_range = (series_idx_range[0], sitk_img.shape[0])
    
    total_plot_cnt = series_idx_range[1] - series_idx_range[0]
    if total_plot_cnt < 0:
        raise ValueError("The first element of series_idx_range must be larger than second one")
    
    num_row = total_plot_cnt // num_col + 1
    if fig_size is not None:
        if not isinstance(fig_size, tuple):
            raise TypeError("fig_size must be a tuple type")
            
        fig, axes = plt.subplots(num_row, num_col, figsize=fig_size)
    else:
        fig, axes = plt.subplots(num_row, num_col, figsize=(6*num_col, 6*num_row))

    for i, series in enumerate(range(series_idx_range[0]-1, series_idx_range[1])):
        pixel_array = sitk_img[series, :, :]
        
        row_ = i//num_col
        col_ = i%num_col
        
        axes[row_][col_].imshow(xray_normalize(pixel_array), 'gray')
        axes[row_][col_].set_title(f"[Image {series + 1}]")