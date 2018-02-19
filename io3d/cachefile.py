#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@hp-mjirik>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
logger = logging.getLogger(__name__)
import argparse
import os.path as op
from . import misc


class CacheFile():
    def __init__(self, filename):
        """

        :param filename: File can be .yaml, .pkl or some other formats supported by misc.obj_from_file
        """
        self.filename = op.expanduser(filename)
        self.__update()

    def __update(self):
        if op.exists(self.filename):
            self.data = misc.obj_from_file(self.filename)
        else:
            self.data = {}

    def get(self, key):
        self.__update()
        return self.data[key]

    def get_or_none(self, key):
        self.__update()
        if key in self.data.keys():
            return self.data[key]
        else:
            return None

    def get_or_save_default(self, key, default_value):
        """
        Get value stored in cache file or store there default value.
        :param key:
        :param default_value:
        :return:
        """
        val = self.get_or_none(key)
        if val is None:
            self.update(key, default_value)
            val = default_value
        return val

    def update(self, key, value):
        self.data[key] = value
        misc.obj_to_file(self.data, self.filename)


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
