#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Simple program for ITK image read/write in Python
# import itk


import numpy as np

from loguru import logger

import os.path

import re

import pydicom as dicom

dicom.config.debug(False)

import os.path as op
from typing import Union
from pathlib import Path
from . import rawN
from . import misc

# from sys import argv
from . import dcmtools
from . import image


def write(
    data3d: Union[np.ndarray, dict, image.DataPlus],
    path: Union[Path, str],
    filetype="auto",
    metadata: dict = None,
    allow_rescale_intercept: bool = False,
):
    """

    :param data3d: input ndarray or DataPlus
    :param path: output path, if braces are in the name ("dir/file{:04d}.dcm"), image stack is produced .
    Check function filename_format() for more details.
    :param filetype: dcm, png, h5, ... "image_stack"
    :param metadata: metadata f.e. {'voxelsize_mm': [3,2,2]}
    :param allow_rescale_intercept: SimpleITK does not allow to write 3D files with negative values int dicom. With this
    rescale_intercept option turned on, the unsigned data type will be used and rescale parameter in dicom metadata
    will be set.
    :return:
    """

    dw = DataWriter()
    dw.Write3DData(
        data3d,
        path,
        filetype,
        metadata,
        allow_rescale_intercept=allow_rescale_intercept,
    )


class DataWriter:
    def __init__(self):
        self.stop_writing = False
        self.progress_callback = None

    def __get_segmentation_path(self, path):
        """Create path with "_segmentation" suffix and keep extension.

        :param path:
        :return:
        """
        startpath, ext = os.path.splitext(path)
        segmentation_path = startpath + "_segmentation" + ext
        return segmentation_path

    def Write3DData(
        self,
        data3d,
        path,
        filetype="auto",
        metadata=None,
        progress_callback=None,
        sfin=True,
        allow_rescale_intercept=False,
    ):
        """
        :param data3d: input ndarray data
        :param path: output path, to specify slice number advanced formatting options (like {:06d}) can be used
        Check function filename_format() for more details.
        :param metadata: {'voxelsize_mm': [1, 1, 1]}
        :param filetype: dcm, vtk, rawiv, image_stack
        :param progress_callback: fuction for progressbar f.e. callback(value, minimum, maximum)
        :param sfin: Use separate file for segmentation if necessary
        :param allow_rescale_intercept: SimpleITK does not allow to write 3D files with negative values in dicom. With this
        rescale_intercept option turned on, the unsigned data type will be used and rescale parameter in dicom metadata
        will be set.


        """

        self.orig_path = path
        path = os.path.expanduser(path)

        tp = type(data3d)
        if tp in (image.DataPlus, dict):
            # copy
            datap = dict(data3d)
            data3d = datap.pop("data3d")
            metadata = datap
        elif tp == np.ndarray:
            pass
        else:
            logger.warning(f"Type '{tp}' may not be compatible with datawriter.")

        if progress_callback is not None:
            self.progress_callback = progress_callback

        if filetype == "auto":
            startpath, ext = os.path.splitext(path)
            filetype = ext[1:].lower()

        segmentation = None
        if metadata is not None and "segmentation" in metadata.keys():
            segmentation_path = self.__get_segmentation_path(path)
            segmentation = metadata["segmentation"]

        mtd = {"voxelsize_mm": [1, 1, 1]}
        if metadata is not None:
            mtd.update(metadata)
        metadata = mtd

        if path.find("{") >= 0:
            filetype = "image_stack"
            # one_file_per_slice = True

        #     if one_file_per_slice:
        #         self._one_file_per_slice(self, data3d, path, filetype, metadata)
        #     else:
        #         self._all_in_one_file(self, data3d, path, filetype, metadata)
        #
        # def _all_in_one_file(self, data3d, path, filetype, metadata):

        if filetype in ["vtk", "tiff", "tif", "mhd", "nii", "raw"]:
            self._write_with_sitk(path, data3d, metadata, allow_rescale_intercept)
            if sfin and segmentation is not None:
                self._write_with_sitk(segmentation_path, segmentation, metadata)
        elif filetype in ["dcm", "DCM", "dicom"]:
            if data3d.dtype in (np.uint8, np.int8, np.uint16, np.uint16):
                pass
            else:
                logger.warning(
                    f"Datatype {data3d.dtype} is not supported by io3d due to SimpleITK. Changed to np.int16)"
                )
                data3d = data3d.astype(np.int16)
            self._write_with_sitk(path, data3d, metadata, allow_rescale_intercept)
            self._fix_sitk_bug(path, metadata)
            if sfin and segmentation is not None:
                self._write_with_sitk(
                    segmentation_path, segmentation, metadata, allow_rescale_intercept
                )
                self._fix_sitk_bug(segmentation_path, metadata)
        elif filetype in ["rawiv"]:
            rawN.write(path, data3d, metadata)
        elif filetype in ["image_stack"]:
            self.save_image_stack(data3d, path, metadata)
        elif filetype in ["hdf5", "hdf", "h5", "he5"]:
            self.save_hdf5(data3d, path, metadata)
        elif str(path).lower().endswith(".nii.gz") or ext == "nii":
            import io3d.nifti_io

            metadata["data3d"] = data3d
            datap = metadata
            logger.debug(f'orientation_axcodes={datap["orientation_axcodes"]}')
            io3d.nifti_io.write_nifti(datap, path)
        elif filetype in ["pkl", "pklz"]:
            from . import misc

            metadata["data3d"] = data3d
            datap = metadata

            misc.obj_to_file(datap, path)

        else:
            logger.error('Unknown filetype: "' + filetype + '"')
            raise ValueError("Unknown filetype: '" + filetype + "'")

            # data = dicom.read_file(onefile)

    def _write_with_sitk(self, path, data3d, metadata, allow_rescale_intercept=False):
        self._makedirs(path)
        import SimpleITK as sitk

        dim = dcmtools.get_sitk_image_from_ndarray(
            data3d, allow_rescale_intercept=allow_rescale_intercept
        )
        vsz = metadata["voxelsize_mm"]

        # simple itk does not work with np.float32
        dim.SetSpacing([float(vsz[1]), float(vsz[2]), float(vsz[0])])
        sitk.WriteImage(dim, path)

    def _fix_sitk_bug(self, path, metadata):
        """
        There is a bug in simple ITK for Z axis in 3D images. This is a fix
        :param path:
        :param metadata:
        :return:
        """
        ds = dicom.read_file(path)
        ds.SpacingBetweenSlices = str(metadata["voxelsize_mm"][0])[:16]
        dicom.write_file(path, ds)

    def save_hdf5(self, data3d, path, metadata):
        metadata["data3d"] = data3d
        datap = metadata
        from . import hdf5_io

        hdf5_io.save_dict_to_hdf5(metadata, path)

        # # TODO this is not implemented in proper way
        # import h5py
        # f = h5py.File(path, "w")
        # f.create_dataset('data3d', data=data3d, compression='gzip')
        # met = f.create_group('metadata')
        # met.create_dataset('voxelsize_mm', data=metadata['voxelsize_mm'], compression='gzip')
        # # f.create_dataset('metadata', data=metadata, compression='gzip')
        # f.flush()
        # f.close()

    #
    # def __write_h5_key(self, grp, dct):
    #     import h5py
    #     import numpy as np
    #     retval = {}
    #     for key in dct.keys():
    #         try:
    #             data = dct[key]
    #             if type(data) == np.ndarray:
    #                 if data.dtype == np.dtype('O'):
    #                     logger.warning("problem with dtype('O')")
    #                     print("Press 'c' for continue")
    #                     from PyQt4 import QtCore; QtCore.pyqtRemoveInputHook()
    #                     import ipdb; ipdb.set_trace()
    #                 else:
    #                     grp.create_dataset(key, data=data)
    #             elif type(data) == list:
    #                 grp.create_dataset(key, data=data)
    #             elif type(data) == dict:
    #                 subgrp = grp.create_group('key')
    #                 self.__write_h5_key(subgrp, data)
    #             else:
    #                 grp[key] = data
    #         except:
    #             import traceback
    #             logger.warning(traceback.format_exc())
    #
    #
    #     return retval

    def DataCopyWithOverlay(self, dcmfilelist, out_dir, overlays):
        """
        Function make 3D data from dicom file slices

        :dcmfilelist list of sorted .dcm files
        :overlays dictionary of binary overlays. {1:np.array([...]), 3:...}
        :out_dir output directory

        """
        dcmlist = dcmfilelist
        # data3d = []

        for i in range(len(dcmlist)):
            onefile = dcmlist[i]

            logger.info(onefile)
            data = dicom.read_file(onefile)

            for i_overlay in overlays.keys():
                overlay3d = overlays[i_overlay]
                data = self.encode_overlay_slice(
                    data, overlay3d[-1 - i, :, :], i_overlay
                )

            # construct output path
            head, tail = os.path.split(os.path.normpath(onefile))
            filename_out = os.path.join(out_dir, tail)

            # save
            data.save_as(filename_out)
            # import pdb; pdb.set_trace()

    def add_overlay_to_slice_file(
        self, filename, overlay, i_overlay, filename_out=None
    ):
        """Function adds overlay to existing file."""
        if filename_out is None:
            filename_out = filename
        filename = op.expanduser(filename)
        data = dicom.read_file(filename)
        data = self.encode_overlay_slice(data, overlay, i_overlay)
        data.save_as(filename_out)

    def encode_overlay_slice(self, data, overlay, i_overlay):
        """ """
        # overlay index
        n_bits = 8

        # On (60xx,3000) are stored ovelays.
        # First is (6000,3000), second (6002,3000), third (6004,3000),
        # and so on.
        dicom_tag1 = 0x6000 + 2 * i_overlay

        #  data (0x6000, 0x3000)
        # WR = 'OW'
        # WM = 1

        # On (60xx,0010) and (60xx,0011) is stored overlay size
        row_el = dicom.dataelem.DataElement(
            (dicom_tag1, 0x0010), "US", int(overlay.shape[0])
        )
        data[row_el.tag] = row_el

        col_el = dicom.dataelem.DataElement(
            (dicom_tag1, 0x0011), "US", int(overlay.shape[1])
        )
        data[col_el.tag] = col_el

        # arrange values to bit array
        overlay_linear = np.reshape(overlay, np.prod(overlay.shape))

        # allocation of dataspace
        encoded_linear = np.zeros(
            (np.prod(overlay.shape) / n_bits).astype(np.int), dtype=np.uint8
        )

        # encoded data
        for i in range(0, len(overlay_linear)):
            if overlay_linear[i] > 0:
                bit = 1
            else:
                bit = 0

            encoded_linear[int(i / n_bits)] |= bit << (i % n_bits)

        overlay_raw = encoded_linear.tostring()

        # Decoding data. Each bit is stored as array element
        # TODO neni tady ta jednička blbě?
        #        for i in range(1,len(overlay_raw)):
        #            for k in range (0,n_bits):
        #                byte_as_int = ord(overlay_raw[i])
        #                decoded_linear[i*n_bits + k] = (byte_as_int >> k) & 0b1
        #
        # overlay = np.array(pol)

        overlay_el = dicom.dataelem.DataElement((dicom_tag1, 0x3000), "OW", overlay_raw)
        data[overlay_el.tag] = overlay_el

        return data

    def _makedirs(self, filepattern, series_number=None):
        filename = get_first_filename(filepattern, series_number=series_number)
        datadir, dataname = os.path.split(filename)

        if datadir != "" and not os.path.exists(datadir):
            os.makedirs(datadir)

    def save_image_stack(self, data3d, filepattern, metadata=None):

        if (metadata is not None) and "series_number" in metadata.keys():
            series_number = int(metadata["series_number"])
        else:
            series_number = get_unoccupied_series_number(filepattern)

        self._makedirs(filepattern, series_number=series_number)
        datadir, dataname = os.path.split(filepattern)
        databasename, dataext = os.path.splitext(dataname)

        if filepattern.find("{") < 0:
            # filepattern does not contain place for integer
            filepattern = os.path.join(datadir, databasename + "{:05d}" + dataext)
        # print(filepattern)
        if (metadata is not None) and "voxelsize_mm" in metadata.keys():
            z_position = 0.0  # metadata["voxelsize_mm"][0]
            z_vs = metadata["voxelsize_mm"][0]
        else:
            z_position = 0.0
            z_vs = 1.0

        total_number = data3d.shape[0]
        for i in range(total_number):
            if self.progress_callback is not None:
                self.progress_callback(value=i, minimum=0, maximum=total_number)
            if self.stop_writing:
                break
            newfilename = filename_format(
                filepattern,
                slice_number=i,
                slice_position=z_position,
                series_number=series_number,
            )
            # newfilename = filepattern.format(i)
            logger.debug(newfilename)
            data2d = data3d[i, :, :]
            import SimpleITK as sitk

            # pixelType = itk.UC
            # imageType = itk.Image[pixelType, 2]
            dim = sitk.GetImageFromArray(data2d)

            if metadata is not None:
                vsz = np.asarray(metadata["voxelsize_mm"]).astype("double")
                dim.SetSpacing([vsz[2], vsz[1]])
                if dataext in (".dcm", ".DCM"):
                    self._set_dicom_tag(
                        dim, metadata, "PatientName", f"patient"
                    )  # 0010|0010
                    self._set_dicom_tag(dim, metadata, "PatientID", f"0")  # 0010|0020
                    self._set_dicom_tag(
                        dim, metadata, "SliceThickness", f"{z_vs}"
                    )  # 0018|050 Slice Thickness
                    self._set_dicom_tag(
                        dim, metadata, "SpacingBetweenSlices", f"{z_vs}"
                    )  # 0018|0088
                    # self._set_dicom_tag(dim, metadata, "Nominal Scanned Pixel Spacing", f"{z_vs}")  # 0018|2010
                    self._set_dicom_tag(dim, metadata, "StudyID", str(0))  # 0020|0010
                    self._set_dicom_tag(
                        dim, metadata, "SeriesNumber", str(series_number)
                    )  # 0020|0011
                    self._set_dicom_tag(
                        dim, metadata, "InstanceNumber", str(i)
                    )  # 0020|0013
                    self._set_dicom_tag(
                        dim, metadata, "ImagePosition", f"0\\0\\{z_position}"
                    )  # 0020|0032
                    self._set_dicom_tag(
                        dim, metadata, "ImageOrientationPatient", r"1\0\0\0\1\0"
                    )  # 0020|0037
                    # self._set_dicom_tag(dim, metadata, "0020|1041", z_position)  # Slice Location
                    self._set_dicom_tag(
                        dim, metadata, "SliceLocation", str(z_position)
                    )  # 0020|1041
                    # self._set_dicom_tag(dim, metadata, "0028|0030", str(vsz[1]))  # Pixel Spacing
                    self._set_dicom_tag(
                        dim, metadata, "PixelSpacing", f"{vsz[1]}\\{vsz[2]}"
                    )  # 0028|0030
                    self._set_dicom_tag(dim, metadata, "Modality", f"")

            # import ipdb; ipdb.set_trace()
            sitk.WriteImage(dim, newfilename)
            z_position += z_vs

    def _set_dicom_tag(self, dim, metadata, tagname, default):
        """
        Set valude to dicom. Use value from metadata if possible.
        :param dim:
        :param metadata:
        :param tagname:
        :param default:
        :return:
        """

        if "|" in tagname:
            sitk_dicom_tag = tagname
        else:
            sitk_dicom_tag = (
                str(dicom.tag.Tag(tagname))
                .replace(", ", "|")
                .replace("(", "")
                .replace(")", "")
            )
        value = metadata[tagname] if tagname in metadata else default
        dim.SetMetaData(sitk_dicom_tag, value)

    def stop(self):
        self.stop_writing = True


