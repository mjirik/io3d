#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
DICOM reader

Example:

$ dcmreaddata -d sample_data -o head.mat
"""

import logging
import os
import re
import sys
import traceback
from optparse import OptionParser

try:
    import dicom
except:
    import pydicom as dicom

import numpy as np
import scipy
import scipy.io
from scipy.io import savemat
import os.path as op

logger = logging.getLogger(__name__)
from . import misc

# compatibility between python 2 and 3
if sys.version_info[0] >= 3:
    xrange = range
    raw_input = input

__version__ = [1, 4]


# def obj_from_file(filename='annotation.yaml', filetype='yaml'):
#     """
#     Read object from file
#     """
#     if filetype == 'yaml':
#         import yaml
#         f = open(filename, 'r')
#         obj = yaml.load(f)
#     elif filetype == 'pickle':
#         import pickle
#         f = open(filename, 'rb')
#         obj = pickle.load(f)
#     else:
#         logger.error('Unknown filetype')
#
#     f.close()
#
#     return obj
#
#
# def obj_to_file(obj, filename='annotation.yaml', filetype='yaml'):
#     """
#     Writes annotation in file
#     """
#     if filetype == 'yaml':
#         import yaml
#         f = open(filename, 'w')
#         yaml.dump(obj, f)
#     elif filetype == 'pickle':
#         import pickle
#         f = open(filename, 'wb')
#         pickle.dump(obj, f, -1)
#     else:
#         logger.error('Unknown filetype')
#
#     f.close
def dicomdir_info(dirpath, *args, **kwargs):
    """ Get information about series in dir"""
    dr = DicomReader(dirpath=dirpath, *args, **kwargs)
    info = dr.dicomdirectory.dcmdirstats()
    return info

def is_dicom_dir(datapath):
    """
    Check if in dir is one or more dicom file. We use two methods.
    First is based on dcm extension detection.
    """
    # Second tries open files
    # with dicom module.

    retval = False
    datapath = op.expanduser(datapath)
    for f in os.listdir(datapath):
        if f.endswith((".dcm", ".DCM")):
            retval = True
            return True
# @todo not working and I dont know why
        try:
            dicom.read_file(os.path.join(datapath, f))

            retval = True
        except:
            import traceback
            traceback.print_exc

        if retval:
            return True
    return False


