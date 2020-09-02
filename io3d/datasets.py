#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Module is used for visualization of segmentation stored in pkl, dcm and other files.
"""

from loguru import logger
# import logging
#
# logger = logging.getLogger(__name__)
import os.path
import sys
import argparse
import numpy as np
import zipfile
import glob
import os.path as op
import csv
import urllib.request
import io
from pathlib import Path
# import io3d
from . import cachefile as cachef
from . import datareader

# if sys.version_info < (3, 0):
#     import urllib as urllibr
# else:
#     import urllib.request as urllibr


# you can get hash from command line with:
#  python imtools/sample_data.py -v sliver_training_001
# local_dir = "~/data/medical/orig/"
local_dir = "~/data/"
# vessels.pkl nejprve vytvoří prázný adresář s názvem vessels.pkl, pak jej při rozbalování zase smaže
__url_home = "http://home.zcu.cz/~mjirik/lisa/testdata/sample-extra-data/"
__url_server = "http://147.228.240.61/queetech/"
__url_server = "http://home.zcu.cz/~mjirik/lisa/"
__hash_path_prefix = ""
__rel_medical_orig_path = "medical/orig/"
__local_dataset_specific_dir_prefix = "local_dataset_specific_dir_"
__datasets_csv_url = "https://raw.githubusercontent.com/mjirik/io3d/master/datasets/datasets.csv"

# Tenhle hash znamená prázdný seznam souborů 'd41d8cd98f00b204e9800998ecf8427e'
data_urls = {
    "head": [
        __url_server + "sample_data/head.zip",
        "89e9b60fd23257f01c4a1632ff7bb800",
        __hash_path_prefix + "/matlab",
    ],
    "jatra_06mm_jenjatra": [
        __url_server + "sample_data/jatra_06mm_jenjatra.zip",
        None,
        "jatra_06mm_jenjatra/*.dcm",
    ],
    "jatra_5mm": [
        __url_server + "sample_data/jatra_5mm.zip",
        "1b9039ffe1ff9af9caa344341c8cec03",
        __hash_path_prefix + "jatra_5mm/*.dcm",
    ],
    "exp": [__url_server + "sample_data/exp.zip", "74f2c10b17b6bd31bd03662df6cf884d"],
    "sliver_training_001": [
        __url_server + "sample_data/sliver_training_001.zip",
        "d64235727c0adafe13d24bfb311d1ed0",
        "liver*001.*",
    ],
    "volumetrie": [
        __url_server + "sample_data/volumetrie.zip",
        "6b2a2da67874ba526e2fe00a78dd19c9",
    ],
    "vessels.pkl": [
        __url_server + "sample_data/vessels.pkl.zip",
        "698ef2bc345bb616f8d4195048538ded",
    ],
    "biodur_sample": [
        __url_server + "sample_data/biodur_sample.zip",
        "d459dd5b308ca07d10414b3a3a9000ea",
        "biodur_sample/*.tiff"
    ],
    "gensei_slices": [
        __url_server + "sample_data/gensei_slices.zip",
        "ef93b121add8e4a133bb086e9e6491c9",
        # __hash_path_prefix
    ],
    "arina": [
        __url_server + "anwa/arina.mp4",
        '913b49be5aa27b8519aa101b5df869bb',
        "arina.mp4",
        "animals/orig/",
        ],
    "exp_small": [
        __url_server + "sample_data/exp_small.zip",
        "0526ba8ea363fe8b5227f5807b7aaca7",
        # __hash_path_prefix
    ],
    "vincentka": [
        __url_server + "sample_data/vincentka.zip",
        "a30fdabaa39c5ce032a3223ed30b88e3",
        # __hash_path_prefix
    ],
    "vincentka_sample": [__url_server + "sample_data/vincentka_sample.zip"],
    "SCP003-ndpi": [
        __url_server + "sample_data/SCP003/SCP003.ndpi",
        "c7e74c1487bcaa9061aea1ce5c9b8bc9",
        "SCP003.ndpi",
        __rel_medical_orig_path + "sample_data/SCP003",
    ],
    "SCP003-ndpa": [
        __url_server + "sample_data/SCP003/SCP003.ndpi.ndpa",
        None,
        "SCP003.ndpi.ndpa",
        __rel_medical_orig_path + "sample_data/SCP003",
    ],
    "SCP003": {"package": ["SCP003-ndpi", "SCP003-ndpa"]},
    # "SCP003": [__url_server + "sample_data/SCP003.zip", "001a3ff3831eb87dccc2aa3a55f96152", "SCP0003/SCP003*.ndp?"],
    "donut": [__url_server + "sample_data/donut.zip", None, __hash_path_prefix],
    # alternative linux hash nrn4 'd41d8cd98f00b204e9800998ecf8427e'
    "nrn4": [
        __url_server + "sample_data/nrn4.pklz",
        "ec470d016c31b8d17d09475fa93ad7d2",
        "nrn4.pklz",
        __rel_medical_orig_path + "sample_data/",
    ],
    "nrn10": [
        __url_server + "sample_data/nrn10.pklz",
        None,
        "nrn4.pklz",
        __rel_medical_orig_path + "sample_data/",
    ],
    # "io3d_sample_data": [__url_server + "sample-extra-data/io3d_sample_data.zip"],
    "io3d_sample_data": [__url_server + "sample_data/io3d_sample_data.zip", None, __hash_path_prefix],
    "lisa": {
        "package": [
            "donut",
            "vincentka_sample",
            "exp_small",
            "gensei_slices",
            "biodur_sample",
            "vessels.pkl",
            "sliver_training_001",
            "jatra_5mm",
            "head",
            "volumetrie",
        ]
    },
    # "3Dircadb1": ["http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.zip", None, None, "ircad/*[!p]/*[!pfg]"],
    "3Dircadb1": {
        "package": [
            "3Dircadb1.1",
            "3Dircadb1.2",
            "3Dircadb1.3",
            "3Dircadb1.4",
            "3Dircadb1.5",
            "3Dircadb1.6",
            "3Dircadb1.7",
            "3Dircadb1.8",
            "3Dircadb1.9",
            "3Dircadb1.10",
            "3Dircadb1.11",
            "3Dircadb1.12",
            "3Dircadb1.13",
            "3Dircadb1.14",
            "3Dircadb1.15",
            "3Dircadb1.16",
            "3Dircadb1.17",
            "3Dircadb1.18",
            "3Dircadb1.19",
            "3Dircadb1.20",
        ],
        "path_structure":{

        }

    },
    "3Dircadb1.1": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.1.zip",
        "2f29b5a66946c4d76cbea38fd643e7d2",
        "3Dircadb1.1/**/image_*"
        # "6408942626845de25a36ece2e32600e8", "3Dircadb1.1/**/image_*"
        # '2f29b5a66946c4d76cbea38fd643e7d2'
        #     "1b9039ffe1ff9af9caa344341c8cec03"
    ],
    "3Dircadb1.2": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.2.zip",
        "eff7ff35b7ebc87ce55488549bfc5ee4",
        __hash_path_prefix + "3Dircadb1.2/**/image_*",
    ],
    "3Dircadb1.3": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.3.zip",
        "e5de3e88e062c4c2ee26e53b029aac6d",
        __hash_path_prefix + "3Dircadb1.3/**/image_*",
    ],
    "3Dircadb1.4": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.4.zip",
        "71b9108d25f257e6b295323ec129aafc",
        __hash_path_prefix + "3Dircadb1.4/**/image_*",
    ],
    "3Dircadb1.5": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.5.zip",
        "e3ac71113dc1dd1cb6b0418f98b2e02d",
        __hash_path_prefix + "3Dircadb1.5/**/image_*",
    ],
    "3Dircadb1.6": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.6.zip",
        "79825fd27c3261976ecb2f0f2a7e43f7",
        __hash_path_prefix + "3Dircadb1.6/**/image_*",
    ],
    "3Dircadb1.7": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.7.zip",
        "f74267454be34a8fd6ce9f446528044f",
        __hash_path_prefix + "3Dircadb1.7/**/image_*",
    ],
    "3Dircadb1.8": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.8.zip",
        "b05978969d4e5b4e9169eac2ec6d912c",
        __hash_path_prefix + "3Dircadb1.8/**/image_*",
    ],
    "3Dircadb1.9": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.9.zip",
        "c8c57d9a37e5b6951f7c63fa2cec1e4c",
        __hash_path_prefix + "3Dircadb1.9/**/image_*",
    ],
    "3Dircadb1.10": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.10.zip",
        "3ab9c809148993efa879cbaa60c20a25",
        __hash_path_prefix + "3Dircadb1.10/**/image_*",
    ],
    "3Dircadb1.11": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.11.zip",
        "e0fb55fd031f526a7e77539d709fbff1",
        __hash_path_prefix + "3Dircadb1.11/**/image_*",
    ],
    "3Dircadb1.12": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.12.zip",
        "867b014422550205306477dad3c8725e",
        __hash_path_prefix + "3Dircadb1.12/**/image_*",
    ],
    "3Dircadb1.13": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.13.zip",
        "2f476b9fa26bfb3f28df84288adaf78a",
        __hash_path_prefix + "3Dircadb1.13/**/image_*",
    ],
    "3Dircadb1.14": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.14.zip",
        "7c1035538d2506fb49bdb28942a6900a",
        __hash_path_prefix + "3Dircadb1.14/**/image_*",
    ],
    "3Dircadb1.15": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.15.zip",
        "63dc46d980d5c7b6ef91c7b85afbbb5b",
        __hash_path_prefix + "3Dircadb1.15/**/image_*",
    ],
    "3Dircadb1.16": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.16.zip",
        "ba7dd7f899f9c9a63f5dcb1a2165fb16",
        __hash_path_prefix + "3Dircadb1.16/**/image_*",
    ],
    "3Dircadb1.17": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.17.zip",
        "c6b59e9ea625b2b72348fdbd9cdc4ca3",
        __hash_path_prefix + "3Dircadb1.17/**/image_*",
    ],
    "3Dircadb1.18": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.18.zip",
        "92e63cd6c268efe6f285a8779ddfa437",
        __hash_path_prefix + "3Dircadb1.18/**/image_*",
    ],
    "3Dircadb1.19": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.19.zip",
        "30555382d82ee5057997a48987b0f47b",
        __hash_path_prefix + "3Dircadb1.19/**/image_*",
    ],
    "3Dircadb1.20": [
        "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.20.zip",
        "89790e5e2060a642365ebf8bb1bfa14b",
        __hash_path_prefix + "3Dircadb1.20/**/image_*",
    ],
    "CMU-1": [
        "http://openslide.cs.cmu.edu/download/openslide-testdata/Hamamatsu/CMU-1.ndpi",
        "1f9df18b8dc6403cd2434bfd3cf20c7f",
        __hash_path_prefix + "CMU-1.ndpi",
    ],
    "CMU-1-annotation": [
        __url_server + "sample_data/CMU-1.ndpi.ndpa",
        "f2f70fe432bd9dc3c252540313b92df0",
        __hash_path_prefix + "CMU-1.ndpi.ndpa",
    ],
    "R2D2": [
        # "https://drive.google.com/file/d/1hGeRrU9iOnbwOU-8YqZFx9HiCjvV1y10/view?usp=sharing",
        __url_server + "data/biology/orig/roots/examples/R2D2-20x-1.tif",
        None,
        "R2D2-20x-1.tif",
        "biology/orig/roots/examples/"
        ],
    # není nutné pole, stačí jen string
    # "exp_small": "http://147.228.240.61/queetech/sample_data/exp_small.zip",
}
# cachefile = "~/io3d_cache.yaml"

DATASET_PATH_STRUCTURE = {
    "3Dircadb1": {
        "_": "medical/orig/3Dircadb1.{id}/MASKS_DICOM/{data_type}/",
        "data3d": "medical/orig/3Dircadb1.{id}/PATIENT_DICOM/"
    },
    "sliver07": {
        "data3d": "medical/orig/sliver07/training/liver-orig{id:03d}.mhd",
        "liver": "medical/orig/sliver07/training/liver-seg{id:03d}.mhd",
    }
}


def join_path(*path_to_join, get_root=False, sep_on_end=True, return_as_str=True):
    logger.warning("Function deprecated use joinp instead.")
    return joinp(
        *path_to_join,
        get_root=get_root,
        sep_on_end=sep_on_end,
        return_as_str=return_as_str
    )

def joinp(*path_to_join, get_root=True, sep_on_end=True, return_as_str=False):
    """Join input path to sample data path (usually in ~/lisa_data)

    :param path_to_join: one or more paths
    :param get_root: return dataset root path. If false, the path would be into "medical/orig"
    For backward compatibility set False.
    :param sep_on_end True, False or None. Control the separator on the end of path.
    :param return_as_str: the output can be string or Path (default)
    :return: joined path
    """
    # if "get_root" in kwargs:
    #     get_root = kwargs["get_root"]
    # else:
    #     # default value
    #     get_root = False
    # if
    sdp, path_to_join = dataset_path(get_root=get_root, path_to_join=path_to_join, sep_on_end=sep_on_end)
    # pth = os.path.join(sdp, str(Path(path_to_join)).replace("\\", "/"))
    if path_to_join is not None:
        pth = Path(sdp) / Path(path_to_join)
    else:
        pth = Path(sdp)
    # pth = str(Path(pth))
    logger.debug("sample_data_path=" + str(sdp) + f", path_to_joina={path_to_join}")
    logger.debug("path " + str(pth))
    if return_as_str:
        pth = str(pth)
    else:
        pth = Path(pth)
    return pth

def _update_datasets_url():
    stream = urllib.request.urlopen(__datasets_csv_url)
    content = stream.read().decode(
        "utf-8"
    )
    # fieldnames = ['label', 'url', "hash", 'filename_hash_mask', "local_path"]

    csv_reader = csv.DictReader(io.StringIO(content))
    for row in csv_reader:
        label = row["label"]
        metadata = [row["url"], row["hash"], row["filename_hash_mask"], row["local_path"]]
        data_urls[label] = metadata



def set_dataset_path(path, cache=None, cachefile="~/.io3d_cache.yaml"):
    """Sets path to dataset. Warning: function with side effects!

    :param path: path you want to store dataset
    :param cache: CacheFile object
    :param cachefile: default '~/.io3d_cache.yaml'
    """
    if cachefile is not None:
        cache = cachef.CacheFile(cachefile)
    cache.update("local_dataset_dir", path)


def set_specific_dataset_path(path, key_path_prefix, cache=None, cachefile="~/.io3d_cache.yaml"):
    """Sets path to dataset. Warning: function with side effects!

    :param path: path you want to store dataset
    :param key_path_prefix: specific string to identify the specific path
    :param cache: CacheFile object
    :param cachefile: default '~/.io3d_cache.yaml'
    """
    key_path_prefix = str(Path(key_path_prefix)).replace("\\", "/")
    logger.debug(f"adding specific dataset path prefix: {key_path_prefix}")

    if cachefile is not None:
        cache = cachef.CacheFile(cachefile)
    cache.update(__local_dataset_specific_dir_prefix + key_path_prefix, path)


def read_dataset(
        dataset_label, data_type, id,
        qt_app=None,
        dataplus_format=True,
        gui=False,
        start=0,
        stop=None,
        step=1,
        convert_to_gray=True,
        series_number=None,
        dicom_expected=None,
        **kwargs
):
    """
    Read data in organised way. You need just dataset name. Name of the subset of the dataset and numeric ID.

    :param dataset_label:
    :param data_type:
    :param id:
    :param qt_app:
    :param dataplus_format:
    :param gui:
    :param start:
    :param stop:
    :param step:
    :param convert_to_gray:
    :param series_number:
    :param dicom_expected:
    :param kwargs:
    :return:
    """
    # meta = get_dataset_meta(dataset_label)
    selected_dataset = DATASET_PATH_STRUCTURE[dataset_label]
    pth_fmt_str = selected_dataset[data_type] if data_type in selected_dataset else selected_dataset["_"]
    pth = pth_fmt_str.format(dataset_label=dataset_label, data_type=data_type, id=id)
    datapath = joinp(pth)
    # relative_donwload_dir = meta[3]
    # pth = f"{relative_donwload_dir}/{ds_struct[dataset_label][]}"
    # data_urls[dataset_label]
    # datapath
    dr = datareader.DataReader()
    return dr.Get3DData(
        datapath=datapath,
        qt_app=qt_app,
        dataplus_format=dataplus_format,
        gui=gui,
        start=start,
        stop=stop,
        step=step,
        convert_to_gray=convert_to_gray,
        series_number=series_number,
        use_economic_dtype=True,
        dicom_expected=dicom_expected,
        **kwargs
    )


def delete_specific_dataset_path(key_path_prefix, cache=None, cachefile="~/.io3d_cache.yaml"):
    key_path_prefix = str(Path(key_path_prefix)).replace("\\", "/")
    if cachefile is not None:
        cache = cachef.CacheFile(cachefile)
    cache.delete_key(__local_dataset_specific_dir_prefix + key_path_prefix)


def dataset_path(cache=None, cachefile="~/.io3d_cache.yaml", get_root=None, path_to_join=None, sep_on_end:bool=True):
    """Get dataset path.

    :param cache: CacheFile object
    :param cachefile: cachefile path, default '~/.io3d_cache.yaml'
    :param get_root: In old versions the path was to root/medical/orig. If the get_root is set to True, the path
    :param path_to_join: List. Used if specific dataset is installed in other than normal destination.

    is root.
    :return: path to dataset

    """

    if get_root is None:
        get_root = False
        logger.warning("Deprecated call without get_root. The actual value "
                       "get_root=False will be changed to get_root=True in the future.")
    if get_root:
        append_path = []
    else:
        append_path = ["medical", "orig"]

    local_data_dir = op.expanduser(local_dir)

    if cachefile is not None:
        cache = cachef.CacheFile(cachefile)
        # cache.update('local_dataset_dir', head)
    if cache is not None:
        local_data_dir = cache.get_or_save_default("local_dataset_dir", local_data_dir)

    local_data_dir = op.join(local_data_dir, *append_path)

    if path_to_join is not None:

        # convert to string
        if type(path_to_join) in(list, tuple):
            path_to_join = "/".join(path_to_join).replace("\\","/")

        if get_root:
            sappend_path = "/".join(append_path).replace("\\", "/")
            if sep_on_end == True and len(sappend_path) > 0 and sappend_path[-1] != "/":
                sappend_path = sappend_path + "/"

            elif sep_on_end == False and len(sappend_path) > 0 and sappend_path[-1] == "/":
                sappend_path = sappend_path[:-1]
            path_to_join =  sappend_path + path_to_join


        new_path_to_join = Path(path_to_join)
        if cache is not None:
            pths = [Path(path_to_join)] + [pth for pth in Path(path_to_join).parents]
            for pth in reversed(pths):
                spth = str(pth).replace("\\","/")
                key = __local_dataset_specific_dir_prefix + spth
                logger.debug(f"checking for key {key}")
                val = cache.get_or_none(key)
                if val is not None:
                    local_data_dir = val
                    logger.debug(f"found value {val}")
                    new_path_to_join = Path(path_to_join).relative_to(Path(spth))
                    logger.debug(f"path_to_join={path_to_join}")
                    logger.debug(f"spth={spth}")
                    logger.debug(f"new_path_to_join={new_path_to_join}, npth.resolve={new_path_to_join.resolve()}")
                    if str(new_path_to_join) == ".":
                        # because Path(".") resolve is ABSOLUTE actual path on
                        # windows
                        new_path_to_join = None
                    else:
                        new_path_to_join = str(new_path_to_join.resolve())
                    if str(new_path_to_join)[0] == "/":
                        # linux hack
                        # on linux resolve everytime add absolute prefix to
                        # path
                        new_path_to_join = str(Path(new_path_to_join).relative_to(Path("").absolute()))
                    # new_path_to_join
        out_local_data_dir = op.expanduser(local_data_dir)
        logger.debug(f"returning path={out_local_data_dir} , new_path_to_join={new_path_to_join}")
        return out_local_data_dir,  new_path_to_join # .replace("\\", "/")

    return str(Path(op.expanduser(local_data_dir)))


# def get_sample_data():
#     keys = imtools.sample_data.data_urls.keys()
#     imtools.sample_data.get_sample_data(keys, sample_data_path())

def get_data_url(label):
    """
    Based on label return raw_metadata from url table
    :param label:
    :return:
    """
    if label in data_urls:
        return data_urls[label]
    else:
        return None

# noinspection PyUnboundLocalVariable
def get_dataset_meta(label:str):
    """Gives you metadata for dataset chosen via 'label' param

    :param label: label = key in data_url dict (that big dict containing all possible datasets)
    :return: tuple (data_url, url, expected_hash, hash_path, relative_download_dir)
    relative_download_dir says where will be downloaded the file from url and eventually unzipped

    """
    # check for url
    if label.find(":") > 0:
        logger.info("URL detected")
        splitted = label.split(":")
        if len(splitted) > 3:
            logger.warning("There should be just two ':' symbols in url. <protocol>:<url>:<local path>")
        if len(splitted) > 2:
            pth = splitted.pop(-1)
        else:
            pth = ""
        url = ":".join(splitted)
        data_url = [url, None, ".", pth]
    else:
        # data_url = data_urls[label]
        data_url = get_data_url(label)

    if data_url is None:
        raise ValueError(f"Label '{label}' not found.")

    if type(data_url) == str:
        # back compatibility
        data_url = [data_url]
    if type(data_url) == list:
        data_url.extend([None, None, None, None])
        data_url = data_url[:4]
        url, expected_hash, hash_path, relative_donwload_dir = data_url
        if hash_path is None:
            hash_path = label
    # elif type(data_url) == dict:

    if relative_donwload_dir is None:
        relative_donwload_dir = "medical/orig"

    # return data_url, url, expected_hash, hash_path, relative_donwload_dir
    return url, expected_hash, hash_path, relative_donwload_dir


# noinspection PyTypeChecker
def _expand_dataset_packages(dataset_label_dict):
    """Returns list of possible packages contained in dataset, in case the dataset is multi dataset, eg. 'lisa'.

    In case the param is not pointing to multidataset returns only that label in a list.

    :param str dataset_label_dict: label of multi dataset
    :return: list of labels
    """
    new_dataset_label_dict = []
    for label in dataset_label_dict:
        if label in data_urls:
            dataset_metadata = data_urls[label]
            if type(dataset_metadata) == dict and "package" in dataset_metadata:
                # package
                new_dataset_label_dict.extend(dataset_metadata["package"])
            else:
                # standard dataset
                new_dataset_label_dict.append(label)
        else:
            # potential url will be checked later
            new_dataset_label_dict.append(label)
    return new_dataset_label_dict


def download(dataset_label=None, destination_dir=None, dry_run=False):
    """Download sample data by data label. Warning: function with side effect!

    Labels can be listed by sample_data.data_urls.keys(). Returns downloaded files.

    :param dataset_label: label of data. If it is set to None, all data are downloaded
    :param destination_dir: output dir for data
    :param dry_run: runs function without downloading anything
    """
    _update_datasets_url()

    if dataset_label is None:
        dataset_label = data_urls.keys()

    if type(dataset_label) == str:
        dataset_label = [dataset_label]
    retval_list_of_output_dist = []
    dataset_label = _expand_dataset_packages(dataset_label)

    for label in dataset_label:
        # make all data:url have length 3
        url, expected_hash, hash_path_suffix, relative_download_dir = get_dataset_meta(
            label
        )
        logger.debug(f"dataset_label={dataset_label}")
        logger.debug(f"hash_path_suffix={hash_path_suffix}, relative_download_dir={relative_download_dir}")

        logger.info("input destination dir: {}".format(destination_dir))
        if destination_dir is None:
            label_destination_dir = join_path(relative_download_dir, get_root=True, sep_on_end=False)
        else:
            destination_dir = op.expanduser(destination_dir)
            label_destination_dir = op.join(destination_dir, relative_download_dir)
        logger.info("destination dir: {}".format(destination_dir))
        logger.info("label destination dir: {}".format(label_destination_dir))

        if not op.exists(label_destination_dir):
            logger.debug("creating directory {}".format(label_destination_dir))
            os.makedirs(label_destination_dir)

        if hash_path_suffix is None:
            hash_path_suffix = label

        path_to_hash = os.path.join(label_destination_dir, hash_path_suffix)
        try:
            computed_hash = checksum(path_to_hash)
        except Exception as e:
            # there is probably no checksumdir module
            logger.warning(e)
            logger.warning("problem with sample_data.checksum()")
            computed_hash = None

        # None,
        logger.info("dataset: '" + label + "'")
        # logger.info("path to hash: {}".format(path_to_hash))
        logger.info("expected hash:   '" + str(expected_hash) + "'")
        if expected_hash == "d41d8cd98f00b204e9800998ecf8427e":
            logger.warning("Expected hash is equal to hash of empty file list.")
        logger.info("initial hash:    '" + str(computed_hash) + f"' in path: {path_to_hash}")
        if computed_hash == "d41d8cd98f00b204e9800998ecf8427e":
            logger.warning("Computed hash is equal to hash of empty file list.")
        if (computed_hash is not None) and (expected_hash == computed_hash):
            logger.info("match ok - no download needed")
        else:
            logger.info("downloading")
            if not dry_run:
                downzip(url, destination=label_destination_dir)
                logger.info("finished")
                logger.debug(f"label_destination_dir={label_destination_dir}")
                logger.debug(f"hash_path_suffix= {hash_path_suffix}")
                new_hash_path = os.path.join(label_destination_dir, hash_path_suffix)
                downloaded_hash = checksum(
                    new_hash_path
                )
                logger.info(f"downloaded hash: '" + str(downloaded_hash) + f"' in path: {new_hash_path}")
                if downloaded_hash != expected_hash:
                    logger.warning(
                        "downloaded hash is different from expected hash\n"
                        + "expected hash: '"
                        + str(expected_hash)
                        + "'\n"
                        + "downloaded hash: '"
                        + str(downloaded_hash)
                        + "'\n"
                    )
            else:
                logger.debug("dry run")
        retval_list_of_output_dist.append(label_destination_dir)
    return retval_list_of_output_dist



# # NOTE(mareklovci): I suppose, this isn't working at all
# def get_old(dataset_label, data_id, destination_dir=None):
#     """Get the 3D data from specified dataset with specified id.
#
#     Download data if necessary.
#
#     :param dataset_label:
#     :param data_id: integer or wildcards file pattern
#     :param destination_dir:
#     :return:
#     """
#     # TODO implement
#     if destination_dir is None:
#         destination_dir = op.join(dataset_path(get_root=True), "medical", "orig")
#
#     destination_dir = op.expanduser(destination_dir)
#     data_url, url, expected_hash, hash_path, relative_output_path = get_dataset_meta(
#         dataset_label
#     )
#     paths = glob.glob(os.path.join(destination_dir, hash_path))
#     paths.sort()
#     import fnmatch
#
#     print(paths)
#     print(data_id)
#     pathsf = fnmatch.filter(paths, data_id)
#     print(pathsf)
#     datap = datareader.read(pathsf[0], dataplus_format=True)
#     return datap


