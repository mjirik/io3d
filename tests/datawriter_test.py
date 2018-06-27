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
    import dicom
    dicom.debug(False)
except:
    import pydicom as dicom

#
import io3d
import io3d.datawriter as dwriter
import io3d.datareader as dreader

# import sed3 as pyed
SAMPLE_DATA_DIR = "~/data/medical/orig/sample_data"


class DicomWriterTest(unittest.TestCase):
    # def setUp(self):
    #     import imtools
    #     import imtools.sample_data
    #     imtools.sample_data.get_sample_data(["jatra_5mm", "volumetrie"], SAMPLE_DATA_DIR)

    # def test_write_h5(self):
    #     """
    #     Reads dicom data and from slices and stores into one Dicom file. This
    #     file is then readed and compared with input data.
    #     """
    #     filename = 'tests/output_dcm3d.dcm'
    #     dr = dreader.DataReader()
    #     data3d, metadata = dr.Get3DData(
    #         'sample_data/jatra_5mm/'
    #         # 'sample_data/volumetrie/'
    #     )
    #     # import pdb; pdb.set_trace()
    #
    #
    #     dw = dwriter.DataWriter()
    #     dw.Write3DData(data3d, filename, filetype='dcm', metadata=metadata)
    #
    #     data3d_n, metadata_n = dr.Get3DData(filename)
    #     self.assertEqual(data3d[10, 11, 12], data3d_n[10, 11, 12])
    #     os.remove(filename)

    @attr('dataset')
    def test_write_dicom_from_scratch(self):
        """
        Reads dicom data and from slices and stores into one Dicom file. This
        file is then readed and compared with input data.
        """
        filename = 'tests/output_dcm3d.dcm'
        dr = dreader.DataReader()
        path_to_data = op.join(SAMPLE_DATA_DIR, 'jatra_5mm')
        logger.debug(SAMPLE_DATA_DIR)
        logger.debug(path_to_data)
        data3d, metadata = dr.Get3DData(
            path_to_data, dataplus_format=False
            # 'sample_data/volumetrie/'
        )
        dw = dwriter.DataWriter()
        dw.Write3DData(data3d, filename, filetype='dcm', metadata=metadata)

        data3d_n, metadata_n = dr.Get3DData(filename, dataplus_format=False)
        self.assertEqual(data3d[10, 11, 12], data3d_n[10, 11, 12])
        os.remove(filename)

#    def setUp(self):
#        self.dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
# self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
#        reader = dcmr.DicomReader(self.dcmdir)
#        self.data3d = reader.get_3Ddata()
#        self.metadata = reader.get_metaData()
    def test_write_and_read(self):
        filename = 'test_file.dcm'
        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        metadata = {'voxelsize_mm': [1, 2, 3]}
        dw = dwriter.DataWriter()
        logger.debug(filename)
        dw.Write3DData(data, filename, filetype='dcm', metadata=metadata)

        dr = dreader.DataReader()
        newdata, newmetadata = dr.Get3DData(filename, dataplus_format=False)

        # print("meta ", metadata)
        # print("new meta ", newmetadata)

        # hack with -1024, because of wrong data reading
        self.assertEqual(data[10, 10, 10], newdata[10, 10, 10])
        self.assertEqual(data[2, 10, 1], newdata[2, 10, 1])
        # print(metadata["voxelsize_mm"])
        # print(newmetadata["voxelsize_mm"])
        self.assertEqual(metadata['voxelsize_mm'][0],
                         newmetadata['voxelsize_mm'][0])
        self. assertEqual(metadata['voxelsize_mm'][1],
                          newmetadata['voxelsize_mm'][1])
        self.assertEqual(metadata['voxelsize_mm'][2],
                         newmetadata['voxelsize_mm'][2])
        os.remove(filename)

    def test_write_and_read_pklz(self):
        filename = 'test_file.pklz'
        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        metadata = {'voxelsize_mm': [1, 2, 3]}
        dw = dwriter.DataWriter()
        dw.Write3DData(data, filename, filetype='auto', metadata=metadata)

        dr = dreader.DataReader()
        newdata, newmetadata = dr.Get3DData(filename, dataplus_format=False)

        # print("meta ", metadata)
        # print("new meta ", newmetadata)

        # hack with -1024, because of wrong data reading
        self.assertEqual(data[10, 10, 10], newdata[10, 10, 10])
        self.assertEqual(data[2, 10, 1], newdata[2, 10, 1])
        self.assertEqual(metadata['voxelsize_mm'][0],
                         newmetadata['voxelsize_mm'][0])


    @unittest.skip('SliceThickness is not stored in dicom files')
    def test_write_dcm_slices_datap(self):
        # Z nějakého důvodu plošné snímky neukládají tloušťku řezu. Jinak by test měl fungovat.
        datadir = "test_dcm"
        filename = datadir + '/test_file{slice_position:07.3f}.dcm'
        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        datap = {'voxelsize_mm': [1, 2, 3], "data3d": data}
        dw = dwriter.DataWriter()
        dw.Write3DData(datap, filename, filetype='auto')

        dr = dreader.DataReader()
        newdata, newmetadata = dr.Get3DData(datadir, dataplus_format=False)

        # print("meta ", metadata)
        # print("new meta ", newmetadata)

        # hack with -1024, because of wrong data reading
        self.assertEqual(data[10, 10, 10], newdata[10, 10, 10])
        self.assertEqual(data[2, 10, 1], newdata[2, 10, 1])
        self.assertEqual(datap['voxelsize_mm'][0],
                         newmetadata['voxelsize_mm'][0])
        # os.removedirs()
        shutil.rmtree(datadir)

    @attr("slow")
    def test_read_mhd_and_write_pklz(self):
        """
        test data on sliver dataset
        :return:
        """
        # infn = op.join(op.expanduser(io3d.datasets.local_dir), "sliver07/training/liver-orig001.mhd")
        infn = io3d.datasets.join_path("liver-orig001.mhd")
        datap = io3d.read(infn, dataplus_format=True)
        datap["segmentation"] = np.zeros_like(datap["data3d"], dtype=np.uint8)

        io3d.write(datap, path="test_mhd.pklz")

    def test_write_hdf5(self):
        filename = 'test_file.hdf5'
        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        metadata = {'voxelsize_mm': [1, 2, 3]}
        dwriter.write(data, filename, filetype='hdf5', metadata=metadata)


    # @attr('interactive')
    @attr('interactive')
    def test_write_and_read_hdf5(self):
        filename = 'test_file.hdf5'
        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        metadata = {'voxelsize_mm': [1, 2, 3]}
        dwriter.write(data, filename, filetype='hdf5', metadata=metadata)

        newdata, newmetadata = dreader.read(filename, dataplus_format=False)

        # hack with -1024, because of wrong data reading
        self.assertEqual(data[10, 10, 10], newdata[10, 10, 10])
        self.assertEqual(data[2, 10, 1], newdata[2, 10, 1])
        self.assertEqual(newmetadata['voxelsize_mm'][0],
                         newmetadata['voxelsize_mm'][0])
