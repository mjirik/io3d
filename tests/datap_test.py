#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import io3d

def test_extended_dict():
    datap = io3d.DataPlus()
    datap["voxelsize_mm"] = [1.,2.,3.]
    datap.voxelsize_mm[1] = 4.
    datap.update({"iii": True})
    datap.slab = {"nothing": 0, "liver": 1}
    datap.segmentation = np.zeros([5,5,5])
    datap.data3d = np.zeros([5,5,5])
    # print(f"vs attr= {datap.voxelsize_mm}")
    # print(f"vs attr= {datap['voxelsize_mm']}")
    # print(datap.keys())

    assert datap.voxelsize_mm[0] == 1.
    assert datap.voxelsize_mm[1] == 4.
    assert datap["iii"] is True
    assert datap.slab['liver'] == 1
    assert datap.data3d[0,0,0] == 0
    assert datap.segmentation[0,0,0] == 0


def test_as_datap():
    dt = {"data3d":np.zeros([3,4,5]), "voxelsize_mm":[1,2,3]}

    datap = io3d.as_datap(dt)
    assert type(datap) == io3d.DataPlus
    assert type(io3d.as_datap(datap)) == io3d.DataPlus
    assert io3d.as_datap(None) is None

