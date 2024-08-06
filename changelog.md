# Changelog

Latest version 2.10.7

## 2024

* [changed] Less log messages
* [added] export of masks from COCO annotation files in devel

## 2.10

* [Added] Read by url
* [Added] Export masks from COCO annotation files

## 2.9

* [Changed] Dicom files uint are stored directly. The int dtype in 3D can be stored with intercept in metadata.
* [Added] Nifti support for '.ni.gz' extension

## 2.6

* [Added] Orientation codes support
* [Added] Data can be accessed by the property (e.g. `datap.data3d`)

## 2.5

* [Added] `read_dataset()` allow to read different datasets in the same way
* [Changed] `join_path` return `Path` object as default
* [Added] Datasets are now stored in `datasets.csv` on github
* [Fixed] Deprecation Warning on `get_slice_location()`

## 2.4

* [Fixed] Shortest specific path now works

## 2.3

* [Changed] Relative dataset download path implementation
* [Added] URL can be used to download data
* [Added] Specific dataset can be stored in different path (download is in plan todo)

## 2.2

* [Changed] Some data are stored to `sample_data` instead of `sample-data`
* [Changed] Internal representation of dataset dir is now just `root` 
(instead of`root/medical/orig`)
* [Changed] Yaml save cache with safe typ
* [Added] Crate backup cache file if the old is wrong

## 2.1

* [Changed] dependency on actual `imma` package

## 2.0

* [Changed] Python 3 compatibility only
* [Fixed] mode and order in `resize_to_shape` function
* [Fixed] respect new functionality in skimage.transform
* [Added] New arguments in `resize_to_shape` function
* [Added] New tests for seeds
* [Added] On resize check if all seeds are preserved

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