class DicomReader():
    """
    Example:

    dcr = DicomReader(os.path.abspath(dcmdir))
    data3d = dcr.get_3Ddata()
    metadata = dcr.get_metaData()

    """

    def __init__(self, dirpath=None, initdir='.',
                 qt_app=None, gui=True, series_number=None,
                 get_series_number_callback=None,
                 force_create_dicomdir=False,
                 force_read=False
                 ):
        self.valid = False
        self.dirpath = os.path.expanduser(dirpath)
        self.dicomdirectory = DicomDirectory(self.dirpath, force_create_dicomdir=force_create_dicomdir, force_read=force_read)
        self.force_read = force_read
        # self.dicomdir_info = self.dicomdirectory.get_dicomdir_info()
        self.series_number = series_number
        self.overlay = {}
        self.files_in_serie = []
        self.files_in_serie_with_info = []
        self.qt_app = qt_app
        if get_series_number_callback is None:
            if (qt_app is not None) or gui:
                get_series_number_callback = get_series_number_qt
            else:
                get_series_number_callback = get_series_number_console

        self.get_series_number_callback = get_series_number_callback
        self.__check_series_number()
        self.set_series_number(self.series_number)

        # if self.series_number is not None:
        # else:
    def set_series_number(self, series_number):
        self.files_in_serie, self.files_in_serie_with_info = self.dicomdirectory.get_sorted_series_files(
            SeriesNumber=series_number, return_files_with_info=True)
        if len(self.files_in_serie) == 0:
            # logger.exception("No data for series number {} in directory {}".format(series_number, dirpath))
            raise ValueError("No data for series number {} in directory {}".format(self.series_number, self.dirpath))

    def __check_series_number(self):
        if self.series_number is not None:
            # self.series_number = sn
            pass
        elif len(self.dicomdirectory.files_with_info) > 0:
            self.valid = True
            counts, bins = self.dicomdirectory.series_in_dir()

            if len(bins) > 1:
                if self.series_number is None:  # pragma: no cover
                    self.series_number = self.get_series_number_callback(
                        self,
                        counts,
                        bins,
                        qt_app=self.qt_app
                    )

            else:
                self.series_number = bins[0]

    def dcmdirstats(self):
        return self.dicomdirectory.dcmdirstats()

    def print_series_info(self, *argw, **kwargs):
        return self.dicomdirectory.print_series_info(*argw, **kwargs)

    def validData(self):
        return self.valid

    def get_4d(self):
        #TODO create reading time series
        pass

    def get_overlay(self):
        """
        Function make 3D data from dicom file slices. There are usualy
        more overlays in the data.
        """
        overlay = {}
        dcmlist = self.files_in_serie

        for i in range(len(dcmlist)):
            onefile = dcmlist[i]
            logger.info("reading '%s'" % onefile)
            data = self._read_file(onefile)

            if len(overlay) == 0:
                # first there is created dictionary with
                # avalible overlay indexes
                for i_overlay in range(0, 50):
                    try:
                        # overlay index
                        data2d = self.decode_overlay_slice(data, i_overlay)
                        # mport pdb; pdb.set_trace()
                        shp2 = data2d.shape
                        overlay[i_overlay] = np.zeros([len(dcmlist), shp2[0],
                                                      shp2[1]], dtype=np.int8)
                        overlay[i_overlay][-i - 1, :, :] = data2d

                    except:
                        # exception is exceptetd. We are trying numbers 0-50
                        # logger.exception('Problem with overlay image number ' +
                        #               str(i_overlay))
                        pass

            else:
                for i_overlay in overlay.keys():
                    try:
                        data2d = self.decode_overlay_slice(data, i_overlay)
                        overlay[i_overlay][-i - 1, :, :] = data2d
                    except:
                        logger.warning('Problem with overlay number ' +
                                       str(i_overlay))

        return overlay

    def decode_overlay_slice(self, data, i_overlay):
            # overlay index
            n_bits = 8

            # On (60xx,3000) are stored ovelays.
            # First is (6000,3000), second (6002,3000), third (6004,3000),
            # and so on.
            dicom_tag1 = 0x6000 + 2 * i_overlay

            overlay_raw = data[dicom_tag1, 0x3000].value

            # On (60xx,0010) and (60xx,0011) is stored overlay size
            rows = data[dicom_tag1, 0x0010].value  # rows = 512
            cols = data[dicom_tag1, 0x0011].value  # cols = 512

            decoded_linear = np.zeros(len(overlay_raw) * n_bits)

            # Decoding data. Each bit is stored as array element
