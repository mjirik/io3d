#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import os.path

import unittest

import numpy as np
import os

from io3d import misc


class MiscTest(unittest.TestCase):
    interactivetTest = False
    # interactivetTest = True

    def test_obj_to_and_from_file_yaml(self):
        testdata = np.random.random([4, 4, 3])
        test_object = {'a': 1, 'data': testdata}

        filename = 'test_obj_to_and_from_file.yaml'
        misc.obj_to_file(test_object, filename, 'yaml')
        saved_object = misc.obj_from_file(filename, 'yaml')

        self.assertTrue(saved_object['a'] == 1)
        self.assertTrue(saved_object['data'][1, 1, 1] == testdata[1, 1, 1])

        os.remove(filename)

    def test_obj_to_and_from_file_pickle(self):
        testdata = np.random.random([4, 4, 3])
        test_object = {'a': 1, 'data': testdata}

        filename = 'test_obj_to_and_from_file.pkl'
        misc.obj_to_file(test_object, filename, 'pickle')
        saved_object = misc.obj_from_file(filename, 'pickle')

        self.assertTrue(saved_object['a'] == 1)
        self.assertTrue(saved_object['data'][1, 1, 1] == testdata[1, 1, 1])

        os.remove(filename)

    # def test_obj_to_and_from_file_exeption(self):
    #    test_object = [1]
    #    filename = 'test_obj_to_and_from_file_exeption'
    #    self.assertRaises(misc.obj_to_file(test_object, filename ,'yaml'))

    def test_obj_to_and_from_file_with_directories(self):
        import shutil
        testdata = np.random.random([4, 4, 3])
        test_object = {'a': 1, 'data': testdata}

        dirname = '__test_write_and_read'
        filename = '__test_write_and_read/test_obj_to_and_from_file.pkl'

        misc.obj_to_file(test_object, filename, 'pickle')
        saved_object = misc.obj_from_file(filename, 'pickle')

        self.assertTrue(saved_object['a'] == 1)
        self.assertTrue(saved_object['data'][1, 1, 1] == testdata[1, 1, 1])

        shutil.rmtree(dirname)


if __name__ == "__main__":
    unittest.main()
