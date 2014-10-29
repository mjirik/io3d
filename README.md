io3d
====

3D data read and write


Install
===


    pip install io3d

You can use 3D viewer sed3 for visualization

    pip install sed3


Example
===

    import io3d
    import sed3
    dr = io3d.DataReader()
    datap = dr.Get3DData('sample_data/jatra_5mm/', dataplus_format=True)

    ed = sed3.sed3(datap['data3d'])
    ed.show()

