[![Build Status](https://travis-ci.org/mjirik/io3d.svg?branch=master)](https://travis-ci.org/mjirik/io3d)
[![Coverage Status](https://coveralls.io/repos/mjirik/io3d/badge.svg?branch=master)](https://coveralls.io/r/mjirik/io3d?branch=master)
[![Documentation Status](https://readthedocs.org/projects/io3d/badge/?version=latest)](http://io3d.readthedocs.io/en/latest/?badge=latest)

# io3d

This package contains set of functions used for reading and writing 3D data.

## Install

Use anaconda 

```shell
conda install -c mjirik -c conda-forge -c SimpleITK io3d
```

or

```shell
pip install io3d
```

You can use 3D viewer sed3 for visualization.

```shell
pip install sed3
```

## Examples


### Get sample data

command line:
```shell
python -m io3d -l 3Dircadb1.1
```

### Example 1

```shell
python io3d/datareader.py -i ./sample_data/jatra_5mm/
```

### Example 2

```python
import io3d
import sed3
dr = io3d.DataReader()
pth = io3d.joinp()
datap = dr.Get3DData('sample_data/jatra_5mm/', dataplus_format=True)
print(datap["voxelsize_mm"])

ed = sed3.sed3(datap['data3d'])
ed.show()
```

### Example 3 - Use it in your application - Qt Widget

```python
import sys
from PyQt5 import QtGui
import io3d.datareaderqt

app = QtGui.QApplication(sys.argv)    
w = io3d.datereaderqt.DatareaderWidget()
w.show()
app.exec_()
datap = w.datap
```

![load_widget](imgs/load_widget.png)


## Test data

Get sample data with `io3d` package:

```shell
python -m io3d -l 3Dircadb1.1
```

Get list of available datasets:

```shell
python -m io3d -L
```

... or download data:

[io3d_sample_data](http://147.228.240.61/queetech/sample-extra-data/io3d_sample_data.zip)

[ct_head.rawiv](http://mgltools.scripps.edu/downloads/tars/releases/DocTars/DOCPACKS/Vision/doc/Tutorial/headandslice/ct_head.rawiv)

Put this data into sample_data dir.


### File or directory checksum

```shell
python -m io3d -c directory_path
```


### Specific dataset path

Some parts of dataset can be stored separately. 
You can set it by command

```shell
python -m io3d -ssdp "g:/Můj disk/data/biology/roots" "biology/roots"
python -m io3d -ssdp "g:/Můj disk/data/medical/orig/sliver07" "medical/orig/sliver07"
```

or you can edit `~\.io3d_cache.yaml`


### Get by url

Data can be downloaded from url. Just use URL instead of `label`.
The local path can be specified by adding local path to the end of url separated by colon.'

```bash
python -m io3d.datasets -l http://home.zcu.cz/~mjirik/lisa/sample_data/biodur_sample.zip:biodur_sample/
```
```bash
python -m io3d.datasets -l https://downloads.openmicroscopy.org/images/OME-TIFF/2016-06/bioformats-artificial/time-series.ome.tif:biology/orig/roots
```



# Read datasets coherently


```python
import io3d
import matplotlib.pyplot as plt
datap1 = io3d.read_dataset("3Dircadb1", "data3d", 1)
datap2 = io3d.read_dataset("3Dircadb1", "bone", 1)
plt.imshow(datap1["data3d"][20,:,:], cmap="gray")
plt.contour(datap2["data3d"][20,:,:])
plt.show()
```

![ircad](imgs/ircadb01.png)

Now you can read the sliver07 dataset in the same way. Just put it in `data/orig/medical/sliver07`

```python
import io3d
import matplotlib.pyplot as plt
datap1 = io3d.read_dataset("sliver07", "data3d", 1)
plt.imshow(datap1["data3d"][20,:,:], cmap="gray")
plt.show()
```
