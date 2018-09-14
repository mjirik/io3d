#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
import os

import logging
logger = logging.getLogger(__name__)

import sys
import os.path
import numpy as np
from io import open

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "./extern/sPickle"))

from .dili_subset import ndarray_to_list_in_structure

def old_str_format_to_new(string):
    """
    convert old format style to new style. Works for digits only
    %05d is converted to {:05d}
    :param string:
    :return:
    """
    import re
    return re.sub(r"%(\d*d)", r"{:\1}", string)

def suggest_filename(file_path, exists=None):
    """
    Try if exist path and append number to its end.
    For debug you can set as input if file exists or not.
    """
    import os.path
    import re
    if not isinstance(exists, bool):
        exists = os.path.exists(file_path)

    if exists:
        file_path, file_extension = os.path.splitext(file_path)
        # print(file_path)
        m = re.search(r"\d+$", file_path)
        if m is None:
            # cislo = 2
            new_cislo_str = "2"
        else:
            cislostr = (m.group())
            cislo = int(cislostr) + 1
            file_path = file_path[:-len(cislostr)]
            new_cislo_str = str(cislo)

        file_path = file_path + new_cislo_str + file_extension  # .zfill(2)
        # trorcha rekurze
        file_path = suggest_filename(file_path)

    return file_path


def obj_from_file(filename='annotation.yaml', filetype='auto'):
    ''' Read object from file '''

    if filetype == 'auto':
        _, ext = os.path.splitext(filename)
        filetype = ext[1:]

    if filetype in ('yaml', 'yml'):
        from ruamel.yaml import YAML
        yaml = YAML(typ="unsafe")
        with open(filename, encoding="utf-8") as f:
            obj = yaml.load(f)
        if obj is None:
            obj = {}
        # import yaml
        # with open(filename, encoding="utf-8") as f:
        #     intext = f.read()
        #     obj = yaml.load(intext)
    elif filetype in ('pickle', 'pkl', 'pklz', 'picklezip'):
        fcontent = read_pkl_and_pklz(filename)
        # import pickle
        if sys.version_info[0] < 3:
            import cPickle as pickle
        else:
            import _pickle as pickle
        # import sPickle as pickle
        if sys.version_info.major == 2:
            obj = pickle.loads(fcontent)
        else:
            obj = pickle.loads(fcontent, encoding="latin1")
    else:
        logger.error('Unknown filetype ' + filetype)
    return obj


def read_pkl_and_pklz(filename):
    """
    Try read zipped or not zipped pickle file
    """
    fcontent = None
    try:
        import gzip
        f = gzip.open(filename, 'rb')
        fcontent = f.read()
        f.close()
    except IOError as e:
        # if the problem is in not gzip file
        logger.info("Input gzip exception: " + str(e))
        f = open(filename, 'rb')
        fcontent = f.read()
        f.close()
    except Exception as e:
        # other problem
        import traceback
        logger.error("Input gzip exception: " + str(e))
        logger.error(traceback.format_exc())

    return fcontent


def obj_to_file(obj, filename, filetype='auto', ndarray_to_list=False, squeeze=True):
    '''Writes annotation in file.

    :param filetype:
        auto
        yaml
        pkl, pickle
        pklz, picklezip
    :param ndarray_to_list: convert ndarrays in obj to lists
    :param squeeze: squeeze ndarray

    '''
    # import json
    # with open(filename, mode='w') as f:
    #    json.dump(annotation,f)
    if ndarray_to_list:
        obj = ndarray_to_list_in_structure(obj, squeeze=squeeze)

    # write to yaml
    d = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(d):
        os.makedirs(d)

    if filetype == 'auto':
        _, ext = os.path.splitext(filename)
        filetype = ext[1:]

    if filetype in ('yaml', 'yml'):
        # import yaml
        from ruamel.yaml import YAML
        yaml = YAML(typ="unsafe")
        with open(filename, 'wt', encoding="utf-8") as f:
            yaml.dump(obj, f)
        # if sys.version_info.major == 2:
        #     with open(filename, 'wb') as f:
        #         yaml.dump(obj, f, encoding="utf-8")
        # else:
        #     with open(filename, "w", encoding="utf-8") as f:
        #         yaml.dump(obj, f)
    elif filetype in ('pickle', 'pkl'):
        f = open(filename, 'wb')
        logger.info("filename " + filename)
        # if sys.version_info[0] < 3: import cPickle as pickle
        # else: import _pickle as pickle
        import pickle
        pickle.dump(obj, f, -1)
        f.close
    elif filetype in ('streamingpicklezip', 'spklz'):
        # this is not working :-(
        import gzip
        import sPickle as pickle
        f = gzip.open(filename, 'wb', compresslevel=1)
        # f = open(filename, 'wb')
        pickle.s_dump(obj, f)
        f.close
    elif filetype in ('picklezip', 'pklz'):
        import gzip
        if sys.version_info[0] < 3: import cPickle as pickle
        else: import _pickle as pickle
        f = gzip.open(filename, 'wb', compresslevel=1)
        # f = open(filename, 'wb')
        pickle.dump(obj, f)
        f.close
    elif filetype in('mat'):

        import scipy.io as sio
        sio.savemat(filename, obj)
    else:
        logger.error('Unknown filetype ' + filetype)

