#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import logging
logger = logging.getLogger(__name__)

try:
    import pydicom
except ImportError:
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom as pydicom
    logger.debug("dicom imported - it would be better use pydicom")

import unittest
import os.path as op
import os
import io3d
import io3d.anonym

skip_on_local = False
class AnonTestCase(unittest.TestCase):

    @unittest.skipIf(os.environ.get("TRAVIS", skip_on_local), "Skip on Travis-CI")
    def test_anon_file(self):
        # print("get travis", os.environ.get("TRAVIS"))
        # print("get travis", os.environ.get("TRAVIS", default=skip_on_local))
        # print("get travis", skip_on_local)
        output_file = "output_anon.dcm"
        if op.exists(output_file):
            os.remove(output_file)
        anon = io3d.anonym.Anonymizer()
        cesta_k_souboru_jater = io3d.datasets.join_path("medical", "orig", "jatra_5mm", "IM-0001-0001.dcm", get_root=True)
        anon.file_anonymization(cesta_k_souboru_jater, output_file)
        self.assertTrue(op.exists(output_file))

     
        dcm = pydicom.read_file(output_file)

        logger.debug(dcm.PatientName)
        # self.assertTrue(len(dcm.PatientName) ==  0)
        self.assertEqual(len(str(dcm.PatientName)), 0, "Patient name should be empty")

        self.assertTrue(False)

    @unittest.skipIf(os.environ.get("TRAVIS", skip_on_local), "Skip on Travis-CI")
    def test_anon_dir(self):
        # naimplemetovat test pro rekurzivní
        pass


if __name__ == '__main__':
    unittest.main()
