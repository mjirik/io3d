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
    import dicom as pydicom
except Exception:
# except ModuleNotFoundError:
    import pydicom

import numpy as np
from scipy.io import savemat
import os.path as op

logger = logging.getLogger(__name__)
from . import misc
from . import dcmtools

# compatibility between python 2 and 3
if sys.version_info[0] >= 3:
    xrange = range
    raw_input = input

__version__ = [1, 6]


def dicomdir_info(dirpath, *args, **kwargs):
    """ Get information about series in dir"""
    dr = DicomReader(dirpath=dirpath, *args, **kwargs)
    info = dr.dicomdirectory.get_stats_of_series_in_dir()
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
            pydicom.read_file(os.path.join(datapath, f))

            retval = True
        # except pydicom.errors.InvalidDicomError:
        #     logger.debug("Invalid Dicom while reading file " + str(f))
        except Exception as e:
            logger.warning("Unable to read dicom file " + str(f))
            logger.warning(e)
            # import traceback
            # traceback.print_exc()

        if retval:
            return True
    return False


def decode_overlay_slice(data, i_overlay):
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
            # NOTE: Python2 returns str, Python3 returns int.
            #       Could be by caused by slight difference in dicom lib version number.
            one_byte = overlay_raw[i]
            if sys.version_info.major == 2:
                byte_as_int = ord(one_byte)
            else:
                byte_as_int = one_byte
            # byte_as_int = ord(overlay_raw[i]) if type(overlay_raw[i]) == type(str("")) else overlay_raw[i]
            decoded_linear[i * n_bits + k] = (byte_as_int >> k) & 0b1

    # verlay = np.array(pol)
    overlay_slice = np.reshape(decoded_linear, [rows, cols])
    return overlay_slice


class DicomReader:
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
        self.dicomdirectory = DicomDirectory(self.dirpath, force_create_dicomdir=force_create_dicomdir,
                                             force_read=force_read)
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
            series_number=series_number, return_files_with_info=True)
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
        return self.dicomdirectory.get_stats_of_series_in_dir()

    def print_series_info(self, *argw, **kwargs):
        return self.dicomdirectory.print_series_info(*argw, **kwargs)

    def validData(self):
        return self.valid

    def get_4d(self):
        # TODO create reading time series
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
                        data2d = decode_overlay_slice(data, i_overlay)
                        # mport pdb; pdb.set_trace()
                        shp2 = data2d.shape
                        overlay[i_overlay] = np.zeros([len(dcmlist), shp2[0],
                                                       shp2[1]], dtype=np.int8)
                        overlay[i_overlay][-i - 1, :, :] = data2d

                    except Exception:
                        # exception is exceptetd. We are trying numbers 0-50
                        # logger.exception('Problem with overlay image number ' +
                        #               str(i_overlay))
                        pass

            else:
                for i_overlay in overlay.keys():
                    try:
                        data2d = decode_overlay_slice(data, i_overlay)
                        overlay[i_overlay][-i - 1, :, :] = data2d
                    except Exception:
                        logger.warning('Problem with overlay number ' +
                                       str(i_overlay))

        return overlay

    def _read_file(self, dcmfile):
        data = pydicom.read_file(dcmfile, force=self.force_read)
        return data

    def get_3Ddata(self, start=0, stop=None, step=1):
        """
        Function make 3D data from dicom file slices
        """
        data3d = []
        dcmlist = self.files_in_serie
        # print('stsp ', start, stop, step)

        # raw_max = None
        # raw_min = None
        # slope = None
        # inter = None

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

        # printRescaleWarning = False
        for i in xrange(start, stop, step):
            onefile = dcmlist[i]
            data = self._read_file(onefile)
            new_data2d = data.pixel_array
            # new_data2d, slope, inter = dcmtools.get_pixel_array_from_pdcm(data)
            # mport pdb; pdb.set_trace()

            if len(data3d) == 0:
                shp2 = new_data2d.shape
                data3d = np.zeros([len(dcmlist), shp2[0], shp2[1]],
                                  dtype=new_data2d.dtype)
                slope, inter = dcmtools.get_slope_and_intercept_from_pdcm(data)



            # first readed slide is at the end

            if (data3d.shape[1] == new_data2d.shape[0]) and (data3d.shape[2] == new_data2d.shape[1]):
                data3d[-i - 1, :, :] = new_data2d
            else:
                msg = "Problem with shape " + \
                      "Data size: " + str(data3d.nbytes) + \
                      ', shape: ' + str(shp2) + 'x' + str(len(dcmlist)) + \
                      ' file ' + onefile
                logger.warning(msg)
                print(msg)

            logger.debug("Data size: " + str(data3d.nbytes)
                         + ', shape: ' + str(shp2) + 'x' + str(len(dcmlist))
                         + ' file ' + onefile)
        data3d = misc.use_economic_dtype(data3d, slope=slope, inter=inter)
        # if original_dtype == np.uint16 and data3d.dtype == np.int16:
        #     data3d = data3d.astype(np.int32)
            # or just force set slope=0.5, inter = 0
        # new_data2d = rescale_pixel_array(data2d, slope, inter)
        # if printRescaleWarning:
        #     print("Automatic Rescale with slope 0.5")
        #     logger.warning("Automatic Rescale with slope 0.5")
        # data3d = dcmtools.rescale_pixel_array(data3d, slope=slope, inter=inter)

        return data3d

    def get_metaData(self):
        dcmlist = self.files_in_serie
        # self.dicomdirectory.get_metadata_new(series_number=self.series_number)
        return self.dicomdirectory.get_metaData(dcmlist=dcmlist, series_number=self.series_number)

    def dcmdirstats(self):
        return self.dicomdirectory.get_stats_of_series_in_dir()


