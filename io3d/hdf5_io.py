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
    with h5py.File(filename, "w") as h5file:
        rf = recursively_save_dict_contents_to_group(h5file, "/", dic)
        h5_rf = h5file.create_group("_reconstruction_flags")
        # h5_rf = h5file.create_group("_reconstruction_key_flags")
        for k, v in rf.items():
            h5_rf.create_dataset("/_reconstruction_flags" + k, data=v)
        # for k, v in rfk.items():
        #     h5_rf.create_dataset("/_reconstruction_key_flags" + k, data=v)


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """
    ....
    """
    reconstruction_flags = {}
    # reconstruction_key_flags = {}
    for key, item in dic.items():
        if type(key) is not str:
            # import pickle
            # key = pickle.dumps(key).decode("ascii")
            import json

            key = json.dumps(key)

            reconstruction_flags[path + key + "_key_/"] = "json_key"
        if item is None:
            import json

            jitem = json.dumps(item)
            h5file[path + key] = jitem
            reconstruction_flags[path + key + "_typ_/"] = "json_value"
        elif isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes)):
            h5file[path + key] = item
        elif isinstance(item, (float)):
            h5file[path + key] = item
            reconstruction_flags[path + key + "_typ_/"] = "float"
        elif isinstance(item, (int)):
            h5file[path + key] = item
            reconstruction_flags[path + key + "_typ_/"] = "int"
        elif isinstance(item, dict):
            rf = recursively_save_dict_contents_to_group(h5file, path + key + "/", item)
            reconstruction_flags.update(rf)
            # reconstruction_key_flags.update(rkf)
        elif isinstance(item, list):
            # i = iter(item)
            item_dict = dict(zip(range(len(item)), item))
            wholekey = path + key + "_typ_/"
            reconstruction_flags[wholekey] = "list"
            rf = recursively_save_dict_contents_to_group(
                h5file, path + key + "/", item_dict
            )
            reconstruction_flags.update(rf)
            # reconstruction_key_flags.update(rkf)
        elif isinstance(item, tuple):
            # i = iter(item)
            item_dict = dict(zip(range(len(item)), item))
            wholekey = path + key + "_typ_/"
            reconstruction_flags[wholekey] = "tuple"
            rf = recursively_save_dict_contents_to_group(
                h5file, path + key + "/", item_dict
            )
            reconstruction_flags.update(rf)
        else:
            logger.info("Saving type {} with json".format(type(item)))
            import json

            jitem = json.dumps(item)
            h5file[path + key] = jitem
            reconstruction_flags[path + key + "_typ_/"] = "json_value"
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
            flag = rf[tkey]
            if flag.value == "list":
                dict_to_output = recursively_load_dict_contents_from_group(
                    h5file, path + key + "/"
                )
                ans[dest_key] = list(dict_to_output.values())
                continue
            if flag.value == "tuple":
                dict_to_output = recursively_load_dict_contents_from_group(
                    h5file, path + key + "/"
                )
                ans[dest_key] = tuple(dict_to_output.values())
                continue
            elif flag.value == "json_value":
                import json

                ans[dest_key] = json.loads(item.value)
                continue
            elif flag.value == "float":
                ans[dest_key] = float(item.value)
                continue
            elif flag.value == "int":
                ans[dest_key] = int(item.value)
                continue

        if isinstance(item, h5py._hl.dataset.Dataset):
            ans[dest_key] = item.value
        elif isinstance(item, h5py._hl.group.Group):
            ans[dest_key] = recursively_load_dict_contents_from_group(
                h5file, path + key + "/"
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
