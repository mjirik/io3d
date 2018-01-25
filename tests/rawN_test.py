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
from nose.plugins.attrib import attr
import numpy as np
import os

import io3d.rawN


class RawIOTest(unittest.TestCase):

    # @attr('interactive')
    def test_rawiv_read(self):
        # import sed3
        data3d, metadata = io3d.rawN.read('~/data/medical/orig/sample_data/ct_head.rawiv')
        # ed = sed3.sed3(data3d)
        # ed.show()
        # on this index sould be number 119
        self.assertEqual(data3d[29, 13, 27], 119)
        pass

    @attr('actual')
    def test_rawiv_write(self):
        data3d = (np.random.rand(6, 5, 4) * 10).astype(np.uint8)
        metadata = {
            'voxelsize_mm': [1, 1, 1]
        }
        filename = 'test_rawiv.rawiv'
        io3d.rawN.write(filename, data3d, metadata)

        # import sed3
        data3dout, metadataout = io3d.rawN.read(filename)
        self.assertEqual(data3d[1, 2, 3], data3dout[1, 2, 3])
        self.assertEqual(data3d[4, 2, 1], data3dout[4, 2, 1])
        self.assertEqual(data3d[4, 2, 3], data3dout[4, 2, 3])
        os.remove(filename)

        # ed = sed3.sed3(data3d)
        # ed.show()
        # on this index sould be number 119
        # self.assertEqual(data3d[29, 13, 27], 119)

if __name__ == "__main__":
    unittest.main()