# NOTE(mareklovci - 2018_05_14): work in progress
# noinspection PyUnusedLocal
def get(dataset_label, series_number=None, *args, **kwargs):
    """

    :param dataset_label: label from data_urls
    :param series_number: Series identification in study.
    :param args:
    :param kwargs:
    :return:
    """

    # relative path in the datasets
    relative_path_extracted_from_data_urls = ""
    datapath = join_path(
        relative_path_extracted_from_data_urls, "medical", "data", get_root=True
    )
    # read 3D data from datapath
    datap = datareader.read(
        datapath, series_number=series_number, dataplus_format=True, *args, **kwargs
    )
    return datap


# noinspection PyProtectedMember
def checksum(path, hashfunc="md5"):
    """Return checksum of files given by path.

    Wildcards can be used in check sum. Function is strongly dependent on checksumdir package by 'cakepietoast'.

    :param path: path of files to get hash from
    :param hashfunc: function used to get hash, default 'md5'
    :return: (str) hash of the file/files given by path
    """
    import checksumdir

    hash_func = checksumdir.HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError("{} not implemented.".format(hashfunc))

    if os.path.isdir(path):
        return checksumdir.dirhash(path, hashfunc=hashfunc)

    hashvalues = []
    path_list = list(sorted(glob.glob(path)))
    logger.debug("path_list: len: %i", len(path_list))
    if len(path_list) > 0:
        logger.debug("first ... last: %s ... %s", str(path_list[0]), str(path_list[-1]))

    for path in path_list:
        if os.path.isfile(path):
            hashvalues.append(checksumdir._filehash(path, hashfunc=hash_func))
    logger.debug("one hash per file: len: %i", len(hashvalues))
    if len(path_list) > 0:
        logger.debug(
            "first ... last: %s ... %s", str(hashvalues[0]), str(hashvalues[-1])
        )
    checksum_hash = checksumdir._reduce_hash(hashvalues, hashfunc=hash_func)
    logger.debug("total hash: {}".format(str(checksum_hash)))
    return checksum_hash


