#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import os
import os.path

from nose.plugins.attrib import attr
path_to_script = os.path.dirname(os.path.abspath(__file__))
import unittest

import shutil
import numpy as np

import logging
logger = logging.getLogger(__name__)


# from imtools import qmisc
# from imtools import misc


import io3d.datasets as sd
#

class SampleDataTest(unittest.TestCase):
    interactivetTest = False
    # interactivetTest = True
    def sample_data_test(self):
        sd.download("head", "delete_head")
        self.assertTrue(os.path.exists("./delete_head/matlab/examples/sample_data/DICOM/digest_article/brain_001.dcm"))
        shutil.rmtree("delete_head")


        # import imtools.vesseltree_export as vt
        # yaml_input = os.path.join(path_to_script, "vt_biodur.yaml")
        # yaml_output = os.path.join(path_to_script, "delme_esofspy.txt")
        # vt.vt2esofspy(yaml_input, yaml_output)

    @attr("slow")
    def sample_data_get_all_test(self):
        keys = sd.data_urls.keys()
        sd.download(keys, "delete_all")
        self.assertTrue(os.path.exists("./delete_all/matlab/examples/sample_data/DICOM/digest_article/brain_001.dcm"))
        shutil.rmtree("delete_all")

    def sample_data_batch_test(self):
        tmp_sample_data_path = "delete_sample_data"
        if os.path.exists(tmp_sample_data_path):
            shutil.rmtree(tmp_sample_data_path)

        sd.download(["head", "exp_small"], tmp_sample_data_path)
        self.assertTrue(os.path.exists("./delete_sample_data/exp_small/seeds/org-liver-orig003-seeds.pklz"))
        self.assertTrue(os.path.exists("./delete_sample_data/matlab/examples/sample_data/DICOM/digest_article/brain_001.dcm"))
        shutil.rmtree(tmp_sample_data_path)

    def generate_liver_test(self):
        liver = sd.generate_abdominal()

if __name__ == "__main__":
    # logging.basicConfig()
    unittest.main()