def get_one_serie_info(series_info, serie_number):
    strl = str(serie_number) + " (" \
           + str(series_info[serie_number]['Count'])
    try:
        strl = strl + ", " \
               + str(series_info[serie_number]['Modality'])
        strl = strl + ", " \
               + str(series_info[serie_number]['SeriesDescription'])
        strl = strl + ", " \
               + str(series_info[serie_number]['ImageComments'])
    except Exception:
        logger.debug(
            'Tag Modality, SeriesDescription or ImageComment not found in dcminfo'
        )
        pass
    strl = strl + ')'
    return strl


def files_in_dir(dirpath, wildcard="*", startpath=None):
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


def _prepare_metadata_line(dcmdata, teil):
    metadataline = {'filename': teil,
                    'SeriesNumber': get_series_number(
                        dcmdata),
                    'SliceLocation': get_slice_location(
                        dcmdata, teil)
                    }
    metadataline = attr_to_dict(dcmdata, "AcquisitionTime", metadataline)
    return metadataline


class DicomDirectory:
    def __init__(self, dirpath, force_create_dicomdir=False, force_read=False):
        self.dicomdir_filename = 'dicomdir.pkl'
        self.standard_dicomdir_filename = 'DICOMDIR'
        self.files_with_info = None
        self.dcmdirplus = None
        self.dirpath = dirpath
        self.force_read = force_read
        self.force_create_dicomdir = force_create_dicomdir
        self.__prepare_info_from_dicomdir_file()

    def _read_file(self, dcmfile):
        data = pydicom.read_file(dcmfile, force=self.force_read)
        return data

    def create_standard_dicomdir(self):
        """
        Create standard dicom dir describing files in directory.
        See read_standard_dicomdir_info() and get_standard_dicomdir_info()
        :return:
        """
        # Sample DICOMDIR file can be found here
        # filepath = pydicom.data.get_testdata_files('DICOMDIR')[0]

        pass

    def read_standard_dicomdir_info(self):
        """
        Read standard DICOMDIR file
        :return:
        """
        # self.dirpath
        # os.path.join(self.dirpath, self.standard_dicomdir_filename)

        pass

    def get_standard_dicomdir_info(self):
        """
        Read DICOMDIR, crate if necessary.
        :return:
        """
        dicomdir_filepath = os.path.join(self.dirpath, self.standard_dicomdir_filename)
        if not os.path.exists(dicomdir_filepath):
            self.create_standard_dicomdir()
        return self.read_standard_dicomdir_info()

    # def get_depth
    def get_metadata_new(self, series_number):
        """
        Return series metadata.
        Output condatin information about voxelsize_mm, series_number and modality.
        If it is possible, the ImageComment, AcquisitionDate and few other dicom tags are also in output dict.
        :param series_number:
        :return: metadata dict with voxelsize_mm, SeriesNumber and other dicom tags
        """
        # TODO implement simplier metadata function
        # automatic test is prepared

        files, files_with_info = self.get_sorted_series_files(series_number=series_number, return_files_with_info=True)
        metadata = {
            # 'voxelsize_mm': voxelsize_mm,
            # 'Modality': data1.Modality,
            # 'SeriesNumber': series_number,
            # 'SeriesDescription' = data1.SeriesDescription,
            # 'ImageComments' : data1.ImageComments,
            # "AcquisitionDate": metadata,
            # "StudyDate": metadata,
            # "StudyDescription": metadata,
            # "RequestedProcedureDescription", metadata
        }
        return metadata

    def _get_slice_location_difference(self, dcmlist, ifile, step=1):
        head1, teil1 = os.path.split(dcmlist[ifile])
        head2, teil2 = os.path.split(dcmlist[ifile + step])

        data1 = self._read_file(dcmlist[ifile])
        data2 = self._read_file(dcmlist[ifile + step])
        loc1 = get_slice_location(data1, teil1)
        loc2 = get_slice_location(data2, teil2)
        voxeldepth = float(np.abs(loc1 - loc2))
        return voxeldepth

    def get_metaData(self, dcmlist, series_number):
        """
        Get metadata.
        Voxel size is obtained from PixelSpacing and difference of
        SliceLocation of two neighboorhoding slices (first have index ifile).
        Files in are used.
        """
        # if dcmlist is None:
        #     dcmlist = self.files_in_serie

        # number of slice where to extract metadata inforamtion
        ifile = 0
        if len(dcmlist) == 0:
            return {}

        logger.debug("Filename: " + dcmlist[ifile])
        data1 = self._read_file(dcmlist[ifile])
        try:
            # try to get difference from the beginning and also from the end
            voxeldepth = self._get_slice_location_difference(dcmlist, ifile)
            voxeldepth_end = self._get_slice_location_difference(dcmlist, -2)
            if voxeldepth != voxeldepth_end:
                logger.warning("Depth of slices is not the same in beginning and end of the sequence")
                voxeldepth_1 = self._get_slice_location_difference(dcmlist, 1)
                voxeldepth = np.median([voxeldepth, voxeldepth_end, voxeldepth_1])



            # head1, teil1 = os.path.split(dcmlist[ifile])
            # head2, teil2 = os.path.split(dcmlist[ifile + 1])
            #
            # data2 = self._read_file(dcmlist[ifile + 1])
            # loc1 = get_slice_location(data1, teil1)
            # loc2 = get_slice_location(data2, teil2)
            # voxeldepth = float(np.abs(loc1 - loc2))
        except Exception:
            logger.warning('Problem with voxel depth. Using SliceThickness')
            logger.debug(traceback.format_exc())
            # + ' SeriesNumber: ' + str(data1.SeriesNumber))

            try:
                voxeldepth = float(data1.SliceThickness)
            except Exception:
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
            logger.info(
                'Problem with tag SeriesDescription, SeriesNumber: ' +
                str(data1.SeriesNumber))
        try:
            metadata['ImageComments'] = data1.ImageComments
        except:
            logger.info(
                'Problem with tag ImageComments')
            # , SeriesNumber: ' +
            # str(data1.SeriesNumber))
        try:
            metadata['Modality'] = data1.Modality
        except:
            logger.info(
                'Problem with tag Modality')
            # SeriesNumber: ' +
            #     str(data1.SeriesNumber))
        metadata = attr_to_dict(data1, "AcquisitionDate", metadata)
        metadata = attr_to_dict(data1, "StudyDate", metadata)
        metadata = attr_to_dict(data1, "StudyID", metadata)
        metadata = attr_to_dict(data1, "StudyDescription", metadata)
        metadata = attr_to_dict(data1, "RequestedProcedureDescription", metadata)
        # metadata = attr_to_dict(data1, "AcquisitionTime", metadata)

        metadata['dcmfilelist'] = dcmlist
        return metadata

    def get_stats_of_studies_and_series_in_dir(self):
        retval = {
            1: {
                "info": None,
                "series": self.get_stats_of_series_in_dir()
            }
        }
        return retval

    def get_stats_of_series_in_dir_as_dataframe(self, study_id=None):
        series_stats = self.get_stats_of_series_in_dir(study_id)
        import pandas as pd
        study_df = pd.DataFrame(series_stats).transpose()
        return study_df

    def get_stats_of_series_in_dir(self, study_id=None):
        """ Dicom series staticstics, input is dcmdir, not dirpath
        Information is generated from dicomdir.pkl and first files of series
        """
        if study_id is not None:
            logger.error("study_id tag is not implemented yet")
            return
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

        bins, counts = np.unique(dcmdirseries, return_counts=True)

        # sestavení informace o velikosti série a slovníku

        for i in range(0, len(bins)):
            series_info[bins[i]]['Count'] = counts[i]

            # adding information from files
            lst = self.get_sorted_series_files(series_number=bins[i])
            metadata = self.get_metaData(dcmlist=lst, series_number=bins[i])
            # adding dictionary metadata to series_info dictionary
            series_info[bins[i]] = dict(
                list(series_info[bins[i]].items()) +
                list(metadata.items())
            )

        return series_info

    def print_series_info(self, series_info, minimal_series_number=1):
        """
        Print series_info from dcmdirstats
        """
        strinfo = ''
        if len(series_info) > minimal_series_number:
            for serie_number in series_info.keys():
                strl = get_one_serie_info(series_info, serie_number)
                strinfo = strinfo + strl + '\n'
                # rint strl

        return strinfo

    def get_study_info(self, series_info=None):
        if series_info is None:
            series_info = self.get_stats_of_series_in_dir()

        study_info = {

        }
        key = list(series_info)[0]
        if "StudyDate" in series_info[key]:
            study_info["StudyDate"] = series_info[key]["StudyDate"]
        return study_info

    def get_study_info_msg(self, series_info=None):
        study_info = self.get_study_info(series_info=series_info)

        study_info_msg = ""
        if "StudyDate" in study_info:
            study_info_msg += "StudyDate " + str(study_info["StudyDate"])

        return study_info_msg

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
            except Exception:
                logger.debug('Found dicomdir.pkl with wrong version')
                createdcmdir = True

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

    def series_in_dir(self):
        """input is dcmdir, not dirpath """

        # none_count = 0
        countsd = {}
        # dcmdirseries = []
        for line in self.files_with_info:
            if "SeriesNumber" in line:
                sn = line['SeriesNumber']
            else:
                sn = None
            if sn in countsd:
                countsd[sn] += 1
            else:
                countsd[sn] = 1

        bins = list(countsd)
        counts = list(countsd.values())


        # try:
        #     dcmdirseries = [line['SeriesNumber'] for line in self.files_with_info]
        # except:
        #     return [0], [0]

        # bins, counts = np.unique(dcmdirseries, return_counts=True)
        # binslist = bins.tolist()

        # if None in binslist:
        #     if len(binslist) == 1:
        #         return [0], [0]
        #     else:
        #         logger.warning

        #  kvůli správným intervalům mezi biny je nutno jeden přidat na konce
        # mxb = np.max(bins)
        # if mxb is None:
        #     mxb = 1
        # else:
        #     mxb = mxb + 1
        #
        # binslist.append(mxb)
        # counts, binsvyhodit = np.histogram(dcmdirseries, bins=binslist)

        # return counts.tolist(), bins.tolist()
        return counts, bins

    def get_sorted_series_files(self, startpath="", series_number=None, return_files_with_info=False,
                                sort_keys="SliceLocation", return_files=True, remove_doubled_slice_locations=True):
        """
        Function returns sorted list of dicom files. File paths are organized
        by SeriesUID, StudyUID and FrameUID


        :param startpath: path prefix. E.g. "~/data"
        :param series_number: ID of series used for filtering the data
        :param return_files_with_info: return more complex information about sorted files
        :param return_files: return simple list of sorted files
        :type sort_keys: One key or list of keys used for sorting method by the order of keys.

        """
        dcmdir = self.files_with_info[:]

        # select sublist with SeriesNumber
        if series_number is not None:
            dcmdir = [
                line for line in dcmdir if line['SeriesNumber'] == series_number
            ]
        dcmdir = sort_list_of_dicts(dcmdir, keys=sort_keys)

        logger.debug('SeriesNumber: ' + str(series_number))

        if remove_doubled_slice_locations:
            dcmdir = self._remove_doubled_slice_locations(dcmdir)

        filelist = []
        for onefile in dcmdir:
            filelist.append(os.path.join(startpath,
                                         self.dirpath, onefile['filename']))
            # head, tail = os.path.split(onefile['filename'])


        retval = []
        if return_files:
            retval.append(filelist)
        if return_files_with_info:
            retval.append(dcmdir)

        if len(retval) == 0:
            retval = None
        elif len(retval) == 1:
            retval = retval[0]
        else:
            retval = tuple(retval)

        return retval

    def _remove_doubled_slice_locations(self, dcmdir):
        new_dcmdir = []
        prev_slice_location = None
        for item in dcmdir:
            actual_slice_location = item["SliceLocation"]
            if  actual_slice_location != prev_slice_location:
                new_dcmdir.append(item)
            prev_slice_location = actual_slice_location

        return new_dcmdir

    def _create_dicomdir_info(self):
        """
        Function crates list of all files in dicom dir with all IDs
        """

        filelist = files_in_dir(self.dirpath)
        files = []
        metadataline = {}

        for filepath in filelist:
            head, teil = os.path.split(filepath)
            dcmdata = None
            if os.path.isdir(filepath):
                logger.debug("Subdirectory found in series dir is ignored: " + str(filepath))
                continue
            try:
                dcmdata = pydicom.read_file(filepath)

            except pydicom.errors.InvalidDicomError as e:
                # some files doesnt have DICM marker
                try:
                    dcmdata = pydicom.read_file(filepath, force=self.force_read)

                    # if e.[0].startswith("File is missing \\'DICM\\' marker. Use force=True to force reading")
                except Exception as e:
                    if teil != self.dicomdir_filename:
                        # print('Dicom read problem with file ' + filepath)
                        logger.info('Dicom read problem with file ' + filepath)
                        import traceback
                        logger.debug(traceback.format_exc())
            if hasattr(dcmdata, "DirectoryRecordSequence"):
                # file is DICOMDIR - metainfo about files in directory
                # we are not using this info
                dcmdata = None

            if dcmdata is not None:
                metadataline = _prepare_metadata_line(dcmdata, teil)
                files.append(metadataline)

        # if SliceLocation is None, it is sorted to the end
        # this is not necessary it can be deleted
        files.sort(key=lambda x: (x['SliceLocation'] is None, x["SliceLocation"]))

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
    slice_location = None
    if hasattr(dcmdata, 'SliceLocation'):
        # print(dcmdata.SliceLocation)
        # print(type(dcmdata.SliceLocation))
        try:
            slice_location = float(dcmdata.SliceLocation)
        except Exception as exc:
            logger.info("It is not possible to use SliceLocation")
            logger.debug(traceback.format_exc())
    if slice_location is None and hasattr(dcmdata, "SliceThickness") and teil is not None:
        logger.debug(
            "Estimating SliceLocation wiht image number and SliceThickness"
        )

        # from builtins import map
        i = list(map(int, re.findall('\d+', teil)))
        i = i[-1]
        try:
            slice_location = float(i * float(dcmdata.SliceThickness))
        except ValueError as e:
            print(type(dcmdata.SliceThickness))
            print(dcmdata.SliceThickness)
            logger.debug(traceback.format_exc())
            logger.debug("SliceThickness problem")

    if slice_location is None and hasattr(dcmdata, "ImagePositionPatient") and hasattr(dcmdata,
                                                                                       "ImageOrientationPatient"):
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
    :param dct:
    :param obj: object
    :param attr: object attribute name
    :return:  dict
    """
    if hasattr(obj, attr):
        dct[attr] = getattr(obj, attr)
    return dct


def get_series_number_console(dcmreader, counts, bins, qt_app=None):  # pragma: no cover

    print('series')
    series_info = dcmreader.dicomdirectory.get_stats_of_series_in_dir()
    print(dcmreader.print_series_info(series_info))
    snstring = raw_input('Select Serie: ')

    sn = int(snstring)
    return sn


def get_series_number_qt(dcmreader, counts, bins, qt_app=None):  # pragma: no cover

    if qt_app is None:
        # @TODO  there is problem with type of qappliaction
        # mport PyQt4
        # rom PyQt4.QtGui import QApplication
        # t_app = QApplication(sys.argv)
        # t_app = PyQt4.QtGui.QWidget(sys.argv)
        print(qt_app)

    series_info = dcmreader.dicomdirectory.get_stats_of_series_in_dir()
    study_info_msg = dcmreader.dicomdirectory.get_study_info_msg(series_info=series_info)
    print(dcmreader.print_series_info(series_info))
    from PyQt4.QtGui import QInputDialog
    # bins = ', '.join([str(ii) for ii in bins])
    sbins = [str(ii) for ii in bins]
    sbinsd = {}
    for serie_number in series_info.keys():
        strl = get_one_serie_info(series_info, serie_number)
        sbinsd[strl] = serie_number
        # sbins.append(str(ii) + "  " + serie_number)
    sbins = list(sbinsd)
    snstring, ok = \
        QInputDialog.getItem(qt_app,
                             'Serie Selection',
                             study_info_msg +
                             ' Select serie:',
                             sbins,
                             editable=False)
    sn = sbinsd[str(snstring)]
    return sn


def get_dcmdir_qt(app=False, directory=''):  # pragma: no cover
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


def sort_list_of_dicts(lst_of_dct, keys, reverse=False, **sort_args):
    """
    Sort by defined keys.

    If the key is not available, sort these to the end.

    :param lst_of_dct:
    :param keys:
    :param reverse:
    :param sort_args:
    :return:
    """
    # use this function from imtools.dili.sort_list_of_dicts()

    if type(keys) != list:
        keys = [keys]
    # dcmdir = lst_of_dct[:]
    dcmdir = lst_of_dct
    # sorting is based on two values in tuple (has_this_key: bool, value_or_None)
    # dcmdir.sort(key=lambda x: [((False, x[key] if x[key] is not None else 0) if key in x else (True, 0)) for key in keys], reverse=reverse, **sort_args)
    dcmdir.sort(key=lambda x: [((False, x[key] if x[key] is not None else 0) if key in x else (True, 0)) for key in keys], reverse=reverse, **sort_args)
    # dcmdir.sort(key=lambda x: [(x[key] for key in keys], reverse=reverse, **sort_args)
    return dcmdir

    # dcmdir.sort(key=lambda x: x[sort_key])


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

