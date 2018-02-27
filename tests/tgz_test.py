#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)
# import funkcí z jiného adresáře
# import sys
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
import io3d
import io3d.tgz
import io3d.dcmreaddata as dcmr
sample_data_path = "~/data/medical/orig/sample_data/"
sample_data_path = op.expanduser(sample_data_path)



class DicomReaderTest(unittest.TestCase):
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

    @attr('dataset')
    def test_untar(self):
        dcmdir = os.path.join(sample_data_path, '../sample_data/72136132.tar.bz2')
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)

        io3d.tgz.untar(dcmdir)
        # data3d, metadata = io3d.datareader.read(dcmdir)

    @attr('dataset')
    def test_tar_read(self):
        dcmdir = os.path.join(sample_data_path, '../sample_data/72136132.tar.bz2')
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)

        # io3d.tgz.untar(dcmdir)
        data3d, metadata = io3d.datareader.read(dcmdir, dataplus_format=False)
#slice size is 512x512
        # self.assertEqual(data3d.shape[2], 512)
# voxelsize depth = 5 mm
#         self.assertEqual(metadata['voxelsize_mm'][0], 5)

if __name__ == "__main__":
    unittest.main()
