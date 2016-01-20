[![Build Status](https://travis-ci.org/mjirik/io3d.svg?branch=master)](https://travis-ci.org/mjirik/io3d)
[![Coverage Status](https://coveralls.io/repos/mjirik/io3d/badge.svg?branch=master)](https://coveralls.io/r/mjirik/io3d?branch=master)

io3d
====

3D data read and write


Install
===


    pip install io3d

You can use 3D viewer sed3 for visualization

    pip install sed3


Example 1
===

    python io3d/datareader.py -i ./sample_data/jatra_5mm/

Example 2
===

    import io3d
    import sed3
    dr = io3d.DataReader()
    datap = dr.Get3DData('sample_data/jatra_5mm/', dataplus_format=True)

    ed = sed3.sed3(datap['data3d'])
    ed.show()

Test data
===

[io3d_sample_data](http://147.228.240.61/queetech/sample-extra-data/io3d_sample_data.zip)

[ct_head.rawiv](http://mgltools.scripps.edu/downloads/tars/releases/DocTars/DOCPACKS/Vision/doc/Tutorial/headandslice/ct_head.rawiv)

Put this data into sample_data dir
