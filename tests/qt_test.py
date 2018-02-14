#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)
# import funkcí z jiného adresáře
import os.path
import os.path as op
# import copy

import unittest
from nose.plugins.attrib import attr
# sample_data_path = os.path.dirname(os.path.abspath(__file__))
# sample_data_path
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

# from PyQt4.QtGui import QFileDialog, QApplication, QMainWindow

import numpy as np

import dicom
dicom.debug(False)

#
import sys
import io3d
import io3d.dcmreaddata as dcmr
# sample_data_path = "~/data/medical/orig/sample_data/"
# sample_data_path = op.expanduser(sample_data_path)

from PyQt4.QtGui import QApplication
import io3d.outputqt

class QtTest(unittest.TestCase):
    interactivetTest = False

    # def setUp(self):
    #     import imtools
    #     import imtools.sample_data
    #     imtools.sample_data.get_sample_data(["jatra_5mm", "volumetrie"], SAMPLE_DATA_DIR)
#    def setUp(self):
#        self.dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
# self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
#        reader = dcmr.DicomReader(self.dcmdir)
#        self.data3d = reader.get_3Ddata()
#        self.metadata = reader.get_metaData()
    def test_select_ouput_path(self):
        app = QApplication(sys.argv)
        sopw = io3d.outputqt.SelectOutputPathWidget(widget_label="widget label", path="~/lisa_data/sample.{}.pkl")
        sopw.show()

        in_path = "~/sample{}.vtk"
        sopw.set_path(in_path)

        out_path = sopw.get_path()
        home = op.expanduser("~")

        rp1 = op.relpath(home, in_path)
        rp2 = op.relpath(home, out_path)
        # app.exec_()
        self.assertEqual(rp1, rp2)

    def test_select_ouput_filename(self):
        app = QApplication(sys.argv)
        sopw = io3d.outputqt.SelectOutputPathWidget(widget_label="widget label", path="~/lisa_data/sample.{}.pkl")
        sopw.show()

        in_path = "~/sample{}.vtk"
        sopw.set_path(in_path)

        out_path = sopw.get_filename()
        # app.exec_()
        self.assertEqual(out_path, "sample{}.vtk")

if __name__ == "__main__":
    unittest.main()
