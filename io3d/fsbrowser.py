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

# TODO - PyQt5 - done
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



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

def getOpenFileName(path, *other_params):
    # TODO naimplementovat na základě fsbrowser_test.py:test_devel_qt_dialog_fsbrowser()
    filename = ""
    return filename
    
#Widget - dcm browser    
#dcm preview widget + dir/img info widget
#getOpenFileName - fcn. to get path of chosen file
class DCMage(QFileDialog):
    def __init__(self, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        
        box = QVBoxLayout()

        self.setFixedSize(self.width() + 450, self.height() + 500)

        self.mpPreview = QLabel("Preview", self)
        self.mpPreview.setFixedSize(500, 500)
        self.mpPreview.setAlignment(Qt.AlignCenter)
        self.mpPreview.setObjectName("DCMage")
        box.addWidget(self.mpPreview)
        box.addStretch()
        self.layout().addLayout(box, 1, 3, 1, 1)
        
        self.mpPreview_1 = QLabel("Preview", self)
        self.mpPreview_1.setFixedSize(500, 500)
        self.mpPreview_1.setAlignment(Qt.AlignCenter)
        self.mpPreview_1.setObjectName("DCMage")
        box.addWidget(self.mpPreview_1)
        box.addStretch()
        self.layout().addLayout(box, 3, 3, 1, 1)
        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.getOpenFileName)

        self._fileSelected = None
        

    def dcm2png(self, path):
        ds1 = pdicom.read_file(path, force = True)
        x = plt.imsave('tempfile.png', ds1.pixel_array, cmap=plt.cm.gray)
        img = io.imread("tempfile.png")
        
    def onChange_text(self, path):
        path_l = path.lower()
        if(".dcm" in path_l):
            temp_text = self.get_path_info(path_l)
            self.mpPreview_1.setText(temp_text)
        elif("study" in path_l):
            temp_text = self.get_path_info(path_l)
            self.mpPreview_1.setText(temp_text)
        elif("serie" in path_l):
            temp_text = self.get_path_info(path_l)
            self.mpPreview_1.setText(temp_text)
        elif("case" in path_l):
            temp_text = self.get_path_info(path_l)
            self.mpPreview_1.setText(temp_text)
        elif("series" in path_l):
            temp_text = self.get_path_info(path_l)
            self.mpPreview_1.setText(temp_text)
        else:
            temp_text = "go to dir with dcm files"
            
    def onChange(self, path):
        self._fileSelected = path
        path_l = path.lower()
        self.onChange_text(path_l)
        if(".dcm" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
            self.get_path_info(path_l)
        elif("image_" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
            self.get_path_info(path_l)
        elif("study" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
            self.get_path_info(path_l)
        elif("serie" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
        elif("case" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
        elif("series" in path_l):
            try:
                self.dcm2png(path)
            except:
                print("no dcm to display")
            self.get_path_info(path_l)
        else:
            self.mpPreview.setText("Preview")
            
        pixmap = QPixmap("tempfile.png")

        if(pixmap.isNull()):
            self.mpPreview.setText("Preview")
        else:
            self.mpPreview.setPixmap(pixmap.scaled(self.mpPreview.width(), self.mpPreview.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        #self.get_path_info("tempfile.png")
        try:
            os.remove("tempfile.png")
        except:
            print("")


    def getOpenFileName(self, file):
        self.show()
        self.exec_()
        temp = self._fileSelected
        #print(temp)
        return temp

    
    def get_path_info(self, path):
        #problem with text len for qlabel - recomended for noneditable text //*textlen set to 00 needs to be edited
        if len(path) >= 50 & len(path) < 100:
            path1 = path[:50]
            path2 = path[50:100]
            path_formated = path1 + "\n" + path2
            
        #prepared cases for longer paths...
        elif len(path) >= 100 & len(path) < 150:
            path1 = path[:50]
            path2 = path[50:100]
            path3 = path[100:150]
            path_formated = path1 + "\n" + path2 + "\n" + path3
            
        elif len(path) >= 150 & len(path) < 200:
            path1 = path[:50]
            path2 = path[50:100]
            path3 = path[100:150]
            path4 = path[150:200]
            path_formated = path1 + "\n" + path2 + "\n" + path3 + "\n" + path4 
            
        elif len(path) >= 240 & len(path) < 300:
            path1 = path[:60]
            path2 = path[60:120]
            path3 = path[120:180]
            path4 = path[180:240]
            path5 = path[240:300]
            path_formated = path1 + "\n" + path2 + "\n" + path3 + "\n" + path4 + "\n" + path5

        else:
            print("too long path")
            path_formated = path
        try:
            path_sl = path + "/"
            res_last = path[-1]
            if res_last == "/":
                path_sl = path
            else:
                path_sl = path + "/"
        #name
            name = os.path.basename(os.path.normpath(path))
            name_final = ("name: " + name + '\n')
        #type
            type_ = os.path.isdir(path)
            if type_ == 1:
                type_res = "type: .dir" + '\n'
            if type_ == 0:
                type_res = ("type: " + name + '\n')

        #text - files, series, files
            serie_counter = 0
            study_counter = 0
            all_names = []
            counter_fail = 0
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    all_names.append(d.lower())
                    #TODO fix limit
                    for f in files:
                        all_names.append(f.lower())


        #lowercase - should be able to count all series,studies..
            for i in all_names:
                if "serie" in i: 
                    serie_counter += 1
                if "study" in i:
                    study_counter += 1
            filescounter = sum([len(files) for r, d, files in os.walk(path)])
            text = ("Study: " + str(study_counter) + '\n' + " Series: " + str(serie_counter) +" Files: " + str(filescounter) + '\n')

            path_lower = path.lower()

        #preview - forced path,some pic. from serie?
            if ".jpg" in path_lower:
                preview = ("image.")

            elif ".png" in path_lower:
                preview = ("image.")

            elif ".dcm" in path_lower:
                preview = ("image.")

            else:
                preview = ("Type: " + name) 
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

            text_path = ("path: " + path)
            acquid = 0
            modality = 0
            path = text_path
            name = name_final

            retval = [name, type_res, preview, text, acquid, modality, path_formated]
            #retval = [path_formated, path_formated1]
            retval_str = ''.join(map(str, retval))

            #"acquisition_date": ["2015-02-16", "2015-02-16"],
            #"modality": "MRI",
            return retval_str
        except:
            print("$$$")
            return None
        return None