# TODO neni tady ta jednička blbě?
            for i in range(1, len(overlay_raw)):
                for k in range(0, n_bits):
                    # Python2 returns str, Python3 returns int. (Could also by caused by slight difference in dicom lib version number)
                    byte_as_int = ord(overlay_raw[i]) if type(overlay_raw[i]) == type(str("")) else overlay_raw[i]
                    decoded_linear[i * n_bits + k] = (byte_as_int >> k) & 0b1

            # verlay = np.array(pol)
            overlay_slice = np.reshape(decoded_linear, [rows, cols])
            return overlay_slice

    def _read_file(self, dcmfile):
        data = dicom.read_file(dcmfile, force=self.force_read)
        return data

    def get_3Ddata(self, start=0, stop=None, step=1):
        """
        Function make 3D data from dicom file slices
        """
        data3d = []
        dcmlist = self.files_in_serie
        # print('stsp ', start, stop, step)

        raw_max = None
        raw_min = None
        slope = None
        inter = None

        # get shape 2d

        # sometimes there is render in series
        if len(self.files_in_serie) > 1:
            data = self._read_file(dcmlist[0])
            data2d1 = data.pixel_array
            data = self._read_file(dcmlist[1])
            data2d2 = data.pixel_array
            if (data2d1.shape[0] == data2d2.shape[0]) and (data2d1.shape[1] == data2d2.shape[1]):
                pass
            else:
                dcmlist.pop(0)

        if stop is None:
            stop = len(dcmlist)


        printRescaleWarning = False
        for i in xrange(start, stop, step):
            onefile = dcmlist[i]
            data = self._read_file(onefile)
            data2d = data.pixel_array
            # mport pdb; pdb.set_trace()

            if len(data3d) == 0:
                shp2 = data2d.shape
                data3d = np.zeros([len(dcmlist), shp2[0], shp2[1]],
                                  dtype=np.int16)
                mx = np.max(data2d)
                mn = np.min(data2d)
                if (raw_max is None) or (raw_max < mx):
                    raw_max = mx
                if (raw_min is None) or (raw_min < mx):
                    raw_min = mn

            # if hasattr(data, "RescaleSlope") and hasattr(data, "RescaleIntercept") and\
            #         data3d.dtype == np.int16 and\
            #         (data2d.max() > np.iinfo(np.int16).max or data2d.min() < np.iinfo(np.int16).min):
            #     data3d = data3d.astype(np.int32)

            if hasattr(data, "RescaleSlope") and hasattr(data, "RescaleIntercept"):
                slope = data.RescaleSlope
                inter = data.RescaleIntercept
            else:
                slope = 1
                inter = 0

            if data2d.dtype == np.uint16 and data3d.dtype == np.int16:
                data3d = data3d.astype(np.int32)
                # or just force set slope=0.5, inter = 0

            new_data2d = (np.float(slope) * data2d) \
                         + np.float(inter)
            # first readed slide is at the end

            if (data3d.shape[1] == new_data2d.shape[0]) and (data3d.shape[2] == new_data2d.shape[1]) :
                data3d[-i - 1, :, :] = new_data2d
            else:
                msg = "Problem with shape " +\
                      "Data size: " + str(data3d.nbytes) +\
                      ', shape: ' + str(shp2) + 'x' + str(len(dcmlist)) +\
                      ' file ' + onefile
                logger.warning(msg)
                print(msg)

            logger.debug("Data size: " + str(data3d.nbytes)
                         + ', shape: ' + str(shp2) + 'x' + str(len(dcmlist))
                         + ' file ' + onefile)
        if printRescaleWarning:
            print("Automatic Rescale with slope 0.5")
            logger.warning("Automatic Rescale with slope 0.5")

        return data3d

    def get_metaData(self, ifile=0):
        dcmlist = self.files_in_serie
        # self.dicomdirectory.get_metadata_new(series_number=self.series_number)
        return self.dicomdirectory.get_metaData(dcmlist=dcmlist, series_number=self.series_number, ifile=ifile)
        #
        # if len(dcmlist) == 0:
        #     return {}


        # logger.debug("Filename: " + dcmlist[ifile])

    def dcmdirstats(self):
        return self.dicomdirectory.dcmdirstats()

