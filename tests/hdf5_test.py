#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)
import unittest
import numpy as np
import io3d.hdf5_io as hp

class Hdf5Test(unittest.TestCase):

    def test_read_write_h5(self):
        data = {'x': 'astring',
                'y': np.arange(10),
                'd': {'z': np.ones((2, 3)),
                      'b': b'bytestring'}}

        fn = "hdf5_testfile.h5"
        hp.save_dict_to_hdf5(data, fn)

        data2 = hp.load_dict_from_hdf5(fn)
        # this would raise an exception if there is something wrong
        np.testing.assert_equal(data, data2)
        self.assertEqual(data["x"], data2["x"])
        self.assertTrue(np.array_equal(data["y"], data2["y"]))
        self.assertEqual(data["d"]["b"], data2["d"]["b"])
        self.assertTrue(np.array_equal(data["d"]["z"], data2["d"]["z"]))



