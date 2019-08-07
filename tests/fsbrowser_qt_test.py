#! /usr/bin/env python
# -*- coding: utf-8 -*-


from loguru import logger

# import funkcí z jiného adresáře
import os.path
import os.path as op

# import copy

import unittest

# sample_data_path = os.path.dirname(os.path.abspath(__file__))
# sample_data_path
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

# from PyQt4.QtGui import QFileDialog, QApplication, QMainWindow

import numpy as np

try:
    import dicom

    dicom.debug(False)
except:
    import pydicom as dicom

    dicom.config.debug(False)

#
import sys
import io3d
import io3d.dcmreaddata as dcmr

# sample_data_path = "~/data/medical/orig/sample_data/"
# sample_data_path = op.expanduser(sample_data_path)

from PyQt5.QtWidgets import QApplication
import io3d.outputqt
import io3d.datareaderqt
import io3d.datasets


class QtTest(unittest.TestCase):
    @unittest.skip("waiting for implementation")
    def test_fsbrowser_qt(self):
        import pydicom.data

        # filepath = pydicom.data.get_testdata_files('DICOMDIR')[0]
        filepath = op.join(
            pydicom.data.DATA_ROOT, "test_files/dicomdirtests/98892001/CT2N"
        )

        sdp = io3d.datasets.join_path("sample_data")
        dp = io3d.datasets.join_path("sample_data/jatra_5mm/")
        app = QApplication(sys.argv)

        fsw = io3d.fsbrowser.FilePathInfoWidget()
        fsw.refresh_path(filepath)

        # app.exec_()


if __name__ == "__main__":
    unittest.main()
