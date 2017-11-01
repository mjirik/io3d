#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""
Module for testing format rawiv
"""
import logging
logger = logging.getLogger(__name__)
import unittest
import os.path as op
import shutil

import io3d


class DatasetsTest(unittest.TestCase):

    # @attr('actual')
    # @attr('interactive')
    def test_download(self):

        io3d.datasets.download("gensei_slices")
        pth = op.expanduser(op.join(io3d.datasets.local_dir, "gensei_slices"))
        logger.debug(pth)
        self.assertTrue(op.exists(pth))
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()
        # on this index sould be number 119
        # self.assertEqual(data3d[29, 13, 27], 119)
        pass

    def test_download_to_dir(self):
        pth = op.join("./tmp/", "biodur_sample")
        if op.exists(pth):
            shutil.rmtree(pth)

        io3d.datasets.download("biodur_sample", "./tmp/")
        pth = op.join("./tmp/", "biodur_sample")
        self.assertTrue(op.exists(pth))

    def test_get(self):
        io3d.datasets.get("3Dircadb1", "*1/P*")

if __name__ == "__main__":
    unittest.main()
