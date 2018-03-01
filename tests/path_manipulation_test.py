#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
# import funkcí z jiného adresáře
import unittest
import os
import os.path as op

# path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

import shutil


import numpy as np

from nose.plugins.attrib import attr
try:
    import dicom as pydicom
    pydicom.debug(False)
except:
    import pydicom

#
import io3d
# import io3d.datawriter as dwriter
import io3d.datareader as dreader

# import sed3 as pyed
SAMPLE_DATA_DIR = "./sample_data"


class PathManipulationTest(unittest.TestCase):

    def generate_waving_data(self, szx, szy, szz, value=150, dtype=np.uint8):
        """
        generating smooth non constant data
        """
        data3d = np.zeros([szz, szx, szx], dtype=dtype)
        for i in range(0, data3d.shape[0]):
            x = int(np.sin(i*2*np.pi/(szz - 40.0))*((szx-2)/2) + szx/2)
            y = int(np.cos(i*2*np.pi/(0.3*(szz - 4.0)))*((szy-2)/2) + szy/2)
            # x = int(np.sin(i*2*np.pi/40.0)*((szx-2)/2) + szx/2)
            # print(x, '   ', y)
            data3d[i, 0:x, y:-1] = value
        return data3d
    #
    # @attr('actual')
    # def test_save_image_stack_based_on_filename(self):
    #     testdatadir = 'test_svimstack2'
    #     if os.path.exists(testdatadir):
    #         shutil.rmtree(testdatadir)
    #     szx = 30
    #     szy = 20
    #     szz = 120
    #     data3d = self.generate_waving_data(
    #         szx, szy, szz, value=150, dtype=np.uint8)
    #     # import sed3
    #     # ed = sed3.sed3(data3d)
    #     # ed.show()
    #     #
    #     io3d.write(data3d, testdatadir + "/soubory{:04d}.tiff")
    #
    #
    #
    #     dr = dreader.DataReader()
    #     data3dnew, metadata = dr.Get3DData(
    #         testdatadir
    #         # 'sample_data/volumetrie/'
    #     )
    #     # import sed3
    #     # ed = sed3.sed3(data3dnew)
    #     # ed.show()
    #     self.assertEqual(
    #         np.sum(np.abs(data3d - data3dnew)),
    #         0
    #     )
    #     shutil.rmtree(testdatadir)
    #
    def test_save_image_stack_with_unique_series_number_based_on_filename1(self):
        testdatadir = 'test_svimstack2'
        if os.path.exists(testdatadir):
            shutil.rmtree(testdatadir)
        szx = 30
        szy = 20
        szz = 120
        data3d = self.generate_waving_data(
            szx, szy, szz, value=150, dtype=np.uint8)
        filepattern =  testdatadir + "/{series_number:03d}/soubory{slice_position:07.3f}.tiff"
        io3d.write(data3d,filepattern)
        series_number = io3d.datawriter.get_unoccupied_series_number(filepattern=filepattern)
        out = io3d.datawriter.filepattern_fill_series_number(filepattern, series_number=15)

        # second time there should be directory 002/
        io3d.write(data3d,filepattern)


        series_number = io3d.datawriter.get_unoccupied_series_number(filepattern=filepattern)
        out = io3d.datawriter.filepattern_fill_series_number(filepattern, series_number=15)

        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
            testdatadir + "/002/",
            dataplus_format=False
            # 'sample_data/volumetrie/'
        )
        # import sed3
        # ed = sed3.sed3(data3dnew)
        # ed.show()
        self.assertEqual(
            np.sum(np.abs(data3d - data3dnew)),
            0
        )
        shutil.rmtree(testdatadir)


    def test_fill_series_number(self):
        import io3d.datawriter

        out = io3d.datawriter.filepattern_fill_series_number("{seriesn:03d}/{slicen:06d}", series_number=15)
        self.assertEqual(out, '015/{slicen:06d}')

    def test_fill_series_number_delete(self):
        import io3d.datawriter

        out = io3d.datawriter.filepattern_fill_series_number("{seriesn:03d}/{slicen:06d}", series_number="")
        self.assertEqual(out, '/{slicen:06d}')

    def test_fill_slice_number_delete(self):
        import io3d.datawriter

        out = io3d.datawriter.filepattern_fill_slice_number_or_position("{seriesn:03d}/ra{slicen:06d}.jpg", "")
        self.assertEqual(out, '{seriesn:03d}/ra.jpg')

    def test_fill_slice_number(self):
        import io3d.datawriter

        out = io3d.datawriter.filepattern_fill_slice_number_or_position("{seriesn:03d}/ra{slice_number:06d}.jpg", 10)
        self.assertEqual(out, '{seriesn:03d}/ra000010.jpg')

if __name__ == "__main__":
    unittest.main()
