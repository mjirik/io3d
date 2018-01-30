#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Example with use of pyqt read 3d image
"""

# import funkcí z jiného adresáře
import logging
import sys

from PyQt4 import QtGui
from PyQt4.QtGui import QGridLayout, QLabel, \
    QPushButton, QLineEdit, QApplication

logger = logging.getLogger(__name__)
import argparse

from io3d.datareaderqt import DataReaderWidget

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
        '-sn', '--seriesnumber',
        default=None,
        help='seriesnumber'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    data3d, metadata = read(args.inputfile, series_number = args.seriesnumber)


def show(data3dw):
    data3d = data3dw.datap["data3d"]
    import sed3
    ed = sed3.sed3qt(data3d)
    # ed = sed3.se
    # ed.show()
    ed.exec_()

if __name__ == "__main__":
    # main()

    app = QtGui.QApplication(sys.argv)

    # w = QtGui.QWidget()
    # w = DictEdit(dictionary={'jatra':2, 'ledviny':7})
    w = DataReaderWidget(loaddir="~", loadfiledir="~",
                         cachefile="~/cache.yaml",
                         after_function=None, before_function=None)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('io3dQtWidget')
    w.show()

    app.exec_()
    data3d = w.datap["data3d"]

    import sed3
    ed = sed3.sed3(data3d)
    ed.show()
