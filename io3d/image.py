#! /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union
import numpy as np
from pathlib import Path
from loguru import logger


class DataPlus(dict):
    @property
    def voxelsize_mm(self):
        return self["voxelsize_mm"]

    @voxelsize_mm.setter
    def voxelsize_mm(self, voxelsize_mm):
        self["voxelsize_mm"] = voxelsize_mm

    @property
    def data3d(self) -> np.ndarray:
        return self["data3d"]

    @data3d.setter
    def data3d(self, value: np.ndarray):
        self["data3d"] = value

    @property
    def segmentation(self) -> np.ndarray:
        return self["segmentation"]

    @segmentation.setter
    def segmentation(self, value:np.ndarray):
        self["segmentation"] = value

    @property
    def slab(self):
        return self["slab"]

    @slab.setter
    def slab(self, value):
        self["slab"] = value

    @property
    def orientation_axcodes(self):
        return self["orientation_axcodes"]

    @orientation_axcodes.setter
    def orientation_axcodes(self, value):
        self["orientation_axcodes"] = value

    @property
    def affine(self):
        return self["affine"]

    @affine.setter
    def affine(self, value):
        self["affine"] = value

    def transform_orientation(self, axcodes: str):
        """
        Change the orientation of data3d and voxelsize_mm.

        NiBabel package is used internally (https://nipy.org/nibabel/reference/nibabel.orientations.html)

        :param axcodes: Three-letter code. Most used axcodes are LPS (Left, Posterior and Superior) and RAS (Right,
        Anterior and Superior).  First letters of words Left, Right, Superior,
        Inferior, Anterior and Posterior can be used to describe anatomical orientation.
        To describe common orientation can be used words Left, Right, Up, Down, Front and Back.
        Left means from right to left, Superior means from inferior to superior.
        We use SPL as default orientation.
        """
        if "orientations_axcodes" in self.keys():
             input_axcodes = self["orientation_axcodes"]
        else:
            self["orientation_axcodes"] = "SPL"
            input_axcodes = "SPL"
        self["data3d"] = transform_orientation(self["data3d"], input_axcodes, axcodes)
        self["voxelsize_mm"] = transform_orientation_voxelsize(
            self["voxelsize_mm"], input_axcodes, axcodes
        )
        self["orientation_axcodes"] = axcodes
        if "affine" in self:
            logger.warning("Affine transfomation is not implemented.")

    def write(self, path: Union[str, Path], *args, **kwargs):
        import io3d.datawriter

        return io3d.datawriter.write(self["data3d"], path=path, *args, **kwargs)

    def get_projection(
            self,
            # datap: io3d.image.DataPlus,
            axis: Union[int, str]='axial', method: str = "max"
    ):
        """Get projection of 3D data to 2D."""
        if isinstance(axis, str):
            dict_axis = {"axial": 0, "coronal": 1, "sagittal": 2}
            if axis in dict_axis:
                axis = dict_axis[axis]
            else:
                raise ValueError(f"Unknown axis {axis}, use one of {list(dict_axis.keys())} or 0, 1, 2")

        data3d = self.data3d
        axcodes = self.orientation_axcodes
        data3d = transform_orientation(data3d, axcodes, "SPL")
        if method == "max":
            data2d = data3d.max(axis=axis)
        elif method == "mean":
            data2d = data3d.mean(axis=axis)
        else:
            raise ValueError(f"Unknown method {method}")
        return data2d

    # def __getattr__(self, attr):
    #     print(f"attr: {attr}")
    #     return self[attr]
    #     # KeyError
    #
    # def __setattr__(self, attr, value):
    #     print(f"attr: {attr}: {value}")
    #     self[attr] = value


def as_datap(obj: Union[dict, DataPlus]) -> DataPlus:
    """
    Convert dict to DataPlus format if necessary.
    :param obj:
    :return:
    """
    if type(obj) == DataPlus:
        return obj
    elif type(obj) == dict:
        return DataPlus(obj)
    elif obj is None:
        return None
    else:
        raise TypeError("Type Dict or type DataPlus expected.")


def transform_orientation(arr: np.ndarray, input_axcodes, output_axcodes):
    """
    Change the orientation of the array. Most used axcodes are LPS (Left, Posterior and Superior) and RAS (Right,
    Anterior and Superior).  First letters of words Left, Right, Superior,
    Inferior, Anterior and Posterior can be used to describe anatomical orientation.
    To describe common orientation can be used words Left, Right, Up, Down, Front and Back.
    Left means from right to left, Superior means from inferior to superior.

    NiBabel package is used internally (https://nipy.org/nibabel/reference/nibabel.orientations.html)

    :param arr: input numpy array
    :param input_axcodes: Three letters describing the axis orientation. 'LPS' and 'RAS' are most common codes.
    :param output_axcodes:Three letters describing the axis orientation. 'LPS' and 'RAS' are most common codes.
    :return: transformed array
    """

    # ║ Common ║ Anatomical ║
    # ╠════════╬════════════╣
    # ║ Left   ║ Left       ║
    # ║ Right  ║ Right      ║
    # ║ Up     ║ Superior   ║
    # ║ Down   ║ Inferior   ║
    # ║ Front  ║ Anterior   ║
    # ║ Back   ║ Posterior
    import nibabel

    ornt_my = nibabel.orientations.axcodes2ornt(input_axcodes)
    ornt_ras = nibabel.orientations.axcodes2ornt(output_axcodes)


    try:
        ornt = nibabel.orientations.ornt_transform(ornt_my, ornt_ras)
        data3d_ornt = nibabel.orientations.apply_orientation(arr, ornt)
    except Exception as e:
        logger.error(f"Error in orientation transformation: {e}")
        logger.error(f"Input axcodes: {input_axcodes}, ornt_my: {ornt_my}")
        logger.error(f"Output axcodes: {output_axcodes}, ornt_ras: {ornt_ras}")
        import traceback
        traceback.print_exc()


    return data3d_ornt


def transform_orientation_voxelsize(
    voxelsize: np.ndarray, input_axcodes, output_axcodes
):
    """
    Change the orientation of the array. We use 'SPL'. Most used axcodes are LPS (Left, Posterior and Superior) and
    RAS (Right, Anterior and Superior).  First letters of words Left, Right, Superior,
    Inferior, Anterior and Posterior can be used to describe anatomical orientation.
    To describe common orientation can be used words Left, Right, Up, Down, Front and Back.
    Left means from right to left, Superior means from inferior to superior.

    NiBabel package is used internally (https://nipy.org/nibabel/reference/nibabel.orientations.html)

    :param voxelsize: input voxelsize
    :param input_axcodes: Three letters describing the axis orientation. We use 'SPL'. 'LPS' and 'RAS' are most common codes.
    :param output_axcodes:Three letters describing the axis orientation. We use 'SPL'. 'LPS' and 'RAS' are most common codes.
    :return: transformed array
    """
    import nibabel

    ornt_my = nibabel.orientations.axcodes2ornt(input_axcodes)
    ornt_ras = nibabel.orientations.axcodes2ornt(output_axcodes)
    voxelsize_mid = [0, 0, 0]
    voxelsize_mid[int(ornt_my[0][0])] = voxelsize[0]
    voxelsize_mid[int(ornt_my[1][0])] = voxelsize[1]
    voxelsize_mid[int(ornt_my[2][0])] = voxelsize[2]
    voxelsize_out = [
        voxelsize_mid[int(ornt_ras[0][0])],
        voxelsize_mid[int(ornt_ras[1][0])],
        voxelsize_mid[int(ornt_ras[2][0])],
    ]
    return voxelsize_out