def get_first_filename(filepattern, series_number=None):
    filepattern = os.path.expanduser(filepattern)
    if series_number is None:
        series_number = get_unoccupied_series_number(filepattern)
    return filename_format(filepattern, series_number=series_number)


def get_unoccupied_series_number(filepattern, series_number=1):
    filepattern = os.path.expanduser(filepattern)
    filename = filename_format(filepattern, series_number=series_number)

    while os.path.exists(filename):
        series_number += 1
        fn = filename_format(filepattern, series_number=series_number)
        if fn == filename:
            # no series number is used in filepattern
            return series_number - 1
        filename = fn

    return series_number


# def _fill_filepattern_based_on_rexp(rexp1, filepattern, something_to_fill):
#     if type(something_to_fill) is str:
#         sub1 = re.sub(rexp1, "", filepattern)
#
#     # now it looks for series number
#     rexp1 = r"({\s*seriesn\s*:?.*?})"
#     rexp2 = r"({\s*series_number\s*:?.*?})"
#
#     sub1 = re.findall(rexp1, filepattern)
#     sub2 = re.findall(rexp2, filepattern)
#
#     for single_pattern in sub1:
#         pattern = single_pattern.format(series_number=series_number, seriesn=series_number)
#         filepattern = re.sub(rexp1, pattern, filepattern)
#
#     for single_pattern in sub2:
#         pattern = single_pattern.format(series_number=series_number, seriesn=series_number)
#         filepattern = re.sub(rexp2, pattern, filepattern)


