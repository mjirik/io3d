#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)

import numpy as np

def get_pixel_array_from_sitk(sitk_image):
    dim = sitk_image

    import SimpleITK as sitk
    if dim.HasMetaDataKey("0028|1052") and dim.HasMetaDataKey("0028|1053"):
        rescale_intercept = dim.GetMetaData("0028|1052")
        rescale_slope = dim.GetMetaData("0028|1053")
        slope, inter = get_slope_and_intercept_from_strings(rescale_slope, rescale_intercept)
    else:
        slope = 1
        inter = 0

    data3d = sitk.GetArrayFromImage(sitk_image)  # + 1024
    data3d = rescale_pixel_array(data3d, slope=slope, inter=inter)

    return data3d

def get_sitk_image_from_ndarray(data3d):
    """
    Prepare SimpleItk Image object and rescale data to unsigned types.

    Simple ITK with version higher than 1.0.0 can not write signed int16. This function check
    the SimpleITK version and use work around with Rescale Intercept and Rescale Slope
    :param data3d:
    :return:
    """

    import SimpleITK as sitk
    rescale_intercept = None
    if sitk.Version.MajorVersion() > 0:
        if data3d.dtype == np.int8:
            rescale_intercept = -2**7
            data3d = (data3d - rescale_intercept).astype(np.uint8)
        elif data3d.dtype == np.int16:
            # simpleitk is not able to store this. It uses only 11 bites
            # rescale_intercept = -2**15
            rescale_intercept = -2**10
            data3d = (data3d - rescale_intercept).astype(np.uint16)
        elif data3d.dtype == np.int32:
            rescale_intercept = -2**31
            data3d = (data3d - rescale_intercept).astype(np.uint16)

    dim = sitk.GetImageFromArray(data3d)
    if sitk.Version.MajorVersion() > 0:
        if rescale_intercept is not None:
            # rescale slope (0028|1053), rescale intercept (0028|1052)
            dim.SetMetaData("0028|1052", str(rescale_intercept))
            dim.SetMetaData("0028|1053", "1")

    return dim

def get_slope_and_intercept_from_strings(rescale_slope, rescale_intercept):
    if type(rescale_slope) is str:
        slope = float(rescale_slope)
    else:
        slope = rescale_slope

    if type(rescale_intercept) is str:
        inter = float(rescale_intercept)
    else:
        inter = rescale_intercept

    return slope, inter

def get_slope_and_intercept_from_pdcm(dcmdata):
    """
    Get scale and intercept from pydicom file object.
    :param dcmdata:
    :return:
    """

    if hasattr(dcmdata, "RescaleSlope") and hasattr(dcmdata, "RescaleIntercept"):
        rescale_slope = dcmdata.RescaleSlope
        rescale_intercept = dcmdata.RescaleIntercept
        slope, inter = get_slope_and_intercept_from_strings(rescale_slope, rescale_intercept)
    else:
        slope = 1
        inter = 0

    return slope, inter

# def get_pixel_array_from_pdcm(data):
#     """
#     Get data2d and rescale
#     :param data: pydicom dcmobj
#     :return: data2d, original_data2d_dtype
#     """
#     from . import dcmtools
#     data2d = data.pixel_array
#     slope, inter = get_slope_and_intercept_from_pdcm(data)
#     # new_data2d = rescale_pixel_array(data2d, slope, inter)
#     return data2d, slope, inter

from .misc import use_economic_dtype as rescale_pixel_array

# def rescale_pixel_array(data2d, slope, inter, dtype=None):
#     from .misc import
#     orig_dtype = data2d.dtype
#     if dtype is None:
#         if orig_dtype is np.uint16 and inter == -2**15:
#             dtype = np.int16
#         elif orig_dtype is np.uint16 and inter < 0:
#             dtype = np.int16
#         elif orig_dtype is np.uint32 and inter < 0:
#             dtype = np.int32
#         else:
#             dtype = orig_dtype
#
#     new_data2d = ((np.float(slope) * data2d) + np.float(inter)).astype(dtype)
#     return new_data2d
