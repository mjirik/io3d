import unittest
import pytest

import convert_coco_ann_to_mask



def test_coco_ann_to_mask():
    convert_coco_ann_to_mask.CocoToMask("devel/P026_test_data_coco.json", "./test_coco/")


