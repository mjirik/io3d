#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
import os

import logging
logger = logging.getLogger(__name__)

import numpy as np

def ndarray_to_list_in_structure(item, squeeze=True):
    """ Change ndarray in structure of lists and dicts into lists.
    """
    tp = type(item)

    if tp == np.ndarray:
        if squeeze:
            item = item.squeeze()
        item = item.tolist()
    elif tp == list:
        for i in range(len(item)):
            item[i] = ndarray_to_list_in_structure(item[i])
    elif tp == dict:
        for lab in item:
            item[lab] = ndarray_to_list_in_structure(item[lab])

    return item
