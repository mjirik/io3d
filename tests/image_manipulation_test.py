#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
# import funkcí z jiného adresáře
import os.path

import unittest

import numpy as np
import os

import io3d
import io3d.datasets
import imma.image_manipulation as ima

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

    def test_store_to_SparseMatrix_and_back(self):
        data = np.zeros([4, 4, 4])
        data = np.zeros([4, 4, 4])
        data[1, 0, 3] = 1
        data[2, 1, 2] = 1
        data[0, 1, 3] = 2
        data[1, 2, 0] = 1
        data[2, 1, 1] = 3

        dataSM = ima.SparseMatrix(data)

        data2 = dataSM.todense()
        self.assertTrue(np.all(data == data2))

    def test_crop_and_uncrop(self):
        shape = [10, 10, 5]
        img_in = np.random.random(shape)

        crinfo = [[2, 8], [3, 9], [2, 5]]

        img_cropped = ima.crop(img_in, crinfo)

        img_uncropped = ima.uncrop(img_cropped, crinfo, shape)

        self.assertTrue(img_uncropped[4, 4, 3] == img_in[4, 4, 3])

    def test_crop_from_specific_data(self):

        datap = io3d.datasets.generate_abdominal()
        data3d = datap["data3d"]
        segmentation = datap["segmentation"]
        crinfo_auto1 = io3d.image_manipulation.crinfo_from_specific_data(segmentation, [5])
        crinfo_auto2 = io3d.image_manipulation.crinfo_from_specific_data(segmentation, 5)
        crinfo_auto3 = io3d.image_manipulation.crinfo_from_specific_data(segmentation, [5,5, 5])

        # import sed3
        # ed = sed3.sed3(data3d, contour=segmentation)
        # ed.show()

        crinfo_expected = [[0, 99], [20, 99], [45, 99]]

        self.assertEquals(crinfo_auto1, crinfo_expected)
        self.assertEquals(crinfo_auto1, crinfo_auto2)
        self.assertEquals(crinfo_auto1, crinfo_auto3)

    def test_multiple_crop_and_uncrop(self):
        """
        test combination of multiple crop
        """

        shape = [10, 10, 5]
        img_in = np.random.random(shape)

        crinfo1 = [[2, 8], [3, 9], [2, 5]]
        crinfo2 = [[2, 5], [1, 4], [1, 2]]

        img_cropped = ima.crop(img_in, crinfo1)
        img_cropped = ima.crop(img_cropped, crinfo2)

        crinfo_combined = ima.combinecrinfo(crinfo1, crinfo2)

        img_uncropped = ima.uncrop(img_cropped, crinfo_combined, shape)

        self.assertTrue(img_uncropped[4, 4, 3] == img_in[4, 4, 3])
        self.assertEquals(img_in.shape, img_uncropped.shape)

    @unittest.skip("crinfo_combine should be tested in different way")
    def test_random_multiple_crop_and_uncrop(self):
        """
        test combination of multiple crop
        """

        shape = np.random.randint(10, 30, 3)
        # shape = [10, 10, 5]
        img_in = np.random.random(shape)

        crinfo1 = [
            sorted(np.random.randint(0, shape[0], 2)),
            sorted(np.random.randint(0, shape[1], 2)),
            sorted(np.random.randint(0, shape[2], 2))
        ]
        crinfo2 = [
            sorted(np.random.randint(0, shape[0], 2)),
            sorted(np.random.randint(0, shape[1], 2)),
            sorted(np.random.randint(0, shape[2], 2))
        ]

        img_cropped = ima.crop(img_in, crinfo1)
        img_cropped = ima.crop(img_cropped, crinfo2)

        crinfo_combined = ima.combinecrinfo(crinfo1, crinfo2)

        img_uncropped = ima.uncrop(img_cropped, crinfo_combined, shape)
        logger.debug("shape " + str(shape))
        logger.debug("crinfo_combined " + str(crinfo_combined))
        logger.debug("img_cropped.shape" + str(img_cropped.shape))
        logger.debug("img_uncropped.shape" + str(img_uncropped.shape))


        self.assertEquals(img_in.shape, img_uncropped.shape)
        # sonda indexes inside cropped area
        # cr_com = np.asarray(crinfo_combined)
        # if np.all((cr_com[:, 1] - cr_com[:, 0]) > 1):
        if np.all(img_cropped.shape > 1):
            # sometimes the combination of crinfo has zero size in one dimension
            sonda = np.array([
                np.random.randint(crinfo_combined[0][0], crinfo_combined[0][1] - 1),
                np.random.randint(crinfo_combined[1][0], crinfo_combined[1][1] - 1),
                np.random.randint(crinfo_combined[2][0], crinfo_combined[2][1] - 1),
            ])
            sonda_intensity_uncropped = img_uncropped[sonda[0], sonda[1], sonda[2]]
            sonda_intensity_in = img_in[sonda[0], sonda[1], sonda[2]]
            self.assertEquals(sonda_intensity_in, sonda_intensity_uncropped)

    def test_resize_to_shape(self):

        data = np.random.rand(3, 4, 5)
        new_shape = [5, 6, 6]
        data_out = ima.resize_to_shape(data, new_shape)
        # self.assertCountEqual(new_shape, data_out.shape)
        self.assertEqual(new_shape[0], data_out.shape[0])
        self.assertEqual(new_shape[1], data_out.shape[1])
        self.assertEqual(new_shape[2], data_out.shape[2])

    def test_resize_to_shape_no_new_unique_values(self):
        data = np.zeros([10, 15, 12])
        value1 = 1
        value2 = 2
        data[:5, :7, :6] = value1
        data[-5:, :7, :6] = value2

        expected_shape = [15, 15, 15]
        resized = ima.resize_to_shape(data, expected_shape)
        unique = np.unique(resized)

        self.assertEqual(resized.shape[0], expected_shape[0])
        self.assertEqual(resized.shape[1], expected_shape[1])
        self.assertEqual(resized.shape[2], expected_shape[2])
        self.assertEqual(resized[1, 1, 1], value1)
        self.assertEqual(resized[-2, 1, 1], value2)
        self.assertEqual(len(unique), 3)
        self.assertEqual(unique[0], 0)
        self.assertEqual(unique[1], 1)
        self.assertEqual(unique[2], 2)

    def test_fix_crinfo(self):
        crinfo = [[10, 15], [30, 40], [1, 50]]
        cri_fixed = ima.fix_crinfo(crinfo)

        # print crinfo
        # print cri_fixed

        self.assertTrue(cri_fixed[1, 1] == 40)
        self.assertTrue(cri_fixed[2, 1] == 50)

    def test_resize_to_mm(self):

        data = np.random.rand(3, 4, 5)
        voxelsize_mm = [2, 3, 1]
        new_voxelsize_mm = [1, 3, 2]
        expected_shape = [6, 4, 3]
        data_out = ima.resize_to_mm(data, voxelsize_mm, new_voxelsize_mm)
        self.assertEqual(expected_shape[0], data_out.shape[0])
        self.assertEqual(expected_shape[1], data_out.shape[1])
        self.assertEqual(expected_shape[2], data_out.shape[2])
        # self.assertCountEqual(expected_shape, data_out.shape)

    def test_simple_get_nlabel(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, 2)
        self.assertEqual(val, 2)
        self.assertEqual(len(slab), 2)

    def test_simple_string_get_nlabel(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, "porta")
        self.assertEqual(val, 2)
        self.assertEqual(len(slab), 2)

    def test_simple_new_numeric_get_nlabel(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, 7)
        self.assertNotEqual(val, 1)
        self.assertNotEqual(val, 2)
        self.assertEqual(val, 7)

    def test_simple_new_string_get_nlabel(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, "cava")
        self.assertNotEqual(val, 1)
        self.assertNotEqual(val, 2)

    def test_simple_string_get_nlabel_return_string(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, "porta", return_mode="str")
        self.assertEqual(val, "porta")

    def test_simple_numeric_get_nlabel_return_string(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabel(slab, 2, return_mode="str")
        self.assertEqual(val, "porta")

    def test_get_nlabels_single_label(self):
        slab={"liver": 1, "kindey": 15, "none":0}
        labels = 1
        val = ima.get_nlabels(slab, labels)
        self.assertEqual(val, 1)

    def test_get_nlabels_multiple(self):
        slab={"liver": 1, "porta": 2}
        val = ima.get_nlabels(slab, [2, "porta", "new", 7], return_mode="str")
        self.assertEqual(val[0], "porta")
        self.assertEqual(val[1], "porta")
        self.assertEqual(val[2], "3")
        self.assertEqual(val[3], "7")

    def test_get_nlabels_single(self):
        slab={"liver": 1, "porta": 2}

        val = ima.get_nlabels(slab, "porta", return_mode="int")
        self.assertEqual(val, 2)

    def test_get_nlabels_single_both(self):
        slab={"liver": 1, "porta": 2}

        val = ima.get_nlabels(slab, "porta", return_mode="both")
        self.assertEqual(val[0], 2)
        self.assertEqual(val[1], "porta")

    def test_select_objects_by_seeds(self):
        shape = [12, 15, 12]
        data = np.zeros(shape)
        value1 = 1
        value2 = 1
        data[:5, :7, :6] = value1
        data[-5:, :7, :6] = value2

        seeds = np.zeros(shape)
        seeds[9, 3:6, 3] = 1

        selected = ima.select_objects_by_seeds(data, seeds)
        # import sed3
        # ed =sed3.sed3(selected, contour=data, seeds=seeds)
        # ed.show()
        unique = np.unique(selected)
        #
        self.assertEqual(selected.shape[0], shape[0])
        self.assertEqual(selected.shape[1], shape[1])
        self.assertEqual(selected.shape[2], shape[2])
        self.assertEqual(selected[1, 1, 1], 0)
        self.assertEqual(selected[-2, 1, 1], 1)
        self.assertEqual(len(unique), 2)
        self.assertGreater(np.count_nonzero(data), np.count_nonzero(selected))

    def test_rotate(self):

        datap = io3d.datasets.generate_abdominal()
        data3d = datap["data3d"]
        phi_deg, theta_deg = ima.random_rotate_paramteres()
        data3d_rot = ima.rotate(data3d, phi_deg, theta_deg)
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()
        # import sed3
        # ed = sed3.sed3(data3d_rot, contour=(data3d_rot < 0))
        # ed.show()
        self.assertLessEqual(np.min(data3d), np.min(data3d_rot))
        self.assertGreaterEqual(np.max(data3d), np.max(data3d_rot))

    def test_multiple_crop_and_uncrop_nearest_outside(self):
        """
        test combination of multiple crop
        """

        shape = [10, 11, 5]
        img_in = np.random.random(shape)

        crinfo1 = [[2, 8], [3, 9], [2, 5]]
        # crinfo2 = [[2, 5], [1, 5], [1, 2]]

        img_cropped = ima.crop(img_in, crinfo1)
        # img_cropped = imma.crop(img_cropped, crinfo2)

        # crinfo_combined = imma.combinecrinfo(crinfo1, crinfo2)

        img_uncropped = ima.uncrop(img_cropped, crinfo1, shape, outside_mode="nearest")

        # import sed3
        # ed = sed3.sed3(img_uncropped)
        # ed.show()
        self.assertTrue(img_uncropped[4, 4, 3] == img_in[4, 4, 3])

        self.assertTrue(img_uncropped[crinfo1[0][0], 5, 3] == img_uncropped[0, 5, 3], msg="pixels under crop")
        self.assertTrue(img_uncropped[5, crinfo1[1][0], 3] == img_uncropped[5, 0, 3], msg="pixels under crop")
        self.assertTrue(img_uncropped[7, 3, crinfo1[2][0]] == img_uncropped[7, 3, 0], msg="pixels under crop")

        self.assertTrue(img_uncropped[crinfo1[0][1] - 1, 5, 3] == img_uncropped[-1, 5, 3], msg="pixels over crop")
        self.assertTrue(img_uncropped[5, crinfo1[1][1] - 1, 3] == img_uncropped[5, -1, 3], msg="pixels over crop")
        self.assertTrue(img_uncropped[7, 3, crinfo1[2][1] - 1] == img_uncropped[7, 3, -1], msg="pixels over crop")

        # self.assertTrue(img_uncropped[crinfo1[0][1], 5 , 3] == img_uncropped[0, 5, 3], msg="pixels over crop")
        # self.assertTrue(img_uncropped[crinfo1[1][1], 5 , 3] == img_uncropped[1, 5, 3], msg="pixels over crop")
        # self.assertTrue(img_uncropped[crinfo1[2][1], 5 , 3] == img_uncropped[2, 5, 3], msg="pixels over crop")
        self.assertEquals(img_in.shape, img_uncropped.shape)

    def test_uncrop_with_none_crinfo(self):
        shape = [10, 10, 5]
        orig_shape = [15, 13, 7]
        img_in = np.random.random(shape)

        img_uncropped = ima.uncrop(img_in, crinfo=None, orig_shape=orig_shape)

        self.assertTrue(img_uncropped[-1, -1, -1] == 0)
        self.assertTrue(img_uncropped[4, 4, 3] == img_in[4, 4, 3])


    def test_uncrop_with_start_point_crinfo(self):
        shape = [10, 10, 5]
        orig_shape = [15, 13, 7]
        img_in = np.random.random(shape)
        crinfo = [5, 2, 1]

        img_uncropped = ima.uncrop(img_in, crinfo=crinfo, orig_shape=orig_shape)

        self.assertTrue(img_uncropped[-1, -1, -1] == 0)
        self.assertTrue(img_uncropped[4 + 5, 4 + 2, 3 + 1] == img_in[4 , 4, 3])

    def test_squeeze_labels(self):
        seeds = np.zeros([50, 60, 70])
        seeds[20:30, 20:30, 20:30] = 30
        seeds[20:30, 50:70, 20:30] = 60
        seeds[20:30, 10:200, 40:60] = 61
        squeezed_seeds = io3d.image_manipulation.squeeze_labels(seeds)
        self.assertEqual(np.max(squeezed_seeds), 3)

    def test_squeeze_labels_with_negative_and_collision(self):
        seeds = np.zeros([50, 60, 70])
        seeds[20:30, 20:30, 20:30] = -10
        seeds[20:30, 50:70, 20:30] = 1
        seeds[20:30, 10:200, 40:60] = 61
        squeezed_seeds = io3d.image_manipulation.squeeze_labels(seeds)
        self.assertEqual(np.max(squeezed_seeds), 3)

    def test_dist_segmentation(self):
        seeds = np.zeros([8, 10])
        seeds[1:7, 8] = 1
        seeds[6, 5] = 2
        seeds[2, 0] = 3

        import matplotlib.pyplot as plt
        # plt.imshow(seeds, interpolation="nearest")
        # plt.show()

        segm = ima.distance_segmentation(seeds)

        # plt.imshow(segm, interpolation="nearest")
        # plt.show()

        self.assertEqual(segm[2, 2], 3)
        self.assertEqual(segm[5, 5], 2)

        # dist, inds = scipy.in


if __name__ == "__main__":
    unittest.main()
