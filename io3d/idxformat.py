#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as op

import glob
import numpy as np
import logging
logger = logging.getLogger(__name__)
import sed3

class IDXReader:
    def _init__(self):
        pass

    def read(self, datapath):
        datapath = op.expanduser(datapath)
        data3d = np.zeros([10, 10, 10])
        metadata = {}
        header = self.header_file_parser(datapath)
        self.header = header
        self.read_files(datapath)
        return data3d, metadata

    def read_files(self, datapath):


        datapath = op.expanduser(datapath)

        dirp, filename = op.split(datapath)
        fn_template = op.join(dirp, self.header['filename_template'])

        fn_template = fn_template.replace("%04x", "????")
        filelist = glob.glob(fn_template.strip())
        filelist = sorted(filelist)
        print("sdfa")
        for fl in filelist:
            self.read_bin_file(fl, bitsperblock=int(self.header['bitsperblock']))
            pass

    def read_bin_file(self, filename, bitsperblock=8):
        bytesperblock = bitsperblock / 8
        if bytesperblock == 2:
            dtype = np.uint16
        else:
            logger.error("Unknown data type")

        data = np.fromfile(filename, dtype=np.uint8)
        shape = [1024, 1024, 10]
        d3 = np.reshape(data[:np.prod(shape)],shape)

        ed = sed3.sed3(d3[:200, :200, :])
        ed.show()
        print("all ok")


        # with open(filename, 'rb') as f:	# Use file to refer to the file object
        #
        #     data = f.read(bytesperblock)
        #


    def header_file_parser(self, datapath):
        self.file_keys = [
            'filename_template',
            'logic_to_physic',
            'bitsperblock',
            'blocksperfile',
            'interleave block',
            'box',
            'bits'
        ]
        if op.exists(datapath):
            logger.error("File '%s' not found" % (datapath))

        with open(datapath, 'rt') as f:	# Use file to refer to the file object
            data = f.readlines()
            # data = file.read()
            # print(data)

        out = {}
        for n, line in enumerate(data):
            line = data[n]
            for key in self.file_keys:
                if line.find("(" + key + ")") >= 0:
                    out[key] = data[n + 1]
        return out

class IDXWriter:
    def _init__(self):
        pass
