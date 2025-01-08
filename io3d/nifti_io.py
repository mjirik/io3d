import nibabel as nib
from pathlib import Path
import numpy as np
from typing import Tuple, Union
from . import image
from loguru import logger


def read_nifti(filename: Union[Path, str]) -> Tuple[np.ndarray, dict]:
    img = nib.load(filename)
    data3d = np.asarray(img.dataobj)
    voxelsize_mm = img.header.get_zooms()
    metadata = {
        "voxelsize_mm": voxelsize_mm,
        "affine": img.affine,
        "orientation_axcodes": nib.orientations.aff2axcodes(img.affine),
    }
    return data3d, metadata


def write_nifti(datap: Union[dict, image.DataPlus], filename: Union[str, Path]):
    """
    Write dict with image data into nifti file. There should be fallowing keys in the dict:
    * 'data3d'
    * 'affine' or 'voxelsize_mm' and 'orientation_axcodes'
    :param datap:
    :return:
    """
    if type(datap) == dict:
        datap = image.DataPlus(datap)
    datap.transform_orientation("RAS")
    affine = None
    if "affine" in datap:
        affine = datap.pop("affine")
    else:
        if "voxelsize_mm" in datap:
            diag = np.ones([4])
            diag[:3] = datap.voxelsize_mm[:]
            affine = np.diag(diag)
        if "voxelsize_mm" in datap and "orientation_axcodes" in datap:
            input_axcodes = datap["orientation_axcodes"]
            ornt_my = nib.orientations.axcodes2ornt(input_axcodes)

    data3d = datap.pop("data3d")


    new_image = nib.Nifti1Image(data3d, affine=affine)
    new_image.header.set_zooms(datap.voxelsize_mm)
    nib.save(new_image, filename)