class DicomDirectory():
    def __init__(self, dirpath, force_create_dicomdir=False, force_read=False):
        self.dicomdir_filename = 'dicomdir.pkl'
        self.files_with_info = None
        self.dcmdirplus = None
        self.dirpath = dirpath
        self.force_read = force_read
        self.force_create_dicomdir = force_create_dicomdir
        self.__prepare_info_from_dicomdir_file()

    def _read_file(self, dcmfile):
        data = dicom.read_file(dcmfile, force=self.force_read)
        return data

    # def get_depth
    def get_metadata_new(self, series_number):
        #@ TODO implement simplier metadata function
        files, files_with_info = self.get_sorted_series_files(SeriesNumber=series_number, return_files_with_info=True)
        print("asdf")

    def get_metaData(self, dcmlist, series_number, ifile=0):
        """
        Get metadata.
        Voxel size is obtained from PixelSpacing and difference of
        SliceLocation of two neighboorhoding slices (first have index ifile).
        Files in are used.
        """
        # if dcmlist is None:
        #     dcmlist = self.files_in_serie

        if len(dcmlist) == 0:
            return {}

        logger.debug("Filename: " + dcmlist[ifile])
        data1 = self._read_file(dcmlist[ifile])
        try:
            head1, teil1 = os.path.split(dcmlist[ifile])
            head2, teil2 = os.path.split(dcmlist[ifile + 1])

            data2 = self._read_file(dcmlist[ifile + 1])
            loc1 = get_slice_location(data1, teil1)
            loc2 = get_slice_location(data2, teil2)
            voxeldepth = float(np.abs(loc1 - loc2))
        except:
            logger.warning('Problem with voxel depth. Using SliceThickness')
            logger.debug(traceback.format_exc())
            # + ' SeriesNumber: ' + str(data1.SeriesNumber))

            try:
                voxeldepth = float(data1.SliceThickness)
            except:
                logger.warning('Probem with SliceThicknes, setting zero. '
                               + traceback.format_exc())
                voxeldepth = 0

        try:
            pixelsize_mm = data1.PixelSpacing
        except:
            logger.warning('Problem with PixelSpacing. Using [1,1]')
            pixelsize_mm = [1, 1]
        voxelsize_mm = [
            voxeldepth,
            float(pixelsize_mm[0]),
            float(pixelsize_mm[1]),
        ]
        metadata = {'voxelsize_mm': voxelsize_mm,
                    'Modality': data1.Modality,
                    'SeriesNumber': series_number
                    }

        try:
            metadata['SeriesDescription'] = data1.SeriesDescription

        except:
            logger.warning(
                'Problem with tag SeriesDescription, SeriesNumber: ' +
                str(data1.SeriesNumber))
        try:
            metadata['ImageComments'] = data1.ImageComments
        except:
            logger.warning(
                'Problem with tag ImageComments')
            # , SeriesNumber: ' +
            # str(data1.SeriesNumber))
        try:
            metadata['Modality'] = data1.Modality
        except:
            logger.warning(
                'Problem with tag Modality')
            # SeriesNumber: ' +
            #     str(data1.SeriesNumber))
        metadata = attr_to_dict(data1, "AcquisitionDate", metadata)
        metadata = attr_to_dict(data1, "StudyDate", metadata)
        metadata = attr_to_dict(data1, "StudyDescription", metadata)
        metadata = attr_to_dict(data1, "RequestedProcedureDescription", metadata)

        metadata['dcmfilelist'] = dcmlist
        return metadata

    def dcmdirstats(self):
        """ Dicom series staticstics, input is dcmdir, not dirpath
        Information is generated from dicomdir.pkl and first files of series
        """
        import numpy as np
        dcmdir = self.files_with_info
        # get series number
        # vytvoření slovníku, kde je klíčem číslo série a hodnotou jsou všechny
        # informace z dicomdir
        series_info = {line['SeriesNumber']: line for line in dcmdir}

        # počítání velikosti série
        try:
            dcmdirseries = [line['SeriesNumber'] for line in dcmdir]

        except:
            logger.debug('Dicom tag SeriesNumber not found')
            series_info = {0: {'Count': 0}}
            return series_info
            # eturn [0],[0]

        bins = np.unique(dcmdirseries)
        binslist = bins.tolist()
        #  kvůli správným intervalům mezi biny je nutno jeden přidat na konce
        mxb = np.max(bins) + 1
        binslist.append(mxb)
        # inslist.insert(0,-1)
        counts, binsvyhodit = np.histogram(dcmdirseries, bins=binslist)

        # db.set_trace();

        # sestavení informace o velikosti série a slovníku

        for i in range(0, len(bins)):
            series_info[bins[i]]['Count'] = counts[i]

            # adding information from files
            lst = self.get_sorted_series_files(SeriesNumber=bins[i])
            metadata = self.get_metaData(dcmlist=lst, series_number=bins[i])
            # adding dictionary metadata to series_info dictionary
            series_info[bins[i]] = dict(
                list(series_info[bins[i]].items()) +
                list(metadata.items())
            )

        return series_info

    def get_one_serie_info(self, series_info, serie_number):
        strl = str(serie_number) + " (" \
               + str(series_info[serie_number]['Count'])
        try:
            strl = strl + ", " \
                   + str(series_info[serie_number]['Modality'])
            strl = strl + ", " \
                   + str(series_info[serie_number]['SeriesDescription'])
            strl = strl + ", " \
                   + str(series_info[serie_number]['ImageComments'])
        except:
            logger.debug(
                'Tag Modality, SeriesDescription or ImageComment not found in dcminfo'
            )
            pass
        strl = strl + ')'
        return strl


    def print_series_info(self, series_info, minimal_series_number=1):
        """
        Print series_info from dcmdirstats
        """
        strinfo = ''
        if len(series_info) > minimal_series_number:
            for serie_number in series_info.keys():
                strl = self.get_one_serie_info(series_info, serie_number)
                strinfo = strinfo + strl + '\n'
                # rint strl

        return strinfo

    def get_study_info(self, series_info=None):
        if series_info is None:
            series_info = self.dcmdirstats()

        study_info={

        }
        key = series_info.keys()[0]
        if "StudyDate" in series_info[key]:
            study_info["StudyDate"] = series_info[key]["StudyDate"]
        return study_info

    def get_study_info_msg(self, series_info=None):
        study_info = self.get_study_info(series_info=series_info)

        study_info_msg = ""
        if "StudyDate" in study_info:
            study_info_msg += "StudyDate " + str(study_info["StudyDate"])

        return study_info_msg


    def files_in_dir(self, dirpath, wildcard="*", startpath=None):
        """
        Function generates list of files from specific dir

        files_in_dir(dirpath, wildcard="*.*", startpath=None)

        dirpath: required directory
        wilcard: mask for files
        startpath: start for relative path

        Example
        files_in_dir('medical/jatra-kiv','*.dcm', '~/data/')
        """

        import glob

        filelist = []

        if startpath is not None:
            completedirpath = os.path.join(startpath, dirpath)
        else:
            completedirpath = dirpath

        if os.path.exists(completedirpath):
            logger.info('completedirpath = ' + completedirpath)

        else:
            logger.error('Wrong path: ' + completedirpath)
            raise Exception('Wrong path : ' + completedirpath)

        for infile in glob.glob(os.path.join(completedirpath, wildcard)):
            filelist.append(infile)

        if len(filelist) == 0:
            logger.error('No required files in path: ' + completedirpath)
            raise Exception('No required file in path: ' + completedirpath)

        return filelist

    def __prepare_info_from_dicomdir_file(self, writedicomdirfile=True):
        """
        Check if exists dicomdir file and load it or cerate it

        dcmdir = get_dir(dirpath)

        dcmdir: list with filenames, SeriesNumber and SliceLocation
        """
        createdcmdir = True

        dicomdirfile = os.path.join(self.dirpath, self.dicomdir_filename)
        ftype = 'pickle'
        # if exist dicomdir file and is in correct version, use it
        if os.path.exists(dicomdirfile):
            try:
                dcmdirplus = misc.obj_from_file(dicomdirfile, ftype)
                if dcmdirplus['version'] == __version__:
                    createdcmdir = False
                dcmdir = dcmdirplus['filesinfo']
            except:
                logger.debug('Found dicomdir.pkl with wrong version')
                pass

        if createdcmdir or self.force_create_dicomdir:
            dcmdirplus = self._create_dicomdir_info()
            dcmdir = dcmdirplus['filesinfo']
            if (writedicomdirfile) and len(dcmdir) > 0:
                # obj_to_file(dcmdirplus, dicomdirfile, ftype)
                try:
                    misc.obj_to_file(dcmdirplus, dicomdirfile, ftype)
                except:
                    logger.warning('Cannot write dcmdir file')
                    traceback.print_exc()

                # bj_to_file(dcmdir, dcmdiryamlpath )

        dcmdir = dcmdirplus['filesinfo']
        self.dcmdirplus = dcmdirplus
        self.files_with_info = dcmdir
        return dcmdir


    def _prepare_metadata_line(self, dcmdata, teil):

        metadataline = {'filename': teil,
                        'SeriesNumber': get_series_number(
                            dcmdata),
                        'SliceLocation': get_slice_location(
                            dcmdata, teil)
                        }
        return metadataline

    def series_in_dir(self):
        """input is dcmdir, not dirpath """

        try:
            dcmdirseries = [line['SeriesNumber'] for line in self.files_with_info]
        except:
            # @TODO maybe [0],[None] would be better
            return [0], [0]

        bins = np.unique(dcmdirseries)
        binslist = bins.tolist()
        #  kvůli správným intervalům mezi biny je nutno jeden přidat na konce
        mxb = np.max(bins) + 1
        binslist.append(mxb)
        counts, binsvyhodit = np.histogram(dcmdirseries, bins=binslist)

        return counts, bins

    def get_sorted_series_files(self, startpath="", SeriesNumber=None, return_files_with_info=False):
        """
        Function returns sorted list of dicom files. File paths are organized
        by SeriesUID, StudyUID and FrameUID

        Example:
        get_sortedlist()
        get_sortedlist('~/data/')
        """
        dcmdir = self.files_with_info[:]
        dcmdir.sort(key=lambda x: x['SliceLocation'])

        # select sublist with SeriesNumber
        if SeriesNumber is not None:
            dcmdir = [
                line for line in dcmdir if line['SeriesNumber'] == SeriesNumber
            ]

        logger.debug('SeriesNumber: ' + str(SeriesNumber))

        filelist = []
        for onefile in dcmdir:
            filelist.append(os.path.join(startpath,
                                         self.dirpath, onefile['filename']))
            # head, tail = os.path.split(onefile['filename'])

        if return_files_with_info:
            return filelist, dcmdir
        else:
            return filelist


    def _create_dicomdir_info(self):
        """
        Function crates list of all files in dicom dir with all IDs
        """

        filelist = self.files_in_dir(self.dirpath)
        files = []
        metadataline = {}

        for filepath in filelist:
            head, teil = os.path.split(filepath)
            dcmdata = None
            try:
                dcmdata = dicom.read_file(filepath)

            except dicom.errors.InvalidDicomError as e:
                # some files doesnt have DICM marker
                try:
                    dcmdata = dicom.read_file(filepath, force=self.force_read)

                    # if e.[0].startswith("File is missing \\'DICM\\' marker. Use force=True to force reading")
                except Exception as e:
                    if teil != self.dicomdir_filename:
                        print('Dicom read problem with file ' + filepath)
                    import traceback
                    logger.debug(traceback.format_exc())
            if hasattr(dcmdata, "DirectoryRecordSequence"):
                # file is DICOMDIR - metainfo about files in directory
                # we are not using this info
                dcmdata = None

            if dcmdata is not None:
                metadataline = self._prepare_metadata_line(dcmdata, teil)
                files.append(metadataline)


        files.sort(key=lambda x: x['SliceLocation'])

        dcmdirplus = {'version': __version__, 'filesinfo': files, }
        if "StudyDate" in metadataline:
            dcmdirplus["StudyDate"] = metadataline["StudyDate"]
        return dcmdirplus

