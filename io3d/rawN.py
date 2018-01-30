#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
logger = logging.getLogger(__name__)
import argparse
import struct
import numpy as np
import os.path as op


def read(filename):
    return read_iv(filename)


def __iv_read_header(f):
    minX = __read_float(f)
    minY = __read_float(f)
    minZ = __read_float(f)
    maxX = __read_float(f)
    maxY = __read_float(f)
    maxZ = __read_float(f)
    numVerts = __read_uint(f)
    numCells = __read_uint(f)
    dimX = __read_uint(f)
    dimY = __read_uint(f)
    dimZ = __read_uint(f)
    originX = __read_float(f)
    originY = __read_float(f)
    originZ = __read_float(f)
    spanXorig = __read_float(f)
    spanYorig = __read_float(f)
    spanZorig = __read_float(f)

    # print(dimX * dimY * dimZ, '   ', numVerts)
    if dimX * dimY * dimZ != numVerts:
        logger.error('numVerts is not consistent with dimX, dimY, dimZ')
        print("error")

    spanX  = (maxX - minX)/(dimX -1)
    spanY  = (maxY - minY)/(dimY -1)
    spanZ  = (maxZ - minZ)/(dimZ -1)

    if spanX != spanXorig or \
            spanY != spanYorig or\
            spanZ != spanZorig:
        logger.warning('span in rawiv header is not consistent')
        print('error span')

    return minX , minY , minZ , maxX , maxY , maxZ , numVerts , numCells , dimX\
     , dimY , dimZ , originX , originY , originZ , spanX, spanY, \
     spanZ


def read_iv(filename):
    filename = op.expanduser(filename)
    with open(filename, "rb") as f:
        head = __iv_read_header(f)

        minX, minY, minZ, maxX, maxY, maxZ, numVerts, numCells, dimX,\
            dimY, dimZ, originX, originY, originZ, spanX,\
            spanY, spanZ = head
        # check



        data = f.read()
        i = 0

        print(len(data))
        print(numVerts)
        bytes_per_vertex = len(data)//numVerts

        if bytes_per_vertex == 1:
            nptype = 'uint8'
            pctype = '>B'
        elif bytes_per_vertex == 2:
            nptype = 'uint16'
            pctype = '>H'
        elif bytes_per_vertex == 4:
            nptype = 'float'
            pctype = '>f'

        data3d = np.zeros([dimX, dimY, dimZ], dtype=nptype)


        for z in range(0, dimZ):
            for y in range(0, dimY):
                for x in range(0, dimX):
                    dataraw = data[i:(i+bytes_per_vertex)]
                    data3d[x,y,z] = struct.unpack(pctype, dataraw)[0]
                    i = i + 1

        metadata = {
            'minX':      minX,
            'minY':      minY,
            'minZ':      minZ,
            'maxX':      maxX,
            'maxY':      maxY,
            'maxZ':      maxZ,
            'numVerts':  numVerts,
            'numCells':  numCells,
            'dimX':      dimX,
            'dimY':      dimY,
            'dimZ':      dimZ,
            'originX':   originX,
            'originY':   originY,
            'originZ':   originZ,
            'spanX':     spanX,
            'spanY':     spanY,
            'spanZ':     spanZ,
            'voxelsize_mm': [spanX, spanY, spanZ]
        }


    return data3d, metadata

def __read_float(f):
        data = f.read(4)
        number = struct.unpack('>f', data)
        number = number[0]
        return number


def __read_uint(f):
        data = f.read(4)
        number = struct.unpack('>I', data)
        number = number[0]
        return number


def __write_float(f, number):
        data = struct.pack('>f', number)
        f.write(data)


def __write_uint(f, number):
        data = struct.pack('>I', number)
        f.write(data)


def write(filename, data3d, metadata):
    data3d.shape[0]

    minX = 0
    minY = 0
    minZ = 0
    spanX = metadata['voxelsize_mm'][0]
    spanY = metadata['voxelsize_mm'][1]
    spanZ = metadata['voxelsize_mm'][2]
    dimX = data3d.shape[0]
    dimY = data3d.shape[1]
    dimZ = data3d.shape[2]
    numVerts = dimX * dimY * dimZ
    maxX = spanX * (dimX - 1) + minX
    maxY = spanY * (dimY - 1) + minY
    maxZ = spanZ * (dimZ - 1) + minZ
    numCells = (dimX - 1) * (dimY - 1) * (dimZ - 1)
    originX = 0
    originY = 0
    originZ = 0

    with open(filename, "wb") as f:
        __write_float(f, minX)
        __write_float(f, minY)
        __write_float(f, minZ)
        __write_float(f, maxX)
        __write_float(f, maxY)
        __write_float(f, maxZ)
        __write_uint(f, numVerts)
        __write_uint(f, numCells)
        __write_uint(f, dimX)
        __write_uint(f, dimY)
        __write_uint(f, dimZ)
        __write_float(f, originX)
        __write_float(f, originY)
        __write_float(f, originZ)
        __write_float(f, spanX)
        __write_float(f, spanY)
        __write_float(f, spanZ)

        bytes_per_vertex = 1
        pctype = '>B'

        for z in range(0, dimZ):
            for y in range(0, dimY):
                for x in range(0, dimX):
                    dataraw = struct.pack(pctype, data3d[x,y,z])
                    f.write(dataraw)

def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)



if __name__ == "__main__":
    main()
