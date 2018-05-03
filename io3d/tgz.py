#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
import os

import logging
logger = logging.getLogger(__name__)

import sys
import os.path
import tarfile
import numpy as np

path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "./extern/sPickle"))


def get_tar_output_dir(fname):
    if (fname.endswith("tar.bz2")):
        fname = fname[:-8]
        return fname

def untar(fname, path=".", output_dir_by_filename=True, force_rewrite=False):
    if output_dir_by_filename:
        path= get_tar_output_dir(fname)
    if os.path.exists(path) and force_rewrite is False:
        logger.debug("Extraction of tar file interrupted. Directory %s exists" % path)
        return path

    # extraction
    if (fname.endswith("tar.bz2")):
        if path != ".":
            os.makedirs(path)
        tar = tarfile.open(fname)

        tar.extractall(path=path)
        tar.close()
        logger.debug("Extracted in " + str(path))
        return path
    else:
        logger.warning("Not a tar.bz2 file: '%s '" % path)


