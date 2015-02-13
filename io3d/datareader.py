#  /usr/bin/python
# -*- coding: utf-8 -*-
""" Module for readin 3D dicom data
"""

# import funkcí z jiného adresáře
import sys
import os.path

# path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src"))
# sys.path.append(os.path.join(path_to_script,
#                              "../extern/py3DSeedEditor/"))
# ys.path.append(os.path.join(path_to_script, "../extern/"))
# mport featurevector

import logging
logger = logging.getLogger(__name__)
import argparse

# -------------------- my scripts ------------

import dcmreaddata as dcmr


# import numpy as np

def read(datapath, qt_app=None,
         dataplus_format=False, gui=False,
         start=0, stop=None, step=1, convert_to_gray=True):
    """
    Simple read function. Internally call DataReader.Get3DData()
    """
    dr = DataReader()
    return dr.Get3DData(
        datapath=datapath, qt_app=qt_app, dataplus_format=dataplus_format,
        gui=gui, start=start, stop=stop, step=step,
        convert_to_gray=convert_to_gray)


class DataReader:

    def __init__(self):

        self.overlay_fcn = None

    def Get3DData(self, datapath, qt_app=None,
                  dataplus_format=False, gui=False,
                  start=0, stop=None, step=1, convert_to_gray=True):
        """
        :datapath directory with input data
        :qt_app if it is set to None (as default) all dialogs for series
        selection are performed in terminal. If qt_app is set to
        QtGui.QApplication() dialogs are in Qt.

        :dataplus_format is new data format. Metadata and data are returned in
        one structure.
        """

        if qt_app is None and gui is True:
            from PyQt4.QtGui import QApplication
            qt_app = QApplication(sys.argv)

        datapath = os.path.normpath(datapath)
        if os.path.isfile(datapath):
            logger.debug('file read recognized')
            data3d, metadata = self.__ReadFromFile(datapath)

        elif os.path.exists(datapath):
            logger.debug('directory read recognized')
            # print "read from directory"
            data3d, metadata = self.__ReadFromDirectory(
                datapath, start, stop, step)
        else:
            logger.error('Data path "%s" not found' % (datapath))

        if convert_to_gray:
            if len(data3d.shape) > 3:
                # @TODO implement better rgb2gray
                data3d = data3d[:, :, :, 0]

        if dataplus_format:
            logger.debug('dataplus format')
            # metadata = {'voxelsize_mm': [1, 1, 1]}
            datap = metadata
            datap['data3d'] = data3d
            logger.debug('datap keys () : ' + str(datap.keys()))
            return datap
        else:
            return data3d, metadata

    def __ReadFromDirectory(self, datapath, start, stop, step):
        if dcmr.is_dicom_dir(datapath):  # reading dicom
            logger.debug('Dir - DICOM')
            reader = dcmr.DicomReader(datapath, qt_app=None, gui=True)
            data3d = reader.get_3Ddata(start, stop, step)
            metadata = reader.get_metaData()
            metadata['series_number'] = reader.series_number
            metadata['datadir'] = datapath
            self.overlay_fcn = reader.get_overlay
        else:  # reading image sequence
            import SimpleITK as sitk
            logger.debug('Dir - Image sequence')

            logger.debug('Getting list of readable files...')
            flist = []
            for f in os.listdir(datapath):
                try:
                    sitk.ReadImage(os.path.join(datapath, f))
                except:
                    logger.warning("Cant load file: " + str(f))
                    continue
                flist.append(os.path.join(datapath, f))
            flist.sort()

            logger.debug('Reading image data...')
            image = sitk.ReadImage(flist)
            logger.debug('Getting numpy array from image data...')
            data3d = sitk.GetArrayFromImage(image)

            metadata = {}  # reader.get_metaData()
            metadata['series_number'] = 0  # reader.series_number
            metadata['datadir'] = datapath
            spacing = image.GetSpacing()
            metadata['voxelsize_mm'] = [
                spacing[2],
                spacing[0],
                spacing[1],
            ]

        return data3d, metadata

    def __ReadFromFile(self, datapath):
        path, ext = os.path.splitext(datapath)
        ext = ext[1:]
        if ext in ('pklz', 'pkl'):
            logger.debug('pklz format detected')
            import misc
            data = misc.obj_from_file(datapath, filetype='pkl')
            data3d = data.pop('data3d')
            # etadata must have series_number
            metadata = {
                'series_number': 0,
                'datadir': datapath
            }
            metadata.update(data)

        elif ext in ['hdf5']:
            data = self.read_hdf5(datapath)
            data3d = data.pop('data3d')
            # etadata must have series_number
            metadata = {
                'series_number': 0,
                'datadir': datapath
            }
            metadata.update(data)
            data3d = data.pop('data3d')
            # etadata must have series_number
            metadata = {
                'series_number': 0,
                'datadir': datapath
            }
            metadata.update(data)

        else:
            logger.debug('file format "' + ext + '"')
            # reading raw file
            import SimpleITK as sitk
            image = sitk.ReadImage(datapath)
            # mage =
            # sitk.ReadImage('/home/mjirik/data/medical/data_orig/sliver07/01/liver-orig001.mhd') #  noqa
            # z = image.GetSize()

            # ata3d = sitk.Image(sz[0],sz[1],sz[2], sitk.sitkInt16)

            # or i in range(0,sz[0]):
            #    print i
            #    for j in range(0,sz[1]):
            #        for k in range(0,sz[2]):
            #            data3d[i,j,k]=image[i,j,k]

            data3d = sitk.GetArrayFromImage(image)  # + 1024
            # ata3d = np.transpose(data3d)
            # ata3d = np.rollaxis(data3d,1)
            metadata = {}  # reader.get_metaData()
            metadata['series_number'] = 0  # reader.series_number
            metadata['datadir'] = datapath
            spacing = image.GetSpacing()
            metadata['voxelsize_mm'] = [
                spacing[2],
                spacing[0],
                spacing[1],
            ]
        return data3d, metadata

    def read_hdf5(self, datapath):
        """
        Method is not implemented
        """
# TODO implement this better, this is not working

        import h5py
        f = h5py.File(datapath, 'r')
        import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
        datap = {}
        for item in f.attrs.keys():
            datap[item] = f.attrs['item']
        f.close()
        return datap

    def GetOverlay(self):
        """ Generates dictionary of ovelays
        """

        if self.overlay_fcn == None:  # noqa
            return {}
        else:
            return self.overlay_fcn()


def get_datapath_qt(qt_app):
    # just call function from dcmr
    return dcmr.get_datapath_qt(qt_app)


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

    data3d, metadata = read(args.inputfile)

    import sed3
    ed = sed3.sed3(data3d)
    ed.show()


if __name__ == "__main__":
    main()