# @TODO there is a bug in SimpleITK. slice voxel size must be same
        # self. assertEqual(metadata['voxelsize_mm'][1],
        #                   newmetadata['voxelsize_mm'][1])
        self.assertEqual(metadata['voxelsize_mm'][2],
                         newmetadata['voxelsize_mm'][2])
        os.remove(filename)

    def test_write_single_dicom(self):
        filename = 'tests_outputs/single_test_file.dcm'
        filedir = os.path.dirname(filename)
        data3d = np.zeros([10,10,10], dtype=np.uint8)
        data3d [1:, 5, 3:9] = 124
        data3d [3:, 2:7, 4] = 60

        io3d.write(data3d, filename)
        os.remove(filename)

    def test_add_overlay_and_read_one_file_with_overlay(self):
        filename = 'tests_outputs/test_file.dcm'
        filedir = os.path.dirname(filename)

        # number of tested overlay
        i_overlay = 6

        if not os.path.exists('tests_outputs'):
            os.mkdir('tests_outputs')

        data = (np.random.random([30, 100, 120]) * 30).astype(np.int16)
        data[0:5, 20:60, 60:70] += 30
        overlay = np.zeros([512, 512], dtype=np.uint8)
        overlay[450:500, 30:100] = 1

        # metadata = {'voxelsize_mm': [1, 2, 3]}
        dw = dwriter.DataWriter()
        dw.add_overlay_to_slice_file(
            # 'sample_data/jatra_5mm/IM-0001-0019.dcm',
            op.join(SAMPLE_DATA_DIR, 'volumetrie/volumetry_slice.DCM'),
            overlay,
            i_overlay,
            filename
        )
        # import ipdb; ipdb.set_trace()
        # print("asdfa")
        dr = dreader.DataReader()
        newdata, newmetadata = dr.Get3DData('tests_outputs', dataplus_format=False)
        newoverlay = dr.get_overlay()
        # print(newoverlay)

        # ed = pyed.py3DSeedEditor(newoverlay[6])
        # ed.show()
        # print("oioiu")
        self.assertTrue((newoverlay[i_overlay] == overlay).all())

        # os.remove(filename)
        shutil.rmtree(filedir)

    def test_add_overlay_to_copied_dir(self):
        """
        writes 3d label to copied dicom files
        """
        filedir = 'test_outputs_dir'
        n_files = 3

        # number of tested overlay
        i_overlay = 6

        if not os.path.exists(filedir):
            os.mkdir(filedir)

