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

try:
    import dicom
    dicom.debug(False)
except:
    import pydicom as dicom

#
import sys
import io3d
import io3d.dcmreaddata as dcmr
# sample_data_path = "~/data/medical/orig/sample_data/"
# sample_data_path = op.expanduser(sample_data_path)

from PyQt4.QtGui import QApplication
import io3d.outputqt
import io3d.datareaderqt
import io3d.datasets

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

    def test_read_datareader(self):
        sdp = io3d.datasets.join_path("sample_data")
        dp = io3d.datasets.join_path("sample_data/jatra_5mm/")
        app = QApplication(sys.argv)

        drw = io3d.datareaderqt.DataReaderWidget(loaddir=sdp, qt_app=app)
        # (widget_label="widget label", path="~/lisa_data/sample.{}.pkl")

        drw.show()
        drw.datapath = dp
        drw.read_data_from_prepared_datapath()
        # print(drw.datap["data3d"].shape)
        error = np.sum(np.abs(np.asarray([93, 512, 512]) - np.asarray(drw.datap["data3d"].shape)))
        # app.exec_()
        self.assertEqual(error, 0)

    @attr("interactive")
    def test_read_datareader_interactive(self):
        sdp = io3d.datasets.join_path("sample_data")
        dp = io3d.datasets.join_path("sample_data/jatra_5mm/")
        app = QApplication(sys.argv)

        drw = io3d.datareaderqt.DataReaderWidget(loaddir=sdp, qt_app=app)
        # (widget_label="widget label", path="~/lisa_data/sample.{}.pkl")

        drw.show()
        # drw.datapath = dp
        # drw.read_data_from_prepared_datapath()
        # error = np.sum(np.abs(np.asarray([93, 512, 512]) - np.asarray(drw.datap["data3d"].shape)))
        app.exec_()
        # self.assertEqual(error, 0)

    def test_qstring(self):
        if sys.version_info.major == 2:
            from PyQt4.QtCore import QString
            text = QString("i am qstring")
        else:
            text = "i am str"

        txt = io3d.datareaderqt.get_str(text)
        self.assertTrue(type(txt) is str)


if __name__ == "__main__":
    unittest.main()
