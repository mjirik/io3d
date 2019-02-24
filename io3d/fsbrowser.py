#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import glob
import numpy as np
import os

from fnmatch import fnmatch
import numpy as np
import matplotlib.pylab as plt
from os import listdir
from os.path import isfile, join

from .import datareader

def remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def img_show(im, h=5, **kwargs):#h = sz. scale
    y = im.shape[0]
    x = im.shape[1]
    w = (y/x) * h
    plt.figure(figsize=(w,h))
    plt.imshow(im, interpolation="none", **kwargs)


class FileSystemBrowser():
    def __init__(self, path=None):
        self.path = path
        self.preview_size = [100, 100]
        pass

    # Tady skutečně musí být (self, path). Self je odkaz na mateřský objekt, následují pak další parametry.
    # def get_path_info(path): #(self, path)?
    def get_path_info(self, path):

        path_sl = path + "/"
        #name
        name = os.path.basename(os.path.normpath(path))
        
        #type
        type_ = os.path.isdir(path)
        if type_ == 1:
            type_res = "Dir"
        if type_ == 0:
            type_res = ("Type: " + name)
            
        #text - files, series, files
        serie_counter = 0
        study_counter = 0
        all_names = []
        for root, dirs, files in os.walk(path):
            for d in dirs:
                all_names.append(d)
                #if contains ,,name of picture,, display_path - preview of pics. in study_x, serie_y..
                for f in files:
                    all_names.append(f)
        for i in all_names:
            if "serie" in i: 
                serie_counter += 1
            if "study" in i:
                study_counter += 1
        filescounter = sum([len(files) for r, d, files in os.walk(path)])
        text = ("Studie: " + str(study_counter) + " Serie: " + str(serie_counter) +" Files: " + str(filescounter))
        
        #preview - forced path,some pic. from serie?
        preview = ("Preview of files in dir: " + name)
        only_files = [f for f in listdir(path) if isfile(join(path, f))]
        for x in only_files:
            if ".jpg" in x:
                ending = os.path.basename(os.path.normpath(path_sl + x))
                preview_path = path_sl + ending
            if ".png" in x:
                ending = os.path.basename(os.path.normpath(path_sl + x))
                preview_path = path_sl + ending
            # add required endings..
        # TODO what if there is no jpg or png file?
        im = plt.imread(preview_path)
        im.shape
        # TODO this function should not be interactive - no imshow, no windows, iteractivity can be i.e. in test.
        img_show(im)
        
        #path
        text_path = ("Path: " + path)
        
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
        
        retval = [name, type_res, text, preview, text_path]
        #"acquisition_date": ["2015-02-16", "2015-02-16"],
        #"modality": "MRI",
        print(retval)
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
                "path": "C:/data/Study0545"
            },
            {
                "name": "Serie54864",
                "type": "serie",
                "preview": np.zeros(self.preview_size),
                "text": "3 series, 18321 files, acquisition_date=2017-02-16 to 2017-02-19",
                "acquisition_date": ["2015-02-16", "2015-02-16"],
                "modality": "MRI",
                "path": "c:/data/"

            },
            { # maybe signle file make no sense
                "name": "first.mhd",
                "type": "file",
                "preview": np.zeros(self.preview_size),
                "text": "[1x512x512], voxelsize_mm=[5.0, 0.5, 0.5], acquisition_date=2015-08-16",
                "voxelsize_mm": [5.0, 0.5, 0.5],
                "acquisition_date": "2015-08-16",
                "modality": "CT"

            },
        ]
        return retval
    # def file_anonymization(self, filename, output_filename=None):
    #     pass

    def recursive_anonymization(self, path, output_path=None):
        dirlist = glob.glob(path)

        pass
