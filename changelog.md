# Changelog

## Unreleased


## 2.0

* [Changed] Python 3 compatibility only

## 1.26.0

* [Added] New function io3d.datasets.get_labels() for obtaining list of available data

## 1.25.0

* [Changed] Checkum is computed on oreder directory (is less system dependent)

## 1.24.0

* [Changed] Compact checksumlog. Added hash for ircad

## 1.22.0

* [Added] Control over relative download directory for every dataset

## 1.21.1

* [Changed] Dataset SCP003 splited into image data and annotation

## 1.21.0

* [Added] New sample data SCP003

## 1.20.0

* [Changed] Save all types acceptable by json to hdf5

## 1.19.0 

* [Changed] Accept None type i hdf5 export

## 1.18.0

* [Changed] Not-string like keys supported in hdf5

## 1.17.0 (2018-12-10)

* [Added] File format h5 supported

## 1.16.0 (2018-12-10)

* [Added] Reading patient name, id, age and sex
* [Added] Display patient's info in qt widget

## 1.15.0

* [Changed] If file exists the new file name is created which does not collide
 with Study ID

## 1.14.0

* [Added] Guess series number for automatic liver processing

## 1.13.0 

* [Changed] Logging in dataset more verbatim

## 1.12.0

* [Added] Slice data added to datasets

## 1.11.0

* datasets.join_path can return datasets root path
* pydicom warnings are supressed

## 1.8.0

* New function for removing files

## 1.7.0

* New distance segmentation function

## 1.6.1

* New dataset generate function with synthetic liver and portal vein
* Rotation works now with interpolation order = 1

## 1.5.2

* Test and first development on File System Browser

## 1.5.1

* Logger for `dicom_expected` flag

## 1.5.0

* Added `dicom_expected` flag to prevent warning

## 1.4.4

* Directory information is returned in `pandas` dataframe
* New sample generator - face

## 1.4.3

* Fixed warnings 
* Updated requirements

## 1.4.0

* Datasets update
* New pklz write test
* Fixed SimpleITK version issues

## 1.3.49

* Datasets moved to other server

## 1.3.48

* Filter doubled files

## 1.3.47

* Memory error fixed

## 1.3.44 2018-05-14

* PyQt4 QString compatibility with python 2 and python 3

## 1.3.43

* Better code climate with PEP8 fixes

## 1.3.40

* GUI Qt4 bytes type compatibility with python 2 and python 3

## 1.3.38

* New download function for datasets

## 1.3.36

* Object pickle algorithm compatible with python 2 and python 3

