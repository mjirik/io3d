#! /usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger
import glob
import numpy as np
import os

# TODO remove cv2 - done
import matplotlib.pyplot as plt
from fnmatch import fnmatch

try:
    import pydicom as pdicom
except ImportError:
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom as pdicom
    logger.debug("dicom imported - it would be better use pydicom")

from os import listdir
from os.path import isfile, join
from . import datareader
from skimage import io
import io3d
import io3d.dcmreaddata


def remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)


# FileSystemBrowser("c:/jkdfaldkfj/asdfasjfh")


class FileSystemBrowser:
    def __init__(self, path=None):
        self.path = path
        self.preview_size = [100, 100]
        self.nova_promenna = 5
        pass

    # metoda pouze na zobrazeni obrazku - volala by se v pripade ze tam nejaky bude
    def get_path_info_preview(self, path):
        path_lower = path.lower()
        # name
        name = os.path.basename(os.path.normpath(path))
        name_final = "name: " + name
        path_sl = path + "/"

        if ".jpg" in path_lower:
            preview = "Used path leads to current image."
            img = io.imread(path)
            io.imshow(img)
            io.show()

        elif ".png" in path_lower:
            preview = "Used path leads to current image."
            img = io.imread(path)
            io.imshow(img)
            io.show()

        elif ".dcm" in path_lower:
            preview = "Used path leads to current image."
            ds = pdicom.dcmread(path)
            plt.imshow(ds.pixel_array, cmap=plt.cm.bone)

        else:
            preview = "Preview of files in dir: " + name
            only_files = [f for f in listdir(path) if isfile(join(path, f))]

            for x in only_files:
                if (".dcm" or ".Dcm" or ".DCM") in x:
                    ending = os.path.basename(os.path.normpath(path_sl + x))
                    preview_path = path_sl + ending
                    ds = pdicom.dcmread(preview_path)
                    plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
                    break
                elif (".jpg" or ".Jpg" or ".JPG") in x:
                    ending = os.path.basename(os.path.normpath(path_sl + x))
                    preview_path = path_sl + ending
                    img = io.imread(preview_path)
                    io.imshow(img)
                    io.show()
                    break

                elif (".png" or ".Png" or ".PNG") in x:
                    ending = os.path.basename(os.path.normpath(path_sl + x))
                    preview_path = path_sl + ending
                    img = io.imread(preview_path)
                    io.imshow(img)
                    io.show()
                    break

                else:
                    None
                    break

    # Tady skutečně musí být (self, path). Self je odkaz na mateřský objekt, následují pak další parametry.
    # def get_path_info(path): #(self, path)?
    def get_path_info(self, path):
        try:
            path_sl = path + "/"
            res_last = path[-1]
            if res_last == "/":
                path_sl = path
            else:
                path_sl = path + "/"
            # name
            name = os.path.basename(os.path.normpath(path))
            name_final = "name: " + name
            # type
            type_ = os.path.isdir(path)
            if type_ == 1:
                type_res = "type: .dir"
            if type_ == 0:
                type_res = "type: " + name

            # text - files, series, files
            serie_counter = 0
            study_counter = 0
            all_names = []
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    all_names.append(d.lower())
                    for f in files:
                        all_names.append(f.lower())
            # lowercase - should be able to count all series,studies..
            for i in all_names:
                if "serie" in i:
                    serie_counter += 1
                if "study" in i:
                    study_counter += 1
            filescounter = sum([len(files) for r, d, files in os.walk(path)])
            text = (
                "Study: "
                + str(study_counter)
                + " Series: "
                + str(serie_counter)
                + " Files: "
                + str(filescounter)
            )

            path_lower = path.lower()

            # preview - forced path,some pic. from serie?
            if ".jpg" in path_lower:
                preview = "Used path leads to current image."

            elif ".png" in path_lower:
                preview = "Used path leads to current image."

            elif ".dcm" in path_lower:
                preview = "Used path leads to current image."

            else:
                preview = "Preview of files in dir: " + name
                only_files = [f for f in listdir(path) if isfile(join(path, f))]

                for x in only_files:
                    if (".dcm" or ".Dcm" or ".DCM") in x:
                        print("dcm files")
                        break
                    elif (".jpg" or ".Jpg" or ".JPG") in x:
                        print("jpf files")
                        break

                    elif (".png" or ".Png" or ".PNG") in x:
                        print("png files")
                        break

                    else:
                        None
                        break
                # add required endings..
                # import io3d.datareader
                # io3d.datareader.read(file_path)
                # add required endings..

            # path
            text_path = "path: " + path

            # Fallowing function can be used for directory analysis
            # import io3d.dcmreaddata
            # dd = io3d.dcmreaddata.DicomDirectory(dirpath=path)
            # dd.get_stats_of_series_in_dir()

            # dd = dcmreaddata.DicomDirectory(self.path)
            # stats = dd.get_stats_of_series_in_dir()
            # studies_and_series = dd.get_stats_of_studies_and_series_in_dir()
            # import pydicom
            # pydicom.read_file(stats[7].dcmfilelist[0])

            # np.ndarray.resize()
            # JPG
            # import SimpleITK as Sitk

            # image = Sitk.ReadImage(datapath)
            # data3d = dcmtools.get_pixel_array_from_sitk(image)

            # TODO
            acquid = 0
            modality = 0
            path = text_path
            name = name_final

            retval = [name, type_res, preview, text, acquid, modality, path]
            # "acquisition_date": ["2015-02-16", "2015-02-16"],
            # "modality": "MRI",
            # print(retval)
            # print(retval[0])
            # print(retval[1])
            # print(retval[2])
            # print(retval[3])
            # print(retval[4])
            # print(retval[5])
            # print(retval[6])

        except:
            print("$Error$")
            return None

        return retval

    def get_dir_list(self):

        from . import dcmreaddata

        # datareader.read()
        # TODO check the design of output structure
        retval = [
            {
                "name": "Study0545",
                "type": "dir",
                "preview": np.zeros(self.preview_size),
                "text": "1 study, 3 series, 18321 files, acquisition_date=2017-02-16 to 2017-02-19",
                "acquisition_date": ["2015-02-16", "2015-02-16"],
                "modality": "MRI",
                "path": "C:/data/Study0545",
            },
            {
                "name": "Serie54864",
                "type": "serie",
                "preview": np.zeros(self.preview_size),
                "text": "3 series, 18321 files, acquisition_date=2017-02-16 to 2017-02-19",
                "acquisition_date": ["2015-02-16", "2015-02-16"],
                "modality": "MRI",
                "path": "c:/data/",
            },
            {  # maybe signle file make no sense
                "name": "first.mhd",
                "type": "file",
                "preview": np.zeros(self.preview_size),
                "text": "[1x512x512], voxelsize_mm=[5.0, 0.5, 0.5], acquisition_date=2015-08-16",
                "voxelsize_mm": [5.0, 0.5, 0.5],
                "acquisition_date": "2015-08-16",
                "modality": "CT",
            },
        ]
        return retval

    # def file_anonymization(self, filename, output_filename=None):
    #     pass

    def recursive_anonymization(self, path, output_path=None):
        dirlist = glob.glob(path)

        pass