def get_slice_location(dcmdata, teil=None):
    """ get location of the slice

    :param dcmdata: dicom data structure
    :param teil: filename. Used when slice location doesnt exist
    :return:
    """
    slice_location=None
    if hasattr(dcmdata, 'SliceLocation'):
        # print(dcmdata.SliceLocation)
        # print(type(dcmdata.SliceLocation))
        try:
            slice_location = float(dcmdata.SliceLocation)
        except Exception as exc:
            logger.warning("It is not possible to use SliceLocation")
            logger.info(traceback.format_exc())
    if slice_location is None and hasattr(dcmdata, "SliceThickness") and teil is not None:
        logger.warning(
            "Estimating SliceLocation wiht image number and SliceThickness"
        )
        # print(teil)

        i = map(int, re.findall('\d+', teil))
        i = i[-1]
        slice_location = float(i * float(dcmdata.SliceThickness))

    if slice_location is None and hasattr(dcmdata, "ImagePositionPatient") and hasattr(dcmdata, "ImageOrientationPatient"):
        if dcmdata.ImageOrientationPatient == [1, 0, 0, 0, 1, 0]:
            slice_location = dcmdata.ImagePositionPatient[2]
        else:
            logger.warning("Unknown ImageOrientationPatient")
    if slice_location is None:
        logger.warning("Problem with slice location")

    return slice_location