def filepattern_fill_slice_number_or_position(filepattern, slice_description):
    # for string like series number there should be ignored (removed) the formating part
    if type(slice_description) is str:
        rexp1 = r"{\s*slicen\s*(:?.*?)}"
        rexp2 = r"{\s*slice_number\s*(:?.*?)}"
        rexp3 = r"{\s*slicep\s*(:?.*?)}"
        rexp4 = r"{\s*slice_position\s*(:?.*?)}"
        rexp5 = r"{\s*(:.*?)}"
        filepattern = re.sub(rexp1, "", filepattern)
        filepattern = re.sub(rexp2, "", filepattern)
        filepattern = re.sub(rexp3, "", filepattern)
        filepattern = re.sub(rexp4, "", filepattern)
        filepattern = re.sub(rexp5, "", filepattern)

    # now it looks for series number
    rexp1 = r"({\s*slicen\s*:?.*?})"
    rexp2 = r"({\s*slice_number\s*:?.*?})"
    rexp3 = r"({\s*slicep\s*:?.*?})"
    rexp4 = r"({\s*slice_position\s*:?.*?})"
    rexp5 = r"({\s*:.*?})"
    rexp6 = r"({\s*})"

    sub1 = re.findall(rexp1, filepattern)
    sub2 = re.findall(rexp2, filepattern)
    sub3 = re.findall(rexp3, filepattern)
    sub4 = re.findall(rexp4, filepattern)
    sub5 = re.findall(rexp5, filepattern)
    sub6 = re.findall(rexp5, filepattern)

    for single_pattern in sub1:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp1, pattern, filepattern)

    for single_pattern in sub2:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp2, pattern, filepattern)

    for single_pattern in sub3:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp3, pattern, filepattern)

    for single_pattern in sub4:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp4, pattern, filepattern)

    for single_pattern in sub5:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp5, pattern, filepattern)

    for single_pattern in sub6:
        pattern = single_pattern.format(
            slice_number=slice_description,
            slicen=slice_description,
            slice_position=slice_description,
            slicep=slice_description,
        )
        filepattern = re.sub(rexp6, pattern, filepattern)
    return filepattern


