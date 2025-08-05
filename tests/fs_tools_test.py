import pytest
from io3d import fs_tools as fst
from pathlib import Path


def test_leaf_dirs_with_files(tmp_path):
    dataset_base_path = Path(r"~/mnt/nas-bmc3_ct/Prasata H/2021").expanduser().resolve()

    fst.get_leaf_dirs_with_files(dataset_base_path)