#! /usr/bin/env python
# -*- coding: utf-8 -*-


from loguru import logger

# import funkcí z jiného adresáře
# import sys
import os.path
import os.path as op

# import copy

import unittest

# sample_data_path = os.path.dirname(os.path.abspath(__file__))
# sample_data_path
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
import sys

import numpy as np

try:
    import dicom

    dicom.debug(False)
except:
    import pydicom as dicom

    dicom.config.debug(False)
#
import io3d
import io3d.datasets
import io3d.dicomdir
from pathlib import Path
import os
import io3d.dcmreaddata as dcmr

# sample_data_path = "~/data/medical/orig/sample_data/"
# sample_data_path = op.expanduser(sample_data_path)
sample_data_path = io3d.datasets.join_path("sample_data")


class DicomdirTest(unittest.TestCase):
    interactivetTest = False

    @unittest.skip("waiting for implementation")
    def test_dicomdir_ircad(self):
        dcmdir = Path(io3d.datasets.join_path("3Dircadb1.1", "PATIENT_DICOM"))
        expected_dicomdir_path = dcmdir / "DICOMDIR"

        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        if expected_dicomdir_path.exists():
            os.remove(expected_dicomdir_path)

        dicomdir = io3d.dicomdir.Dicomdir(dcmdir)
        dicomdir.create_dicomdir()
        self.assertTrue(expected_dicomdir_path.exists())


if __name__ == "__main__":
    unittest.main()
