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

from PyQt4.QtGui import QFileDialog, QApplication, QMainWindow
import sys

import numpy as np

try:
    import dicom as pydicom
    pydicom.debug(False)
except:
    import pydicom

#
import io3d
import io3d.dcmreaddata as dcmr
import io3d.fsbrowser
sample_data_path = "~/data/medical/orig/sample_data/"
sample_data_path = op.expanduser(sample_data_path)

class FileSystemBrowserTest(unittest.TestCase):

    @unittest.skip('waiting for implementation')
    def test_fsbrowser(self):

        # TODO make test stronger
        filepath = pydicom.data.get_testdata_files('DICOMDIR')[0]
        fsb = io3d.fsbrowser.FileSystemBrowser(filepath)
        dirlist = fsb.list_directory()
        self.assertTrue("path" in dirlist[0])
        self.assertTrue("name" in dirlist[0])


if __name__ == "__main__":
    unittest.main()
