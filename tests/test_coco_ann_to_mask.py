import unittest
import pytest
import sys
from pathlib import Path
from loguru import logger
import io3d
import glob
import numpy as np
import shutil
import regex


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


def test_all_masks():
    organ_keys = ["Left Kidney", "Right Kidney"]
    output_type = ".png"
    output_path = Path(r"H:\biomedical\orig\pilsen_pigs_raw\transplantation\annotations")
    filenames = list(output_path.glob("**/*.json"))
    logger.debug(filenames)
    # fn = filenames[0]
    # str(fn)
    for fn in filenames:
        for organ_key in organ_keys:
            organ_key_file = organ_key.lower().replace(" ", "_")

            out = regex.findall(f"tx([0-9]+)d", str(fn))
            # logger.debug(out)
            output_path = io3d.datasets.get_dataset_path("pilsen_pigs", organ_key_file, data_id=int(out[0]))
            logger.debug(f"output_path={output_path}, exists={output_path.exists()}")
            convert_coco_ann_to_mask.coco_to_mask(fn, output_path, organ_key , output_type=output_type)

            datap = io3d.read(output_path)
            unq, counts = np.unique(datap.data3d, return_counts=True)
            if len(unq) < 2:
                logger.debug(counts)


def test_check_mask():
    data_id = 25
    organ_key = "Left Kidney"
    output_type = ".png"
    organ_key_file = organ_key.lower().replace(" ", "_")
    output_path = io3d.datasets.get_dataset_path("pilsen_pigs", organ_key_file, data_id=data_id)

    datap = io3d.read(output_path)
    counts = np.unique(datap.data3d, return_counts=True)
    logger.debug(counts)