def generate_donut():
    """Generate donut like shape with stick inside

    :return: dict {'data3d': '', 'segmentation': '', 'voxelsize_mm': ''}
    """
    segmentation = np.zeros([20, 30, 40])
    # generate test data
    segmentation[6:10, 7:24, 10:37] = 1
    segmentation[6:10, 7, 10] = 0
    segmentation[6:10, 23, 10] = 0
    segmentation[6:10, 7, 36] = 0
    segmentation[6:10, 23, 36] = 0
    segmentation[2:18, 12:19, 18:28] = 2

    data3d = segmentation * 100 + np.random.random(segmentation.shape) * 30
    voxelsize_mm = [3, 2, 1]

    datap = {
        "data3d": data3d,
        "segmentation": segmentation,
        "voxelsize_mm": voxelsize_mm,
    }
    # io3d.write(datap, "donut.pklz")
    return datap


def generate_abdominal(
    size=100,
    liver_intensity=100,
    noise_intensity=20,
    portal_vein_intensity=130,
    spleen_intensity=90,
):
    """Create scaleable artificial abdominal like data. Outputs a cube.

    {0: nothing, 1: liver, 2: portal_vein, 17: spleen}

    :param size: the length of the cube edge
    :param liver_intensity: "luminosity" of liver
    :param noise_intensity: adding noise to data
    :param portal_vein_intensity: "luminosity" of portal vein
    :param spleen_intensity: "luminosity" of spleen
    :return: {'data3d': '', 'segmentation': '', 'voxelsize_mm': '', 'seeds': '', 'slab': ''}
    """
    boundary = int(size / 4)
    voxelsize_mm = [1.0, 1.5, 1.5]
    slab = {"liver": 1, "porta": 2, "spleen": 17}

    segmentation = np.zeros([size, size, size], dtype=np.uint8)
    segmentation[
        boundary:-boundary, boundary : -2 * boundary, 2 * boundary : -boundary
    ] = slab["liver"]
    segmentation[
        :, boundary * 2 : boundary * 2 + 5, boundary * 2 : boundary * 2 + 5
    ] = slab["porta"]
    segmentation[
        :, boundary * 2 : boundary * 2 + 5, boundary * 2 : boundary * 2 + 5
    ] = slab["porta"]
    segmentation[:, -5:, -boundary:] = 17
    seeds = np.zeros([size, size, size], dtype=np.uint8)
    seeds[
        boundary + 1 : boundary + 4,
        boundary + 1 : boundary + 4,
        2 * boundary + 1 : 2 * boundary + 4,
    ] = 1

    noise = (np.random.random(segmentation.shape) * noise_intensity).astype(np.int)
    data3d = np.zeros(segmentation.shape, dtype=np.int)
    data3d[segmentation == 1] = liver_intensity
    data3d[segmentation == 2] = portal_vein_intensity
    data3d[segmentation == 17] = spleen_intensity
    data3d += noise
    datap = {
        "data3d": data3d,
        "segmentation": segmentation,
        "voxelsize_mm": voxelsize_mm,
        "seeds": seeds,
        "slab": slab,
    }
    return datap


