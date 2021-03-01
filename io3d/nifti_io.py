import nibabel as nib
from pathlib import Path
import numpy as np
from typing import Tuple, Union


def read_nifti(filename: Union[Path, str]) -> Tuple[np.ndarray, dict]:
    img = nib.load(filename)
    data3d = np.asarray(img.dataobj)
    voxelsize_mm = img.header.get_zooms()
    metadata = {
        'voxelsize_mm': voxelsize_mm,
        'affine': img.affine,
        'orientation_axcodes': nib.orientations.aff2axcodes(img.affine)
    }
    return data3d, metadata
