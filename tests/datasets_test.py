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
from loguru import logger

logger.enable("io3d")
import unittest
import os.path as op
import shutil
import sys
import numpy as np
import io3d
import io3d.network
import os
import datetime

# from pathlib import Path

import pytest


class DatasetsTest(unittest.TestCase):

    # @attr('actual')
    # @attr('interactive')
    def test_get_path(self):
        path = op.join(io3d.datasets.dataset_path(get_root=True), "medical", "orig")
        self.assertEqual(type(path), str)

    def test_expand_dataset_package(self):
        dataset_labels = ["lisa"]
        new_dataset_labels = io3d.datasets._expand_dataset_packages(dataset_labels)
        assert len(dataset_labels) <= len(new_dataset_labels)

    def test_download_package_dry_run(self):
        logger.debug("download in progress")
        io3d.datasets.download("lisa", dry_run=True)

    def test_download(self):

        dirs = io3d.datasets.download("gensei_slices")
        pth = io3d.datasets.join_path("medical", "orig", "gensei_slices", get_root=True)
        logger.debug(pth)
        self.assertTrue(op.exists(pth))
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()
        # on this index sould be number 119
        # self.assertEqual(data3d[29, 13, 27], 119)
        pass

    def test_download_to_dir(self):
        pth = op.join("./tests_tmp_outputs", "medical", "orig", "biodur_sample")
        if op.exists(pth):
            shutil.rmtree(pth)

        odirs = io3d.datasets.download("biodur_sample", "./tests_tmp_outputs")
        # pth = op.join("./tests_tmp_outputs", "medical", "orig", "biodur_sample")
        logger.debug(odirs)
        # import ipdb; ipdb.set_trace()
        self.assertTrue(op.exists(pth))

    def test_change_dataset_path(self):
        dp_new1 = "~/io3d_test1_dataset_dir/"
        dp_new2 = "~/io3d_test2_dataset_dir/"
        dp_old = io3d.datasets.join_path(get_root=True)

        # change once
        io3d.datasets.set_dataset_path(dp_new1)
        dp_joined1 = io3d.datasets.join_path("jatra_5mm")
        self.assertTrue(dp_joined1.find("io3d_test1_dataset_dir") > 0)

        # second change
        io3d.datasets.set_dataset_path(dp_new2)
        dp_joined2 = io3d.datasets.join_path("jatra_5mm")
        self.assertTrue(dp_joined2.find("io3d_test2_dataset_dir") > 0)

        # return path back
        io3d.datasets.set_dataset_path(dp_old)

    def test_change_dataset_path_with_windows_full_path(self):
        dp_new1 = "c:/io3d_test1_dataset_dir/"
        dp_new2 = "c:/io3d_test2_dataset_dir/"
        dp_old = io3d.datasets.join_path(get_root=True)

        # change once
        io3d.datasets.set_dataset_path(dp_new1)
        dp_joined1 = io3d.datasets.join_path("jatra_5mm")
        self.assertTrue(dp_joined1.find("io3d_test1_dataset_dir") > 0)

        # second change
        io3d.datasets.set_dataset_path(dp_new2)
        dp_joined2 = io3d.datasets.join_path("jatra_5mm")
        self.assertTrue(dp_joined2.find("io3d_test2_dataset_dir") > 0)

        # return path back
        io3d.datasets.set_dataset_path(dp_old)

    @pytest.mark.slow
    def test_getold1(self):
        io3d.datasets.download("3Dircadb1.1")
        # io3d.datasets.get_old("3Dircadb1", "*1/P*")

    def test_getold1(self):
        io3d.datasets.download(
            "http://home.zcu.cz/~mjirik/lisa/sample_data/biodur_sample.zip:test_biodur_sample/"
        )

    def test_getold(self):
        pth = io3d.datasets.join_path(
            "medical",
            "orig",
            "sample_data",
            "SCP003",
            "SCP003.ndpi.ndpa",
            get_root=True,
        )
        if op.exists(pth):
            import os

            os.remove(pth)
        io3d.datasets.download("SCP003-ndpa")
        self.assertTrue(op.exists(pth))

    @unittest.skip("waiting for implementation of get() function")
    def test_get_no_series_number(self):

        datap = io3d.datasets.get("jatra_5mm")
        self.assertEqual(datap["data3d"].shape[1], 512)

    @unittest.skip("waiting for implementation of get() function")
    def test_get_with_series_number(self):
        # remove data if they are stored
        shutil.rmtree(io3d.daatsets.join("path_where_the_data_are_usualy_stored"))

        # first read
        datap = io3d.datasets.get("3Dircadb1", 3)
        self.assertEqual(datap["data3d"].shape[1], 512)

        # second read should be faster
        datap = io3d.datasets.get("3Dircadb1", 3)
        self.assertEqual(datap["data3d"].shape[1], 512)

    def test_main_list_labels(self):
        tmpargv = sys.argv
        sys.argv = [tmpargv[0], "-L"]
        io3d.datasets.main()
        sys.argv = tmpargv

    def test_main_get_dataset_path(self):

        tmpargv = sys.argv
        sys.argv = [tmpargv[0], "-gdp"]
        io3d.datasets.main()
        sys.argv = tmpargv

    def test_main_get_dataset_multiple_labels(self):

        tmpargv = sys.argv
        sys.argv = [tmpargv[0], "-l", "jatra_5mm", "head", "-l", "exp", "--dry_run"]
        io3d.datasets.main()
        sys.argv = tmpargv

    def test_generate_round_data(self):
        img, segm, seeds = io3d.datasets.generate_round_data(43)

        self.assertTrue(np.array_equal([43, 44, 45], img.shape))

    def test_generate_face_2d(self):
        img = io3d.datasets.generate_face()

        self.assertTrue(np.array_equal([32, 32], img.shape))
        self.assertEqual(img[0, 0], False, "In the corner should be False")
        self.assertEqual(img[15, 15], True, "In the middle of face should be True")

    def test_generate_face_3d(self):
        img = io3d.datasets.generate_face([5, 42, 34])

        self.assertTrue(np.array_equal([5, 42, 34], img.shape))
        self.assertEqual(img[2, 0, 0], False, "In the corner should be False")
        self.assertEqual(img[2, 21, 17], True, "In the middle of face should be True")

    def test_generate_donut(self):
        datap = io3d.datasets.generate_donut()
        data3d = datap["data3d"]
        segmentation = datap["segmentation"]

        # self.assertTrue(np.array_equal([5, 42, 34], data3d.shape))
        self.assertEqual(segmentation[2, 0, 0], False, "In the corner should be False")
        self.assertTrue(
            np.array_equal(np.unique(segmentation), [0, 1, 2]),
            "Three labels in output segmentation",
        )

    def test_generate_synghetic_liver(self):
        (
            data3d,
            segm,
            voxelsize_mm,
            slab,
            seeds_liver,
            seeds_porta,
        ) = io3d.datasets.generate_synthetic_liver()

        self.assertTrue(np.array_equal(data3d.shape, segm.shape))
        self.assertTrue(np.array_equal(data3d.shape, seeds_porta.shape))
        self.assertTrue(np.array_equal(data3d.shape, seeds_liver.shape))
        self.assertEqual(np.max(segm), 2, "Maximum label is 2")

    def test_get_metadata_from_url(self):

        __url_server = ""

        url_and_path = "http://home.zcu.cz/~mjirik/lisa/sample_data/biodur_sample.zip:biodur_sample/*.tiff"
        metadata = io3d.datasets.get_dataset_meta(url_and_path)
        assert metadata[0].startswith("http:")
        assert metadata[2] == "."
        assert metadata[3] == "biodur_sample/*.tiff"

        url_and_path = "http://home.zcu.cz/~mjirik/lisa/sample_data/biodur_sample.zip"
        metadata = io3d.datasets.get_dataset_meta(url_and_path)
        assert metadata[0].startswith("http:")
        assert metadata[2] == "."
        assert metadata[3] == ""

        # # "biodur_sample": [
        #     "d459dd5b308ca07d10414b3a3a9000ea",
        #     "biodur_sample/*.tiff"
        # ],