def generate_round_data(
    sz=32, offset=0, radius=7, seedsz=3, add_object_without_seeds=False
):
    """
    Generate data with two sphere objects.
    :param sz: output data shape is [sz, sz+1, sz+2]
    :param offset:
    :param radius:
    :param seedsz:
    :param add_object_without_seeds: Add also one cube-like object in the corner.
    :return:
    """

    import scipy.ndimage

    # seedsz= int(sz/10)
    space = 2
    seeds = np.zeros([sz, sz + 1, sz + 2], dtype=np.int8)
    xmin = radius + seedsz + offset + 2
    ymin = radius + seedsz + offset + 6
    seeds[offset + 12, xmin + 3 : xmin + 7 + seedsz, ymin : ymin + 2] = 1
    seeds[offset + 20, xmin + 7 : xmin + 12 + seedsz, ymin + 5 : ymin + 7] = 1

    # add temp seed
    if add_object_without_seeds:
        seeds[-3, -3, -3] = 1
    img = np.ones([sz, sz + 1, sz + 2])
    img = img - seeds

    seeds[2 : 10 + seedsz, 2 : 9 + seedsz, 2 : 3 + seedsz] = 2

    # remove temo seed
    if add_object_without_seeds:
        seeds[-3, -3, -3] = 0

    img = scipy.ndimage.morphology.distance_transform_edt(img)
    segm = img < radius
    img = (100 * segm + 80 * np.random.random(img.shape)).astype(np.uint8)
    return img, segm, seeds


