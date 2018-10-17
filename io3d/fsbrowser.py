import logging
logger = logging.getLogger(__name__)
import glob
import numpy as np
import os

from .import datareader

def remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

class FileSystemBrowser():
    def __init__(self, path=None):
        self.path = path
        self.preview_size = [100, 100]
        pass

    def get_path_info(self, path):
        """
        Get information about path (dir or file).
        :return:
        """

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
        retval = {
            "name": "Study0545",
            "type": "dir",
            "preview": np.zeros(self.preview_size),
            "text": "1 study, 3 series, 18321 files, acquisition_date=2017-02-16 to 2017-02-19",
            "acquisition_date": ["2015-02-16", "2015-02-16"],
            "modality": "MRI",
            "path": "C:/data/Study0545"
        }
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
