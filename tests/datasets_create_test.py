#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

from loguru import logger

logger.enable("io3d")
import unittest
import os.path as op
import shutil
import sys
import numpy as np
import io3d
import os

from pathlib import Path

import pytest
import io3d.datasets_create
import glob


@unittest.skipIf(os.environ.get("TRAVIS", False), "Skip on Travis-CI")
def test_export_to_jpg():
    expected_output_path = "./test_export_to_jpg/"
    output_name = "img_"

    # get the expected path fo file
    dataset_label = "3Dircadb1"
    data_type = 'data3d'
    data_id = 1
    selected_dataset = io3d.datasets.DATASET_PATH_STRUCTURE[dataset_label]
    pth_fmt_str = (
        selected_dataset[data_type]
        if data_type in selected_dataset
        else selected_dataset["_"]
    )
    pth = pth_fmt_str.format(dataset_label=dataset_label, data_type=data_type, id=data_id)
    datapath = io3d.joinp(pth)
    assert Path(datapath).exists()

    io3d.datasets_create.export_to_jpg(datapath, expected_output_path, window_center=40, window_width=400,
                                       output_name=output_name)

    jpg_files = f"{expected_output_path}/{output_name}*.jpg"
    jpg_files_list = glob.glob(jpg_files)

    # are there any files in expected_output_path
    assert len(jpg_files_list) > 0

