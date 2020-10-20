import pytest


import io3d.files
import shutil
import os
from pathlib import Path


def test_unique_path():

    odir = Path("tests/test_unique_path")
    if odir.exists():
        shutil.rmtree(odir)
    os.makedirs(odir, exist_ok=True)
    first_fn = odir / "test001.txt"
    general_fn = odir / "test{:03d}.txt"
    fn = io3d.files.unique_path(general_fn)
    assert fn == first_fn
