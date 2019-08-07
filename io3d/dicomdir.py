#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
DICOM reader

Example:

$ dcmreaddata -d sample_data -o head.mat
"""

from loguru import logger
import os
import re
import sys
import traceback
from optparse import OptionParser

try:
    import pydicom
except ImportError:
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom as pydicom
    logger.debug("dicom imported - it would be better use pydicom")
# except ModuleNotFoundError:

import numpy as np
from pathlib import Path


class Dicomdir:
    def __init__(self, dirpath):
        """

        :param dirpath: Path to directory with dicom files
        """
        self.dirpath = Path(dirpath)
        if self.dirpath.exists():
            pass
        # dirpath / "jmenosouboru.dcm"

    def create_dicomdir(self):
        pass
