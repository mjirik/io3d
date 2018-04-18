#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
import unittest


import numpy as np
import os


from io3d import misc

class ObjectSerializationTest(unittest.TestCase):
    interactivetTest = False
    # interactivetTest = True

    # @unittest.skip("waiting for implementation")
    def test_suggest_filename(self):
        """
        Testing some files. Not testing recursion in filenames. It is situation
        if there exist file0, file1, file2 and input file is file
        """
        filename = "mujsoubor"
        # import ipdb; ipdb.set_trace() # BREAKPOINT
        new_filename = misc.suggest_filename(filename, exists=True)
        self.assertTrue(new_filename == "mujsoubor2")

        filename = "mujsoubor112"
        new_filename = misc.suggest_filename(filename, exists=True)
        self.assertTrue(new_filename == "mujsoubor113")

        filename = "mujsoubor-2.txt"
        new_filename = misc.suggest_filename(filename, exists=True)
        self.assertTrue(new_filename == "mujsoubor-3.txt")

        filename = "mujsoubor-a24.txt"
        new_filename = misc.suggest_filename(filename, exists=False)
        self.assertTrue(new_filename == "mujsoubor-a24.txt")


    def test_obj_to_and_from_file_yaml(self):
        testdata = np.random.random([4, 4, 3])
        test_object = {'a': 1, 'data': testdata}

        filename = 'test_obj_to_and_from_file.yaml'
        misc.obj_to_file(test_object, filename, 'yaml')
        saved_object = misc.obj_from_file(filename, 'yaml')

        self.assertTrue(saved_object['a'] == 1)
        self.assertTrue(saved_object['data'][1, 1, 1] == testdata[1, 1, 1])

        os.remove(filename)

    def test_obj_to_and_from_file_yaml_with_ndarray_to_yaml(self):
        testdata = np.random.random([4, 4, 3])
        test_object = {'a': 1, 'data': testdata, "lst":[1, 2, 3]}

        filename = 'test_obj_to_and_from_file.yaml'
        misc.obj_to_file(test_object, filename, 'yaml', ndarray_to_list=True)
        saved_object = misc.obj_from_file(filename, 'yaml')

        self.assertTrue(saved_object['a'] == 1)
        self.assertTrue(saved_object['data'][1][1][1] == testdata[1, 1, 1])

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


    def test_read_python27_pickle(self):
        import io3d
        datap = io3d.read(io3d.datasets.join_path("exp_small", "seeds", "org-liver-orig003-seeds.pklz"), dataplus_format=True)
        self.assertTrue("segmentation" in datap)

if __name__ == "__main__":
    unittest.main()
