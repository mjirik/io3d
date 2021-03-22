import unittest
import pytest
import sys
from pathlib import Path
from loguru import logger
import io3d
import glob
import numpy as np
import shutil


import convert_coco_ann_to_mask


def test_coco_ann_to_mask():
    logger.debug(Path(".").absolute())
    input_path = Path(__file__).parent / "P026_test_data_coco.json"
    output_path = Path("./test_coco/")
    if output_path.exists():
        shutil.rmtree(output_path)

    convert_coco_ann_to_mask.CocoToMask(input_path, output_path, "Vena Cava")
    fnlist = output_path.glob("*")
    assert len(fnlist) > 0
    dp = io3d.read(output_path)
    un = np.unique(dp.data3d)
    assert 0 in un
    assert 1 in un