def get_series_number(dcmdata):

    series_number = 0
    if hasattr(dcmdata, 'SeriesNumber') and dcmdata.SeriesNumber != '':
        series_number = dcmdata.SeriesNumber
        return series_number



def attr_to_dict(obj, attr, dct):
    """
    Add attribute to dict if it exists.
    :param obj: object
    :param attr: object attribute name
    :param dict:  output dict
    :return:  dict
    """
    if hasattr(obj, attr):
        dct[attr] = getattr(obj, attr)
    return dct

def get_series_number_console(dcmreader, counts, bins, qt_app=None): # pragma: no cover

    print('series')
    series_info = dcmreader.dcmdirstats()
    print(dcmreader.print_series_info(series_info))
    snstring = raw_input('Select Serie: ')

    sn = int(snstring)
    return sn

def get_series_number_qt(dcmreader, counts, bins, qt_app=None): # pragma: no cover

    if qt_app is None:

        # @TODO  there is problem with type of qappliaction
        # mport PyQt4
        # rom PyQt4.QtGui import QApplication
        # t_app = QApplication(sys.argv)
        # t_app = PyQt4.QtGui.QWidget(sys.argv)
        print(qt_app)

    series_info = dcmreader.dicomdirectory.dcmdirstats()
    study_info_msg = dcmreader.dicomdirectory.get_study_info_msg(series_info=series_info)
    print(dcmreader.print_series_info(series_info))
    from PyQt4.QtGui import QInputDialog
    # bins = ', '.join([str(ii) for ii in bins])
    sbins = [str(ii) for ii in bins]
    sbinsd = {}
    for serie_number in series_info.keys():
        strl = dcmreader.dicomdirectory.get_one_serie_info(series_info, serie_number)
        sbinsd[strl] = serie_number
        # sbins.append(str(ii) + "  " + serie_number)
    sbins = sbinsd.keys()
    snstring, ok = \
        QInputDialog.getItem(qt_app,
                             'Serie Selection',
                             study_info_msg +
                             ' Select serie:',
                             sbins,
                             editable=False)
    sn = sbinsd[str(snstring)]
    return sn

