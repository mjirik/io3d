#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import os.path

import unittest

import numpy as np
import os

import io3d

class ImageManipulationTest(unittest.TestCase):
    interactivetTest = False
    # interactivetTest = True


    def test_resize_to_shape(self):

        data = np.random.rand(3, 4, 5)
        new_shape = [5, 6, 6]
        data_out = io3d.misc.resize_to_shape(data, new_shape)
        # print data_out.shape
        # print data
        # print data_out
        self.assertEquals(new_shape[0], data_out.shape[0])
        self.assertEquals(new_shape[1], data_out.shape[1])
        self.assertEquals(new_shape[2], data_out.shape[2])

    def test_resize_to_mm(self):

        data = np.random.rand(3, 4, 6)
        voxelsize_mm = [2, 3, 1]
        new_voxelsize_mm = [1, 3, 2]
        expected_shape = [6, 4, 3]
        data_out = io3d.misc.resize_to_mm(data, voxelsize_mm, new_voxelsize_mm)
        # print(data_out.shape)
        # print data
        # print data_out
        self.assertEquals(expected_shape[0], data_out.shape[0])
        self.assertEquals(expected_shape[1], data_out.shape[1])
        self.assertEquals(expected_shape[2], data_out.shape[2])

if __name__ == "__main__":
    unittest.main()