def test_dataset_csv():
    key = "J7_5_b"
    if key in io3d.datasets.data_urls:
        # this is applied if the url was added before by calling _update_... from other test.
        del io3d.datasets.data_urls[key]
    assert key not in io3d.datasets.data_urls
    io3d.datasets._update_datasets_url()
    assert key in io3d.datasets.data_urls


def test_read_dataset_ircad_data3d():
    datap = io3d.datasets.read_dataset("3Dircadb1", "data3d", 1)
    assert datap["data3d"].shape[1] == 512


def test_read_dataset_ircad_bone():
    datap = io3d.datasets.read_dataset("3Dircadb1", "bone", 1)
    assert datap["data3d"].shape[1] == 512


# @unittest.skip("sliver is not available")
skip_on_local = False


@unittest.skipIf(os.environ.get("TRAVIS", skip_on_local), "Skip on Travis-CI")
def test_read_dataset_sliver():
    datap = io3d.datasets.read_dataset("sliver07", "data3d", 1)
    assert datap["data3d"].shape[1] == 512


def test_read_dataset_example():
    # import matplotlib.pyplot as plt
    datap1 = io3d.read_dataset("3Dircadb1", "data3d", 1)
    datap2 = io3d.read_dataset("3Dircadb1", "bone", 1)
    # plt.imshow(datap1["data3d"][20, :, :], cmap="gray")
    # plt.contour(datap2["data3d"][20, :, :])
    # plt.title(datap1["voxelsize_mm"])
    # plt.show()
    assert datap2["data3d"].shape[0] == datap1["data3d"].shape[0]


def test_read_url():
    """
    Open file from url. If file is already downloaded, just open it.
    :return:
    """
    __url_server = "http://home.zcu.cz/~mjirik/lisa/"
    url = __url_server + "sample_data/nrn4.pklz"
    fn = io3d.network.get_filename(url)
    if fn.exists():
        fn.unlink()

    t0 = datetime.datetime.now()
    datap = io3d.read(url)
    t1 = datetime.datetime.now() - t0
    assert fn.exists()
    assert datap.data3d.shape[0] > 0

    # second r
    t0 = datetime.datetime.now()
    datap = io3d.read(url)
    t2 = datetime.datetime.now() - t0

    assert t2 < t1, "Second run should be faster"


if __name__ == "__main__":
    unittest.main()
