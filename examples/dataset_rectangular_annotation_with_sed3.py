#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Example with use of pyqt read 3d image
"""

import json
from loguru import logger
import itertools
import numpy as np
import matplotlib.pyplot as plt

import io3d
import sed3

ann = {}
for item in itertools.product(["sliver07", "3Dircadb1"], ["data3d"], range(1, 2)):
    print(item)
    datap1 = io3d.read_dataset(*item)
    improj = np.sum(datap1["data3d"], axis=1)
    plt.imshow(improj)
    pts = plt.ginput(n=2, show_clicks=True)
    plt.close()
    print(pts)
    ann[item] = pts