def generate_synthetic_liver(return_dataplus=False):
    """
    Create synthetic data. There is some liver and porta -like object.
    :return data3d, segmentation, voxelsize_mm, slab, seeds_liver, seeds_porta:
    """
    # data
    slab = {"none": 0, "liver": 1, "porta": 2}
    voxelsize_mm = np.array([1.0, 1.0, 1.2])

    segm = np.zeros([80, 256, 250], dtype=np.int16)

    # liver
    segm[30:60, 70:180, 40:190] = slab["liver"]

    # porta
    segm[40:45, 120:130, 70:190] = slab["porta"]
    segm[41:44, 122:127, 68:70] = slab[
        "porta"
    ]  # hack to fix stability of skeleton algorithm
    #
    segm[40:45, 80:130, 100:110] = slab["porta"]
    segm[42:44, 77:80, 103:106] = slab[
        "porta"
    ]  # hack to fix stability of skeleton algorithm
    # segm[41:44, 78:80, 101:109] = slab['porta']
    # vertical branch under main branch
    segm[40:44, 120:170, 130:135] = slab["porta"]

    data3d = np.zeros(segm.shape)
    data3d[segm == slab["liver"]] = 146
    data3d[segm == slab["porta"]] = 206
    noise = np.random.normal(0, 10, segm.shape)  # .astype(np.int16)
    data3d = (data3d + noise).astype(np.int16)

    seeds_liver = np.zeros(data3d.shape, np.int8)
    seeds_liver[40:55, 90:120, 70:110] = 1
    seeds_liver[30:45, 190:200, 40:90] = 2

    seeds_porta = np.zeros(data3d.shape, np.int8)
    seeds_porta[40:45, 121:139, 80:95] = 1

    if return_dataplus:
        datap = {
            "data3d": data3d,
            "voxelsize_mm": voxelsize_mm,
            "slab": slab,
            "seeds_liver": seeds_liver,
            "seeds_porta": seeds_porta,
            "segmentation": segm,
        }
        return datap
    else:
        return data3d, segm, voxelsize_mm, slab, seeds_liver, seeds_porta


