import unittest
import pytest
import sys
from pathlib import Path
from loguru import logger


import convert_coco_ann_to_mask


def test_coco_ann_to_mask():
    logger.debug(Path(".").absolute())
    convert_coco_ann_to_mask.CocoToMask("P026_test_data_coco.json", "./test_coco/", "Liver")
    # todo add assert


