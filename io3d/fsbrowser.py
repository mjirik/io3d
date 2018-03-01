import logging
logger = logging.getLogger(__name__)
import glob
import numpy as np


class FileSystemBrowser():
    def __init__(self, path=None):
        self.path = path
        self.preview_size = [100, 100]
        pass

    def list_directory(self):
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
