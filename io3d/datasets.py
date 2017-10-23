#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Module is used for visualization of segmentation stored in pkl file.
"""

import sys
import os.path

import logging
logger = logging.getLogger(__name__)
import scipy
import numpy as np
import glob
import os.path as op
import io3d

from . import ml
from . import qmisc

def sliver_reader(filename_end_mask="*[0-9].mhd", sliver_reference_dir="~/data/medical/orig/sliver07/training/", read_orig=True, read_seg=False):
    """
    Generator for reading sliver data from directory structure.

    :param filename_end_mask: file selection can be controlled with this parameter
    :param sliver_reference_dir: directory with sliver .mhd and .raw files
    :param read_orig: read image data if is set True
    :param read_seg: read segmentation data if is set True
    :return: numeric_label, vs_mm, oname, orig_data, rname, ref_data
    """
    sliver_reference_dir = op.expanduser(sliver_reference_dir)
    orig_fnames = glob.glob(sliver_reference_dir + "*orig" +  filename_end_mask)
    ref_fnames = glob.glob(sliver_reference_dir + "*seg"+ filename_end_mask)

    orig_fnames.sort()
    ref_fnames.sort()
    output = []
    for i in range(0, len(orig_fnames)):
        oname = orig_fnames[i]
        rname = ref_fnames[i]
        vs_mm = None
        ref_data= None
        orig_data = None
        if read_orig:
            orig_data, metadata = io3d.datareader.read(oname)
            vs_mm = metadata['voxelsize_mm']
        if read_seg:
            ref_data, metadata = io3d.datareader.read(rname)
            vs_mm = metadata['voxelsize_mm']

        import re
        numeric_label = re.search(".*g(\d+)", oname).group(1)
        out = (numeric_label, vs_mm, oname, orig_data, rname, ref_data)
        yield out