def _get_face2(shape=None, face_r=1.0, smile_r1=0.5, smile_r2=0.7, eye_r=0.2):
    """
    Create 2D binar face
    :param shape:
    :param face_r:
    :param smile_r1:
    :param smile_r2:
    :param eye_r:
    :return:
    """

    # data3d = np.zeros([1,7,7], dtype=np.int16)
    if shape is None:
        shape = [32, 32]

    center = (np.asarray(shape) - 1) / 2.0
    r = np.min(center) * face_r

    # np.min(np.asarray(shape) / 2.0)
    # shape = data3d.shape[1:]
    # data3d[center[0], center[1], center[2]] = 1
    x, y = np.meshgrid(range(shape[1]), range(shape[0]))

    head = (x - center[0]) ** 2 + (y - center[1]) ** 2 < r ** 2

    smile = (
        ((x - center[0]) ** 2 + (y - center[1]) ** 2 < (r * smile_r2) ** 2)
        & (y > (center[1] + 0.3 * r))
        & ((x - center[0]) ** 2 + (y - center[1]) ** 2 >= (r * smile_r1) ** 2)
    )
    smile
    e1c = center + r * np.array([-0.35, -0.2])
    e2c = center + r * np.array([0.35, -0.2])

    eyes = (x - e1c[0]) ** 2 + (y - e1c[1]) ** 2 <= (r * eye_r) ** 2
    eyes += (x - e2c[0]) ** 2 + (y - e1c[1]) ** 2 <= (r * eye_r) ** 2

    face = head & ~smile & ~eyes
    return face


