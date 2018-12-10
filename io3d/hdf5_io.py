"""
based on https://codereview.stackexchange.com/questions/120802/recursively-save-python-dictionaries-to-hdf5-files-using-h5py

"""

import numpy as np
import h5py
import os


def save_dict_to_hdf5(dic, filename):
    """
    ....
    """
    with h5py.File(filename, 'w') as h5file:
        rf = recursively_save_dict_contents_to_group(h5file, '/', dic)
        h5_rf = h5file.create_group("_reconstruction_flags")
        for k, v in rf.items():
            h5_rf.create_dataset("/_reconstruction_flags" + k, data=v)


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """
    ....
    """
    reconstruction_flags = {}
    for key, item in dic.items():
        if type(key) is not str:
            key = str(key)
        if isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes, int)):
            h5file[path + key] = item
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
        elif isinstance(item, list):
            # i = iter(item)
            item_dict = dict(zip(range(len(item)), item))
            reconstruction_flags[path + key + "/"] = "list"
            rf = recursively_save_dict_contents_to_group(h5file, path + key + '/', item_dict)
            reconstruction_flags.update(rf)
        else:
            raise ValueError('Cannot save %s type'%type(item))
    return reconstruction_flags

def load_dict_from_hdf5(filename):
    """
    ....
    """
    with h5py.File(filename, 'r') as h5file:
        return recursively_load_dict_contents_from_group(h5file, '/')

def recursively_load_dict_contents_from_group(h5file, path):
    """
    ....
    """
    rf = h5file["_reconstruction_flags"]
    ans = {}
    for key, item in h5file[path].items():
        if key == "_reconstruction_flags":
            continue
        if key in rf:
            flag = rf[key]
            if flag.value == "list":
                dict_to_output = recursively_load_dict_contents_from_group(h5file, path + key + '/')
                ans[key] = list(dict_to_output.values())

        elif isinstance(item, h5py._hl.dataset.Dataset):
            ans[key] = item.value
        elif isinstance(item, h5py._hl.group.Group):
            ans[key] = recursively_load_dict_contents_from_group(h5file, path + key + '/')
    return ans


if __name__ == '__main__':

    data = {'x': 'astring',
            'y': np.arange(10),
            'd': {'z': np.ones((2,3)),
                  'b': b'bytestring'}}
    print(data)
    filename = 'test.h5'
    save_dict_to_hdf5(data, filename)
    dd = load_dict_from_hdf5(filename)
    print(dd)
    # should test for bad type