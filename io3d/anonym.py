import logging
logger = logging.getLogger(__name__)
import glob
try:
    import pydicom
except ImportError:
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom as pydicom
    logger.debug("dicom imported - it would be better use pydicom")

class Anonymizer():
    def __init__(self):
        self.filename = ''
        self.output_filename = ''
        self.whitelist = None

    def file_anonymization(self, filename, output_filename=None):
        self.filename = filename
        self.output_filename = output_filename
        if(self.output_filename == None):
            self.output_filename = 'D:\jatra_test'
        if(self.whitelist == None):
            self.setWhitelistDefault()

        dcmobj = pydicom.read_file(self.filename)
        atrr_list = dir(dcmobj)
        check = None

        for atribut in atrr_list:
            for item in self.whitelist:
                if(atribut != item):
                    check = False
                if(atribut == item):
                    check = True
        if(check == False):
            setattr(dcmobj, atribut, "")
        check = None

        dcmobj.save_as(self.output_filename)

    def recursive_anonymization(self, path, output_path=None):
        dirlist = glob.glob(path)

        pass

     ## gives path to whitelist text (.txt) file
    def setWhitelist(self, whitelistPath):
        self.whitelistPath = whitelistPath
        pthR = whitelistPath
        handleOpen = open(pthR, "r")

        with open(pthR) as file_handler:
            for line in file_handler:
                self.whitelist.append(line)
        handleOpen.close()

    def setWhitelistDefault(self):
        self.whitelist = [
            'Modality',
            'PatientAge',
            'AcquisitionDate',
            'AcquisitionNumber',
            'AcquisitionTime',
            'PatientPosition',
            'PatientSex',
            'RescaleSlope',
            'RescaleIntercept',
            'PixelSpacing',
            'SeriesDate',
            'SeriesDescription',
            'SeriesTime',
            'SeriesNumber',
            'SliceLocation',
            'SliceThickness',
            'StudyDate',
            'StudyID',
            'StudyTime',
            'StudyDesciption',
            'OverlayType',
            'OverlayRows',
            'OverlayOrigin',
            'OverlayDescription',
            'OverlayData',
            'OverlayColumns',
            'OverlayBitsAllocated',
            'OverlayBitPosition',
            'ImageComments',
            'ImageFrameOrigin',
            'ImageOrientationPatient',
            'ImagePositionPatient',
            ]