def generate_face(shape=None, face_r=1.0, smile_r1=0.5, smile_r2=0.7, eye_r=0.2):
    """
    Create 2D or 3D binar data with smile face.

    :param shape: 2D or 3D shape of data
    :param face_r:
    :param smile_r1:
    :param smile_r2:
    :param eye_r:
    :return: binar ndarray
    """
    # TODO add axis (ax=0)
    if shape is None:
        shape = [32, 32]
    nd = len(shape)
    if nd == 2:
        sh2 = shape
    else:
        sh2 = shape[1:]
    fc2 = _get_face2(
        sh2, face_r=face_r, smile_r1=smile_r1, smile_r2=smile_r2, eye_r=eye_r
    )

    if nd == 2:
        return fc2
    else:
        fc3 = np.zeros(shape)
        for i in range(fc3.shape[0]):
            fc3[i, :, :] = fc2
        return fc3


def sliver_reader(
    filename_end_mask="*[0-9].mhd",
    sliver_reference_dir="~/data/medical/orig/sliver07/training/",
    read_orig=True,
    read_seg=False,
):
    """Generator for reading sliver data from directory structure.

    :param filename_end_mask: file selection can be controlled with this parameter
    :param sliver_reference_dir: directory with sliver .mhd and .raw files
    :param read_orig: read image data if is set True
    :param read_seg: read segmentation data if is set True
    :return: tuple (numeric_label, vs_mm, oname, orig_data, rname, ref_data)
    """
    sliver_reference_dir = op.expanduser(sliver_reference_dir)
    orig_fnames = glob.glob(sliver_reference_dir + "*orig" + filename_end_mask)
    ref_fnames = glob.glob(sliver_reference_dir + "*seg" + filename_end_mask)

    orig_fnames.sort()
    ref_fnames.sort()
    for i in range(0, len(orig_fnames)):
        oname = orig_fnames[i]
        rname = ref_fnames[i]
        vs_mm = None
        ref_data = None
        orig_data = None
        if read_orig:
            orig_data, metadata = datareader.read(oname, dataplus_format=False)
            vs_mm = metadata["voxelsize_mm"]
        if read_seg:
            ref_data, metadata = datareader.read(rname, dataplus_format=False)
            vs_mm = metadata["voxelsize_mm"]

        import re

        numeric_label = re.search(r".*g(\d+)", oname).group(1)
        out = (numeric_label, vs_mm, oname, orig_data, rname, ref_data)
        yield out


