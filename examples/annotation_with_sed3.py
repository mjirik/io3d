#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Module is used for visualization of segmentation stored in pkl, dcm and other files.
"""

from loguru import logger
import io3d
import sed3
import numpy as np

pth = io3d.datasets.join_path("medical", "orig", "3Dircadb1.1", "PATIENT_DICOM", get_root=True)
datap = io3d.read(pth)
# pth = io3d.datasets.join_path("medical", "orig", "3Dircadb1.1", "LABELLED_DICOM" , get_root=True)
pth = io3d.datasets.join_path("medical", "orig", "3Dircadb1.1", "MASKS_DICOM", "liver", get_root=True)
datap_labeled = io3d.read(pth)
ed = sed3.sed3(datap["data3d"], contour=datap_labeled["data3d"])
ed.show()

ed.seeds
nz = np.nonzero(ed.seeds == 1)
print(np.unique(nz[0]))
nz = np.nonzero(ed.seeds == 2)
print(np.unique(nz[0]))
nz = np.nonzero(ed.seeds == 3)
print(np.unique(nz[0]))



pth = io3d.datasets.join_path("medical", "orig", "3Dircadb1.1", "MASKS_DICOM", "liver", get_root=True)
datap = io3d.read(pth)
ed = sed3.sed3(datap["data3d"])
ed.show()

nz_liver = np.nonzero(datap["data3d"])
print(np.unique(nz_liver[0]))
print(f"first slide with the liver: {np.min(np.unique(nz_liver[0]))}")
print(f"last slide with the liver: {np.max(np.unique(nz_liver[0]))}")