# open copied data to obtain dcmfilefilelist
        dr = dreader.DataReader()
        data3d, metadata = dr.Get3DData(
            op.join(SAMPLE_DATA_DIR, 'jatra_5mm/'), dataplus_format=False
            # 'sample_data/volumetrie/'
        )
# for test we are working only with small number of files (n_files)
        metadata['dcmfilelist'] = metadata['dcmfilelist'][:n_files]

# create overlay
        overlay = np.zeros([n_files, 512, 512], dtype=np.uint8)
        overlay[:, 450:500, 30:100] = 1
# if there is more slides, try more complicated overlay
        overlay[0, 430:460, 20:110] = 1
        overlay[-1:, 470:520, 10:120] = 1

        overlays = {i_overlay: overlay}

        dw = dwriter.DataWriter()
        dw.DataCopyWithOverlay(metadata['dcmfilelist'], filedir, overlays)

# try read written data
        dr = dreader.DataReader()
        newdata, newmetadata = dr.Get3DData(filedir, dataplus_format=False)

        # test old function
        newoverlay = dr.GetOverlay()
        newoverlay = dr.get_overlay()


        self.assertTrue((newoverlay[i_overlay] == overlays[i_overlay]).all())

        # os.remove(filename)
        shutil.rmtree(filedir)

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

    @attr('actual')
    def test_save_image_stack_based_on_filename(self):
        testdatadir = 'test_svimstack2'
        if os.path.exists(testdatadir):
            shutil.rmtree(testdatadir, ignore_errors=True)
        szx = 30
        szy = 20
        szz = 120
        data3d = self.generate_waving_data(
            szx, szy, szz, value=150, dtype=np.uint8)
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()
        #
        io3d.write(data3d, testdatadir + "/soubory{:04d}.tiff")



        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
            testdatadir, dataplus_format=False
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

    def test_save_image_stack_with_unique_series_number_based_on_filename(self):
        testdatadir = 'test_svimstack2'
        if os.path.exists(testdatadir):
            shutil.rmtree(testdatadir, ignore_errors=True)
        szx = 30
        szy = 20
        szz = 120
        data3d = self.generate_waving_data(
            szx, szy, szz, value=150, dtype=np.uint8)
        io3d.write(data3d, testdatadir + "/{series_number:03d}/soubory{slice_position:07.3f}.tiff")
        # second time there should be directory 002/
        io3d.write(data3d, testdatadir + "/{series_number:03d}/soubory{slice_position:07.3f}.tiff")



        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
            testdatadir + "/002/", dataplus_format=False
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

    def test_save_image_stack(self):
        testdatadir = 'test_svimstack'
        if os.path.exists(testdatadir):
            shutil.rmtree(testdatadir, ignore_errors=True)
        szx = 30
        szy = 20
        szz = 120
        data3d = self.generate_waving_data(
            szx, szy, szz, value=150, dtype=np.uint8)
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()
        #
        dw = dwriter.DataWriter()

        dw.save_image_stack(data3d, testdatadir + '/soubory.png')
        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
            testdatadir, dataplus_format=False
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

    def test_save_image_stack_with_writer(self):
        testdatadir = 'test_svimstack_with_writer'
        data3d = self.generate_waving_data(
            szx=30, szy=20, szz=10, value=150, dtype=np.uint8)
        dw = dwriter.DataWriter()

        dw.Write3DData(data3d, testdatadir + '/soubory.png',
                       filetype='image_stack')
        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
            testdatadir, dataplus_format=False
        )
        # import sed3
        # ed = sed3.sed3(data3dnew)
        # ed.show()
        self.assertEqual(
            np.sum(np.abs(data3d - data3dnew)),
            0
        )
        shutil.rmtree(testdatadir)

    def test_SimpleITK(self):
        path = "new_dcmfile.dcm"
        data3d = np.zeros([10, 15, 20], dtype='uint16')
        vsz = np.asarray([2,3,1.5])

        import SimpleITK as sitk
        dim = sitk.GetImageFromArray(data3d)
        dim.SetSpacing([vsz[1], vsz[2], vsz[0]])
        sitk.WriteImage(dim, path)


    def test_fill_series_number(self):
        import io3d.datawriter

        out = io3d.datawriter.filepattern_fill_series_number("{seriesn:03d}/{slicen:06d}", series_number=15)
        self.assertEqual(out, '015/{slicen:06d}')

    @attr('interactive')
    def test_read_data_without_slice_thickness(self):
        """ data without SliceThickness
        :return:
        """

        dr = dreader.DataReader()
        data3dnew, metadata = dr.Get3DData(
                "~/data/medical/orig/dicom_test_claudio", dataplus_format=False
        )
        metadata

if __name__ == "__main__":
    unittest.main()