def remove(local_file_name):
    """Function attempts to remove file, if failure occures -> print exception

    :param local_file_name: name of file to remove
    """
    try:
        os.remove(local_file_name)
    except Exception as e:
        print(
            "Cannot remove file '" + local_file_name + "'. Please remove it manually."
        )
        print(e)


def get_labels():
    _update_datasets_url()
    return list(sorted(data_urls.keys()))


def downzip(url, destination="./sample_data/"):
    """Download, unzip and delete. Warning: function with strong side effects!

    Returns downloaded data.

    :param str url: url from which data should be donloaded
    :param destination: destination to which data should be downloaded
    """

    # url = "http://147.228.240.61/queetech/sample_data/jatra_06mm_jenjatra.zip"
    logmsg = "downloading from '" + url + "' to '" + destination + "'"
    print(logmsg)
    logger.info(logmsg)
    tmp_filename = url[url.rfind("/") + 1 :]
    # tmp_filename = "tmp.zip"
    # urllibr.urlretrieve(url, zip_file_name)
    from . import network

    network.download_file(url, destination, filename=tmp_filename)
    zip_file_name = os.path.join(destination, tmp_filename)
    base, ext = op.splitext(tmp_filename)
    # print(ext)
    # print(tmp_filename)
    if ext in (".zip"):
        unzip_recursive(zip_file_name)
    # unzip_one(local_file_name)


# def unzip_all(path):
#     """ Unzip all .zip files packed in other .zip in path recusively.
#
#     :param path:
#     :return:
#     """
#
#     ziplist = glob.glob(op.join(path, '*.zip'))
#     while len(ziplist) > 0:
#     # for local_file_name in ziplist:
#         local_file_name = ziplist[0]
#         unzip_one(local_file_name)
#         ziplist = glob.glob(op.join(path, '*.zip'))


def unzip_one(local_file_name):
    """Unzips one file and deletes it. Warning: function with side effects!

    :param str local_file_name: file name of zip file
    :return: list of archive members by name.
    """
    local_file_name = op.expanduser(local_file_name)
    destination = op.dirname(local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    namelist = datafile.namelist()
    datafile.extractall(destination)
    datafile.close()
    remove(local_file_name)

    fullnamelist = []
    for fn in namelist:
        fullnamelist.append(op.join(destination, fn))
    return fullnamelist


def unzip_recursive(zip_file_name):
    """Unzip file with all recursive zip files inside and delete zip files after that.

    :param zip_file_name: file name of zip file
    :return: list of archive members by name.
    """
    logger.debug("unzipping " + zip_file_name)
    fnlist = unzip_one(zip_file_name)
    for fn in fnlist:
        if zipfile.is_zipfile(fn):
            local_fnlist = unzip_recursive(fn)
            fnlist.extend(local_fnlist)
    return fnlist


class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)


def main(turn_on_logging=False):
    if turn_on_logging:
        pass
    else:
        logger.add(sys.stderr, level="INFO")

    # logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(description="Work on dataset")
    parser.register("action", "extend", ExtendAction)
    parser.add_argument(
        "-l",
        "--labels",
        metavar="N",
        nargs="+",
        action="extend",
        default=None,
        help="Get sample data",
    )
    parser.add_argument(
        "-L",
        "--print_labels",
        action="store_true",
        default=False,
        help="print all available labels",
    )
    parser.add_argument(
        "-c",
        "--checksum",  # action="store_true",
        default=None,
        help="Get hash for requested path",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="more messages"
    )
    parser.add_argument(
        "-d", "--debug", default=None, help="Set debug level"  # action="store_true",
    )
    parser.add_argument(
        "-o",
        "--destination_dir",
        default=op.join(dataset_path(get_root=True)),
        help="Set output directory. If not used, the standard dataset dir is used",
    )
    parser.add_argument(
        "-sdp", "--set_dataset_path", default=None, help="Set standard dataset path"
    )
    parser.add_argument(
        "-ssdp", "--set_specific_dataset_path", nargs=2, default=None,
        help="Set specific dataset path. First argument is path (e.g. c:/data), second is key prefix (e.g. bio/flowers)."
    )
    parser.add_argument(
        "-gdp",
        "--get_dataset_path",
        default=False,
        action="store_true",
        help="Get standard dataset path",
    )
    parser.add_argument(
        "--dry_run", action="store_true", default=False, help="Do not download"
    )

    args = parser.parse_args()

    # if args.get_sample_data == False and args.install == False and args.build_gco == False:
    # default setup is install and get sample data
    #        args.get_sample_data = True
    #        args.install = True
    #        args.build_gco = False
    if args.verbose:
        logger.add(sys.stderr, level="INFO")
    if args.debug is not None:
        logger.add(sys.stderr, level="DEBUG")

    if args.set_dataset_path is not None:
        set_dataset_path(args.set_dataset_path)
        logger.info("Dataset path changed")
        return

    if args.get_dataset_path:
        # dp = dataset_path()
        dp = (op.join(dataset_path(get_root=True)))
        logger.info(dp)
        print(dp)
        # logger.info("Dataset path changed")
        return

    if args.set_specific_dataset_path is not None:
        set_specific_dataset_path(
            path=args.set_specific_dataset_path[0],
            key_path_prefix=args.set_specific_dataset_path[1],
            )

    if args.checksum is not None:
        print(checksum(args.checksum))
        if args.labels is None:
            return
    if args.print_labels:
        print(get_labels())
        return

    if args.labels is not None:
        logger.info("Downloading labels: {}".format(args.labels))
        download(
            args.labels, destination_dir=args.destination_dir, dry_run=args.dry_run
        )

    # submodule_update()


if __name__ == "__main__":
    main(turn_on_logging=False)
