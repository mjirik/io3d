import unittest
import pytest
import sys
from pathlib import Path
from loguru import logger
import io3d
import glob
import numpy as np
import shutil


from io3d import convert_coco_ann_to_mask


def test_coco_ann_to_mask():
    logger.debug(Path(".").absolute())
    input_path = Path(__file__).parent / "P026_test_data_coco.json"
    output_path = Path("./test_coco/")

    output_type = 'png'

    if output_path.exists():
        shutil.rmtree(output_path)

    convert_coco_ann_to_mask.coco_to_mask(input_path, output_path, "Vena Cava", output_type=output_type)
    fnlist = output_path.glob(f"*.{output_type}")
    assert len(list(fnlist)) > 0
    dp = io3d.read(output_path)
    un = np.unique(dp.data3d)
    assert 0 in un
    assert len(un) == 2


