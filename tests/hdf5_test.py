#! /usr/bin/env python
# -*- coding: utf-8 -*-


from loguru import logger
import unittest
import numpy as np
import io3d.hdf5_io as hp


class Hdf5Test(unittest.TestCase):
    def test_read_write_h5(self):
        data = {
            "x": "astring",
            "y": np.arange(10),
            "d": {"z": np.ones((2, 3)), "b": b"bytestring"},
            "none": None,
            1: 1,
            "tuple": (5, 7),
            5: None,
            "float": 3.14,
        }

        fn = "hdf5_testfile.h5"
        hp.save_dict_to_hdf5(data, fn)

        data2 = hp.load_dict_from_hdf5(fn)
        # this would raise an exception if there is something wrong
        np.testing.assert_equal(data, data2)
        self.assertEqual(data["x"], data2["x"])
        self.assertTrue(np.array_equal(data["y"], data2["y"]))
        self.assertEqual(data["d"]["b"], data2["d"]["b"])
        self.assertTrue(np.array_equal(data["d"]["z"], data2["d"]["z"]))
        self.assertEqual(data["none"], data2["none"])
        self.assertEqual(data[1], data2[1])
        self.assertEqual(type(data2["tuple"]), tuple)
        self.assertEqual(data[5], data2[5])
        self.assertEqual(type(data["float"]), type(data2["float"]))
        self.assertEqual(type(data[1]), type(data2[1]))