def get_dcmdir_qt(app=False, directory=''): # pragma: no cover
    from PyQt4.QtGui import QFileDialog, QApplication
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


usage = '%prog [options]\n' + __doc__.rstrip()
help = {
    'dcm_dir': 'DICOM data direcotory',
    'out_file': 'store the output matrix to the file',
    "degrad": "degradation of input data. For no degradation use 1",
    'debug': 'Print debug info',
    'zoom': 'Resize input data wit defined zoom. Use zoom 0.5 to obtain half\
voxels. Various zoom can be used for each axis: -z [1,0.5,2.5]'
}

if __name__ == "__main__":  # pragma: no cover
    parser = OptionParser(description='Read DIOCOM data.')
    parser.add_option('-i', '--dcmdir', action='store',
                      dest='dcmdir', default=None,
                      help=help['dcm_dir'])
    parser.add_option('-o', '--outputfile', action='store',
                      dest='out_filename', default='output.mat',
                      help=help['out_file'])
    parser.add_option('--degrad', action='store',
                      dest='degrad', default=1,
                      help=help['degrad'])
    parser.add_option('-z', '--zoom', action='store',
                      dest='zoom', default='1',
                      help=help['zoom'])
    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug',
                      help=help['debug'])
    (options, args) = parser.parse_args()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    if options.debug:
        logger.setLevel(logging.DEBUG)

    if options.dcmdir is None:
        dcmdir = get_dcmdir_qt()
        if dcmdir is None:
            raise IOError('No DICOM directory!')
    else:
        dcmdir = options.dcmdir

    dcr = DicomReader(os.path.abspath(dcmdir), gui=True)
    data3d = dcr.get_3Ddata()
    metadata = dcr.get_metaData()

    zoom = eval(options.zoom)
    if options.zoom != 1:
        import scipy
        import scipy.ndimage
        # oom = float(options.zoom)
        # mport pdb; pdb.set_trace()
        data3d = scipy.ndimage.zoom(data3d, zoom=zoom)
        metadata['voxelsize_mm'] = list(np.array(metadata['voxelsize_mm']) /
                                        zoom)

    degrad = int(options.degrad)

    data3d_out = data3d[::degrad, ::degrad, ::degrad]
    vs_out = list(np.array(metadata['voxelsize_mm']) * degrad)

    logger.debug('voxelsize_mm ' + vs_out.__str__())
    savemat(options.out_filename,
            {'data': data3d_out, 'voxelsize_mm': vs_out}
            )
    print("Data size: %d, shape: %s" % (data3d_out.nbytes, data3d_out.shape))
