#! /usr/bin/env python
# -*- coding: utf-8 -*-

class DataPlus(dict):

    @property
    def voxelsize_mm(self):
        return self["voxelsize_mm"]

    @voxelsize_mm.setter
    def voxelsize_mm(self, voxelsize_mm):
        self["voxelsize_mm"] = voxelsize_mm

    @property
    def data3d(self):
        return self["data3d"]

    @data3d.setter
    def data3d(self, value):
        self["data3d"] = value

    @property
    def segmentation(self):
        return self["segmentation"]

    @segmentation.setter
    def segmentation(self, value):
        self["segmentation"] = value

    @property
    def slab(self):
        return self["slab"]

    @slab.setter
    def slab(self, value):
        self["slab"] = value


    # def __getattr__(self, attr):
    #     print(f"attr: {attr}")
    #     return self[attr]
    #     # KeyError
    #
    # def __setattr__(self, attr, value):
    #     print(f"attr: {attr}: {value}")
    #     self[attr] = value

def as_datap(obj):
    if type(obj) == DataPlus:
        return obj
    elif type(obj) == dict:
        return DataPlus(obj)
    elif obj is None:
        return None
    else:
        raise TypeError("Type Dict or type DataPlus expected.")