def resize_to_shape(data, shape, zoom=None, mode='nearest', order=0):
    """
    Function resize input data to specific shape.

    :param data: input 3d array-like data
    :param shape: shape of output data
    :param zoom: zoom is used for back compatibility
    :mode: default is 'nearest'
    """
    # @TODO remove old code in except part

    try:
        # rint 'pred vyjimkou'
        # aise Exception ('test without skimage')
        # rint 'za vyjimkou'
        import skimage
        import skimage.transform
# Now we need reshape  seeds and segmentation to original size

        segm_orig_scale = skimage.transform.resize(
            data, shape, order=0,
            preserve_range=True,
            mode="constant",
        )

        segmentation = segm_orig_scale
        logger.debug('resize to orig with skimage')
    except:
        import scipy
        import scipy.ndimage
        dtype = data.dtype
        if zoom is None:
            zoom = shape / np.asarray(data.shape).astype(np.double)

        segm_orig_scale = scipy.ndimage.zoom(
            data,
            1.0 / zoom,
            mode=mode,
            order=order
        ).astype(dtype)
        logger.debug('resize to orig with scipy.ndimage')

# @TODO odstranit hack pro oříznutí na stejnou velikost
# v podstatě je to vyřešeno, ale nechalo by se to dělat elegantněji v zoom
# tam je bohužel patrně bug
        # rint 'd3d ', self.data3d.shape
        # rint 's orig scale shape ', segm_orig_scale.shape
        shp = [
            np.min([segm_orig_scale.shape[0], shape[0]]),
            np.min([segm_orig_scale.shape[1], shape[1]]),
            np.min([segm_orig_scale.shape[2], shape[2]]),
        ]
        # elf.data3d = self.data3d[0:shp[0], 0:shp[1], 0:shp[2]]
        # mport ipdb; ipdb.set_trace() # BREAKPOINT

        segmentation = np.zeros(shape, dtype=dtype)
        segmentation[
            0:shp[0],
            0:shp[1],
            0:shp[2]] = segm_orig_scale[0:shp[0], 0:shp[1], 0:shp[2]]

        del segm_orig_scale
    return segmentation


def resize_to_mm(data3d, voxelsize_mm, new_voxelsize_mm, mode='nearest'):
    """
    Function can resize data3d or segmentation to specifed voxelsize_mm
    :new_voxelsize_mm: requested voxelsize. List of 3 numbers, also
        can be a string 'orig', 'orgi*2' and 'orgi*4'.

    :voxelsize_mm: size of voxel
    :mode: default is 'nearest'
    """
    import scipy
    import scipy.ndimage

    if np.all(list(new_voxelsize_mm) == 'orig'):
        new_voxelsize_mm = np.array(voxelsize_mm)
    elif np.all(list(new_voxelsize_mm) == 'orig*2'):
        new_voxelsize_mm = np.array(voxelsize_mm) * 2
    elif np.all(list(new_voxelsize_mm) == 'orig*4'):
        new_voxelsize_mm = np.array(voxelsize_mm) * 4
        # vx_size = np.array(metadata['voxelsize_mm']) * 4

    zoom = voxelsize_mm / (1.0 * np.array(new_voxelsize_mm))
    data3d_res = scipy.ndimage.zoom(
        data3d,
        zoom,
        mode=mode,
        order=1
    ).astype(data3d.dtype)
    return data3d_res

def suits_with_dtype(mn, mx, dtype):
    """
    Check whether range of values can be stored into defined data type.
    :param mn: range minimum
    :param mx: range maximum
    :param dtype:
    :return:
    """
    type_info = np.iinfo(dtype)
    if mx <= type_info.max and mn >= type_info.min:
        return True
    else:
        return False

def use_economic_dtype(data3d, slope=1, inter=0, dtype=None):
    """ Use more economic integer-like dtype if it is possible.

    :param data3d:
    :param dtype: if dtype is not used, the automatic is used
    :return:
    """

    if dtype is None:
        dtype = data3d.dtype
        if issubclass(dtype.type, np.integer):
            mn = data3d.min() * slope + inter
            mx = data3d.max() * slope + inter
            if suits_with_dtype(mn, mx, dtype=np.uint8):
                dtype = np.uint8
            elif suits_with_dtype(mn, mx, dtype=np.int8):
                dtype = np.int8
            elif suits_with_dtype(mn, mx, dtype=np.uint16):
                dtype = np.uint16
            elif suits_with_dtype(mn, mx, dtype=np.int16):
                dtype = np.int16
            elif suits_with_dtype(mn, mx, dtype=np.uint32):
                dtype = np.uint32
            elif suits_with_dtype(mn, mx, dtype=np.int32):
                dtype = np.int32

    # new_data3d = ((np.float(slope) * data3d) + np.float(inter)).astype(dtype)
    if slope == 1 and inter == 0:
        # this can prevent out of memmory
        new_data3d = data3d.astype(dtype)
    else:
        new_data3d = ((slope * data3d) + inter).astype(dtype)
    return new_data3d

