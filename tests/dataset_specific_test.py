#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""
Module for testing format rawiv
"""
from loguru import logger

logger.enable("io3d")

import unittest
import os.path as op
import shutil
import sys
import numpy as np
import io3d
from pathlib import Path

import pytest


def test_change_specific_dataset():
    dp_new4 = "~/io3d_test4_dataset_dir/"

    dp_specific = str(Path("~/io3d_test3_dataset_dir/").expanduser())
    dp_specific_prefix = "io3d/test3/"

    dp_old = io3d.datasets.join_path(get_root=True)
    # io3d.datasets.set_dataset_path(dp_new4)

    logger.info("prepared to search")
    io3d.datasets.set_specific_dataset_path(
        dp_specific, key_path_prefix=dp_specific_prefix
    )

    dp_joined1 = io3d.datasets.join_path("io3d/test3/something/more", get_root=True)
    logger.debug(f"dp_joined1: {dp_joined1}")

    # check if the specific path is nested in
    assert (
        not Path(dp_old) in Path(dp_joined1).parents
    ), "specific path should not be nested"
    logger.debug(f"dp_specific={dp_specific}")
    logger.debug(f"dp_joined1.parents={list(Path(dp_joined1).parents)}")
    assert (
        Path(dp_specific).expanduser() in Path(dp_joined1).parents
    ), "specific path should nested"

    dp_joined12 = io3d.datasets.join_path("io3d/test3/", get_root=True)
    logger.debug(f"dp_joined12: {dp_joined12}")
    assert (
        not Path(dp_specific) in Path(dp_joined12).parents
    ), "specific path should nested"

    io3d.datasets.delete_specific_dataset_path(dp_specific_prefix)
    dp_joined2 = io3d.datasets.join_path("io3d/test3/something/more", get_root=True)
    logger.debug(f"dp_joined2: {dp_joined2}")
    assert (
        Path(dp_old) in Path(dp_joined2).parents
    ), "specific path is now not specific and should be nested"

    # Path(dp_joined1)

    # return path back
    # io3d.datasets.set_dataset_path(dp_old)


def test_change_specific_dataset():
    key = "test"

    io3d.datasets.delete_dataset_path_structure(key)
    dataset_path_structure = {
        key: {
            "data3d": "medical/orig/sliver07/training/liver-orig{id:03d}.mhd",
            "liver": "medical/orig/sliver07/training/liver-seg{id:03d}.mhd",
            "_": "medical/orig/sliver07/training_extra/{data_type}-{id:03d}.mhd",
        }
    }
    io3d.datasets.add_dataset_path_structure(dataset_path_structure)

    dps = io3d.datasets.get_dataset_path(
        dataset_label=key, data_type="data3d", data_id=3
    )
    assert str(dps).find("medical") > 0
    # Remove key
    io3d.datasets.delete_dataset_path_structure(key)
    with pytest.raises(KeyError):
        dps = io3d.datasets.get_dataset_path(
            dataset_label=key, data_type="data3d", data_id=3
        )
