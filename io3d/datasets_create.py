#! /usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
from pathlib import Path
from typing import TypeVar, Union
from numbers import Number



def export_to_jpg(
        input_path:Union[Path, str],
        output_path:Union[Path, str],
        window_center:Number,
        window_width:Number,
        output_name:str="image_",
        cmap='gray'
):
    """
    Read volumetric data form dir, apply intnsity windowing and store the output to the series of JPGs.

    :param input_path:
    :param output_path:
    :param output_name: prefix of output filename
    :param window_center: intensity window center
    :param window_width: intensity window width
    :param cmap: Color map
    :return:
    """

    pass


# def extend_dataset(
#         dataset_label,
#         data_type=None,
#         id=None,
# ):
#     """
#     Exted dataset by bodynavigation distance maps. Maps are saved on hard-drive.
#
#     :param dataset_label: "sliver07" or "3Dircadb1"
#     :param data_type:  not implemented - "saggital"
#     :param id: not implemented
#     :return:
#     """
#     import io3d.datasets
#     # DATASET_PATH_STRUCTURE = {
#     #     "3Dircadb1": {
#     #         "data3d": "medical/orig/3Dircadb1.{id}/PATIENT_DICOM/",
#     #         "_": "medical/orig/3Dircadb1.{id}/MASKS_DICOM/{data_type}/",
#     #     },
#     #     "sliver07": {
#     #         "data3d": "medical/orig/sliver07/training/liver-orig{id:03d}.mhd",
#     #         "liver": "medical/orig/sliver07/training/liver-seg{id:03d}.mhd",
#     #         "_": "medical/orig/sliver07/training_extra/{data_type}-{id:03d}.mhd",
#     #     },
#     # }
#
#     # get the expected path fo file
#     selected_dataset = io3d.DATASET_PATH_STRUCTURE[dataset_label]
#     pth_fmt_str = (
#         selected_dataset[data_type]
#         if data_type in selected_dataset
#         else selected_dataset["_"]
#     )
#     pth = pth_fmt_str.format(dataset_label=dataset_label, data_type=data_type, id=id)
#     datapath = io3d.joinp(pth)
#
#
#
#
