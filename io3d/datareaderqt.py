#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR%  <>
#
# Distributed under terms of the %LICENSE% license.

"""

"""

import logging

logger = logging.getLogger(__name__)
import argparse



from PyQt4.QtGui import QGridLayout, QLabel,\
    QPushButton, QLineEdit, QApplication
from PyQt4 import QtGui
import sys
import os.path
import copy


import datareader

class LoadDataWidget(QtGui.QWidget):

    def __init__(self, dictionary):
        super(LoadDataWidget, self).__init__()

        # status function can be used to proceed messages out of this module
        # it is defined fcn(str)
        self.showMessageFunction = None
        self.loadfiledir = ''
        self.loaddir = ''
        self.datapath = None
        self.afterFunction = None

        self.initUI()



    def initUI(self):
        self.mainLayout = QGridLayout(self)
        # self.mainLayout.addWidget(QLabel("Key"), 0, 1)
        # self.mainLayout.addWidget(QLabel("Value"), 0, 2)
        btnLoadFile = QPushButton("Load file", self)
        btnLoadFile.clicked.connect(self.readDataFileDialog)
        self.mainLayout.addWidget(btnLoadFile, 0, 0)

        btnLoadFile = QPushButton("Load dir", self)
        btnLoadFile.clicked.connect(self.readDataDirDialog)
        self.mainLayout.addWidget(btnLoadFile, 0, 1)

        self.text_dcm_dir = QLabel('data path:')
        self.text_dcm_data = QLabel('data description:')
        self.mainLayout.addWidget(self.text_dcm_dir, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.text_dcm_data, 2, 0, 1, 2)

    def __get_datafile(self, app=False, directory=''):
        """
        Draw a dialog for directory selection.
        """

        from PyQt4.QtGui import QFileDialog
        if app:
            dcmdir = QFileDialog.getOpenFileName(
                caption='Select Data File',
                directory=directory
                # ptions=QFileDialog.ShowDirsOnly,
            )
        else:
            app = QApplication(sys.argv)
            dcmdir = QFileDialog.getOpenFileName(
                caption='Select DICOM Folder',
                # ptions=QFileDialog.ShowDirsOnly,
                directory=directory
            )
            # pp.exec_()
            app.exit(0)
        if len(dcmdir) > 0:

            dcmdir = "%s" % (dcmdir)
            dcmdir = dcmdir.encode("utf8")
        else:
            dcmdir = None
        return dcmdir

    def __get_datadir(self, app=False, directory=''):
        """
        Draw a dialog for directory selection.
        """

        from PyQt4.QtGui import QFileDialog
        if app:
            dcmdir = QFileDialog.getExistingDirectory(
                caption='Select DICOM Folder',
                options=QFileDialog.ShowDirsOnly,
                directory=directory
            )
        else:
            app = QApplication(sys.argv)
            dcmdir = QFileDialog.getExistingDirectory(
                caption='Select DICOM Folder',
                options=QFileDialog.ShowDirsOnly,
                directory=directory
            )
            # pp.exec_()
            app.exit(0)
        if len(dcmdir) > 0:

            dcmdir = "%s" % (dcmdir)
            dcmdir = dcmdir.encode("utf8")
        else:
            dcmdir = None
        return dcmdir

    def readDataFileDialog(self):
        self.__showMessage('Reading data file...')
        QApplication.processEvents()

        self.datapath = self.__get_datafile(
            app=True,
            directory=self.loadfiledir
        )

        if self.datapath is None:
            self.__showMessage('No data path specified!')
            return
        head, teil = os.path.split(self.datapath)
        self.loadfiledir = head

        self.readDataFromPreparedDatapath()

    def readDataDirDialog(self):
        self.__showMessage('Reading data file...')
        QApplication.processEvents()


        self.datapath = self.__get_datadir(
            app=True,
            directory=self.loaddir
        )

        if self.datapath is None:
            self.__showMessage('No DICOM directory specified!')
            return
        # head, teil = os.path.split(oseg.datapath)
        self.loaddir = copy.copy(self.datapath)

        self.readDataFromPreparedDatapath()

        # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)


    def readDataFromPreparedDatapath(self):
        """
        Function is called in the end of process
        :return:
        """

        reader = datareader.DataReader()

        self.datap = reader.Get3DData(self.datapath, dataplus_format=True)


        self.__setLabelText(self.text_dcm_dir, self.__makeTextShort(self.datapath), self.datapath)
        self.__setLabelText(self.text_dcm_data, self.getDataInfo())
        if self.afterFunction is not None:
            self.afterFunction()
        self.__showMessage('Data read finished')

    def __makeTextShort(self, text, max_lenght=40):
        return text[:int(max_lenght/2)] + ".." + text[-int(max_lenght/2):]

    def __setLabelText(self, obj, text, tooltip=None):
        dlab = str(obj.text())
        obj.setText(dlab[:dlab.find(':')] + ': %s' % text)
        if tooltip is not None:
            obj.setToolTip(tooltip)

    def getDataInfo(self):
        vx_size = self.datap['voxelsize_mm']
        vsize = tuple([float(ii) for ii in vx_size])
        ret = ' %dx%dx%d,  %fx%fx%f mm' % (self.datap['data3d'].shape + vsize)

        return ret

    def __showMessage(self, msg):
        logger.debug(msg)

        if self.showMessageFunction is not None:
            self.showMessageFunction(msg)


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
    # parser.add_argument(
    #     '-i', '--inputfile',
    #     default=None,
    #     required=True,
    #     help='input file'
    # )
    parser.add_argument(
        '--dict',
        default="{'jatra':2, 'ledviny':7}",
        # required=True,
        help='input dict'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    app = QtGui.QApplication(sys.argv)

    # w = QtGui.QWidget()
    # w = DictEdit(dictionary={'jatra':2, 'ledviny':7})
    w = LoadDataWidget(dictionary=eval(args.dict))
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()