def filepattern_fill_series_number(filepattern, series_number):

    # for string like series number there should be ignored (removed) the formating part
    if type(series_number) is str:
        rexp1 = r"{\s*seriesn\s*(:?.*?)}"
        rexp2 = r"{\s*series_number\s*(:?.*?)}"
        filepattern = re.sub(rexp1, "", filepattern)
        filepattern = re.sub(rexp2, "", filepattern)

    # now it looks for series number
    rexp1 = r"({\s*seriesn\s*:?.*?})"
    rexp2 = r"({\s*series_number\s*:?.*?})"

    sub1 = re.findall(rexp1, filepattern)
    sub2 = re.findall(rexp2, filepattern)

    for single_pattern in sub1:
        pattern = single_pattern.format(
            series_number=series_number, seriesn=series_number
        )
        filepattern = re.sub(rexp1, pattern, filepattern)

    for single_pattern in sub2:
        pattern = single_pattern.format(
            series_number=series_number, seriesn=series_number
        )
        filepattern = re.sub(rexp2, pattern, filepattern)

    return filepattern


def filename_format(filepattern, series_number=1, slice_number=0, slice_position=0.0):
    """

    :param filepattern: advanced format options can be used in filepattern.
    Fallowing keys can be used: slice_number, slicen, series_number, seriesn, series_position, seriesp.
    For example '{:06d}.jpg', '{series_number:03d}/{slice_position:07.3f}.png'
    :param series_number:
    :param slice_number:
    :param slice_position:
    :param change_series_number_if_file_exists:
    :return:
    """
    filepattern = misc.old_str_format_to_new(filepattern)

    filename = filepattern.format(
        slice_number,
        slice_number=slice_number,
        slice_position=slice_position,
        series_number=series_number,
        slicen=slice_number,
        slicep=slice_position,
        seriesn=series_number,
    )
    return filename


def saveOverlayToDicomCopy(
    input_dcmfilelist, output_dicom_dir, overlays, crinfo, orig_shape
):
    """Save overlay to dicom."""
    from . import datawriter as dwriter

    # import qmisc
    if not os.path.exists(output_dicom_dir):
        os.makedirs(output_dicom_dir)

    import imtools.image_manipulation

    # uncrop all overlays
    for key in overlays:
        overlays[key] = imtools.image_manipulation.uncrop(
            overlays[key], crinfo, orig_shape
        )

    dw = dwriter.DataWriter()
    dw.DataCopyWithOverlay(input_dcmfilelist, output_dicom_dir, overlays)
