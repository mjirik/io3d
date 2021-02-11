#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
based on https://codereview.stackexchange.com/questions/120802/recursively-save-python-dictionaries-to-hdf5-files-using-h5py

"""

from loguru import logger

import numpy as np
import h5py
import os


def save_dict_to_hdf5(dic, filename):
    """
    ....
    """
    delimiter = '/'
    with h5py.File(filename, "w") as h5file:
        print("start writing h5")
        rf = recursively_save_dict_contents_to_group(h5file, delimiter, dic)
        h5_rf = h5file.create_group("_reconstruction_flags")
        # h5_rf = h5file.create_group("_reconstruction_key_flags")
        print("reconstruction_flags:")
        for k, v in rf.items():
            # print(f'{k} {v}')
            h5_rf.create_dataset(delimiter + "_reconstruction_flags" + k, data=v)
            # print('created')
        # for k, v in rfk.items():
        #     h5_rf.create_dataset("/_reconstruction_key_flags" + k, data=v)


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """
    ....
    """
    delimiter = '/'
    # print(f"saving {path}, type={type(dic)}, {list(dic.keys())}")
    reconstruction_flags = {}
    # reconstruction_key_flags = {}
    for key, item in dic.items():
        # print(f"   {key}, type={type(item)}")
        if type(key) is not str:
            # import pickle
            # key = pickle.dumps(key).decode("ascii")
            import json

            key = json.dumps(key)

            # whole_reconstruction_key = path + key + "_key_" + delimiter
            whole_reconstruction_key = path + key + "_key_"
            reconstruction_flags[whole_reconstruction_key] = "json_key"

        # wholekey = path + key + "_typ_" + delimiter
        wholekey = path + key + "_typ_"
        if item is None:
            import json

            jitem = json.dumps(item)
            h5file[path + key] = jitem
            reconstruction_flags[wholekey] = "json_value"
        elif isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes)):
            h5file[path + key] = item
        elif isinstance(item, (float)):
            h5file[path + key] = item
            reconstruction_flags[wholekey] = "float"
        elif isinstance(item, (int)):
            h5file[path + key] = item
            reconstruction_flags[wholekey] = "int"
        elif isinstance(item, dict):
            rf = recursively_save_dict_contents_to_group(h5file, path + key + delimiter, item)
            reconstruction_flags.update(rf)
            # reconstruction_key_flags.update(rkf)
        elif isinstance(item, list):
            # i = iter(item)
            item_dict = dict(zip(range(len(item)), item))
            reconstruction_flags[wholekey] = "list"
            rf = recursively_save_dict_contents_to_group(
                h5file, path + key + delimiter, item_dict
            )
            reconstruction_flags.update(rf)
            # reconstruction_key_flags.update(rkf)
        elif isinstance(item, tuple):
            # i = iter(item)
            item_dict = dict(zip(range(len(item)), item))
            reconstruction_flags[wholekey] = "tuple"
            rf = recursively_save_dict_contents_to_group(
                h5file, path + key + delimiter, item_dict
            )
            reconstruction_flags.update(rf)
        else:
            logger.info("Saving type {} with json".format(type(item)))
            import json

            jitem = json.dumps(item)
            h5file[path + key] = jitem
            reconstruction_flags[wholekey] = "json_value"
            # raise ValueError('Cannot save %s type'%type(item))
    return reconstruction_flags  # , reconstruction_key_flags


def load_dict_from_hdf5(filename):
    """
    ....
    """
    with h5py.File(filename, "r") as h5file:
        return recursively_load_dict_contents_from_group(h5file, "/")


def recursively_load_dict_contents_from_group(h5file, path):
    """
    ....
    """
    rf = h5file["_reconstruction_flags"]
    # rkf = h5file["_reconstruction_key_flags"]
    delimiter = '/'
    ans = {}
    for key, item in h5file[path].items():
        dest_key = key
        # if key in ("_reconstruction_flags", "_reconstruction_key_flags"):
        if key in "_reconstruction_flags":
            continue
        kkey = key + "_key_"
        tkey = key + "_typ_"
        if kkey in rf:
            flag = rf[kkey]
            if flag.value == "json_key":
                import json

                dest_key = json.loads(key)
                # import pickle
                # dest_key = pickle.loads(key.encode("ascii"))
                # logger.debug("unpickling key")

        if tkey in rf:
            flag = rf[tkey][()]
            if flag == b"list":
                dict_to_output = recursively_load_dict_contents_from_group(
                    h5file, path + key + delimiter
                )
                ans[dest_key] = list(dict_to_output.values())
                continue
            if flag == b"tuple":
                dict_to_output = recursively_load_dict_contents_from_group(
                    h5file, path + key + delimiter
                )
                ans[dest_key] = tuple(dict_to_output.values())
                continue
            elif flag == b"json_value":
                import json

                ans[dest_key] = json.loads(item[()])
                continue
            elif flag == b"float":
                ans[dest_key] = float(item[()])
                continue
            elif flag == b"int":
                ans[dest_key] = int(item[()])
                continue

        if isinstance(item, h5py._hl.dataset.Dataset):
            ans[dest_key] = item[()]
        elif isinstance(item, h5py._hl.group.Group):
            ans[dest_key] = recursively_load_dict_contents_from_group(
                h5file, path + key + delimiter
            )
    return ans


if __name__ == "__main__":

    data = {
        "x": "astring",
        "y": np.arange(10),
        "d": {"z": np.ones((2, 3)), "b": b"bytestring"},
    }
    print(data)
    filename = "test.h5"
    save_dict_to_hdf5(data, filename)
    dd = load_dict_from_hdf5(filename)
    print(dd)
    # should test for bad type
