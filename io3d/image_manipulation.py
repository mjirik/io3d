#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
DeprecationWarning("Image_manipulation would be removed from io3d in the future. Use imma.image_manipulation.")
logger.warning("Image_manipulation would be removed from io3d in the future. Use imma.image_manipulation.")
from imma.image_manipulation import *

# import os.path
# import sys
# import numpy as np
# import scipy
# import scipy.ndimage
#
# from io3d import dili
#
# path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/sed3"))
#
#
# def select_labels(segmentation, labels, slab=None):
#     """
#     return ndimage with zeros and ones based on input labels
#
#     :param segmentation: 3D ndimage
#     :param labels: labels to select
#     :param slab: dictionary{string_label: numeric_label}. Allow to use
#     string labels if it is defined
#     :return:
#     """
#
#     if slab is not None:
#         labels = get_nlabels(slab, labels)
#
#     if type(labels) not in (list, np.ndarray):
#         labels = [labels]
#
#     ds = np.zeros(segmentation.shape, np.bool)
#     for lab in labels:
#         dadd = (segmentation == lab)
#
#         ds = ds | dadd
#     if len(labels) == 0:
#         logger.warning("Labels not found in slab.")
#
#     return ds
#
#
# def get_nlabels(slab, labels, labels_meta=None, return_mode="num", return_first=False):
#     """
#     Get one or more labels, create a new one if necessary and return its numeric value.
#
#     Look at the get_nlabel function for more details.
#
#     :param slab:
#     :param labels:
#     :param labels_meta:
#     :param return_mode: "num" or "str" or "both". Both means (numlabel, strlabel).
#     :param return_first: Return just first found label
#     :return:
#     """
#
#     if type(labels) not in (list, np.ndarray):
#         labels = [labels]
#         labels_meta = [labels_meta]
#         return_first = True
#
#     if labels_meta is None:
#         labels_meta = [None] * len(labels)
#
#     nlabels = []
#     for label, label_meta in zip(labels, labels_meta):
#         nlab = get_nlabel(slab, label, label_meta, return_mode=return_mode)
#         nlabels.append(nlab)
#
#     if return_first:
#         nlabels = nlabels[0]
#     return nlabels
#
#
# def get_nlabel(slab, label, label_meta=None, return_mode="num"):
#     """
#     Add label if it is necessery and return its numeric value.
#
#     If "new" keyword is used and no other information is provided, the max + 1 label is created.
#     If "new" keyword is used and additional numeric info is provided, the number is used also as a key.
#     :param return_mode: Set requested label return type. "int", "num", "numeric" or "str" or "both".
#     "both" means (numlabel, strlabel).
#     :param label: string, number or "new"
#     :param label_meta: string, number or "new
#     :return:
#     """
#     numlabel = None
#     strlabel = None
#     if type(label) == str:
#         if label_meta is None:
#             if label not in slab.keys():
#                 free_numeric_label = np.max(list(slab.values())) + 1
#                 if label == "new":
#                     label = str(free_numeric_label)
#                 slab[label] = free_numeric_label
#                 strlabel = label
#                 numlabel = slab[label]
#             else:
#                 strlabel = label
#                 numlabel = slab[label]
#         else:
#             if label == "new":
#                 label = str(label_meta)
#             update_slab(slab, label_meta, label)
#             strlabel = label
#             numlabel = label_meta
#     else:
#         # it is numeric
#         if label_meta is None:
#             if label not in list(slab.values()):
#                 update_slab(slab, label, str(label))
#                 strlabel = str(label)
#             else:
#                 strlabel = dili.dict_find_key(slab, label)
#
#             numlabel = label
#
#         else:
#             if label_meta == "new":
#                 label_meta = str(label)
#             update_slab(slab, label, label_meta)
#             strlabel = label_meta
#             numlabel = label
#             # return label
#
#     if return_mode in ("num", "int", "numeric"):
#         return numlabel
#     elif return_mode == "str":
#         return strlabel
#     elif return_mode == "both":
#         return numlabel, strlabel
#     else:
#         logger.error("Unknown return_mode: " + str(return_mode))
#
#
# def update_slab(slab, numeric_label, string_label):
#     """ Add label to segmentation label dictionary if it is not there yet.
#
#     :param numeric_label:
#     :param string_label:
#     :return:
#     """
#
#     slab_tmp = {string_label: numeric_label}
#     slab.update(slab_tmp)
#     # slab = slab_tmp
#     logger.debug('self.slab')
#     logger.debug(str(slab))
#
#
# def add_slab_label_carefully2(slab, numeric_label, string_label):
#     """ Add label to slab if it is not there yet.
#
#     :param numeric_label:
#     :param string_label:
#     :return:
#     """
#     # todo implement
#     # if numeric_label in
#     pass
#
#
# def add_missing_labels(segmentation, slab):
#     labels = np.unique(segmentation)
#     get_nlabels(slab, labels)
#
#
# def add_slab_label_carefully(slab, numeric_label, string_label):
#     """ Add label to slab if it is not there yet.
#
#     :param numeric_label:
#     :param string_label:
#     :return:
#     """
#     slab_tmp = {string_label: numeric_label}
#     slab_tmp.update(slab)
#     slab = slab_tmp
#     logger.debug('self.slab')
#     logger.debug(str(slab))
#
#
# def add_missing_labels(segmentation, slab):
#     labels = np.unique(segmentation)
#     get_nlabels(slab, labels)
#
#
# class SparseMatrix():
#     def __init__(self, ndarray):
#         self.coordinates = ndarray.nonzero()
#         self.shape = ndarray.shape
#         self.values = ndarray[self.coordinates]
#         self.dtype = ndarray.dtype
#         self.sparse = True
#
#     def todense(self):
#         dense = np.zeros(self.shape, dtype=self.dtype)
#         dense[self.coordinates[:]] = self.values
#         return dense
#
#
# def isSparseMatrix(obj):
#     if obj.__class__.__name__ == 'SparseMatrix':
#         return True
#     else:
#         return False
#
#
# # import sed3
#
# def manualcrop(data):  # pragma: no cover
#
#     try:
#         from pysegbase import seed_editor_qt
#     except:
#         logger.warning("Deprecated of pyseg_base as submodule")
#         import seed_editor_qt
#
#     pyed = seed_editor_qt.QTSeedEditor(data, mode='crop')
#     pyed.exec_()
#     # pyed = sed3.sed3(data)
#     # pyed.show()
#     nzs = pyed.seeds.nonzero()
#     crinfo = [
#         [np.min(nzs[0]), np.max(nzs[0])],
#         [np.min(nzs[1]), np.max(nzs[1])],
#         [np.min(nzs[2]), np.max(nzs[2])],
#     ]
#     data = crop(data, crinfo)
#     return data, crinfo
#
#
# def crop(data, crinfo):
#     """
#     Crop the data.
#
#     crop(data, crinfo)
#
#     :param crinfo: min and max for each axis - [[minX, maxX], [minY, maxY], [minZ, maxZ]]
#
#     """
#     crinfo = fix_crinfo(crinfo)
#     return data[
#            __int_or_none(crinfo[0][0]):__int_or_none(crinfo[0][1]),
#            __int_or_none(crinfo[1][0]):__int_or_none(crinfo[1][1]),
#            __int_or_none(crinfo[2][0]):__int_or_none(crinfo[2][1])
#            ]
#
#
# def __int_or_none(number):
#     if number is not None:
#         number = int(number)
#     return number
#
#
# def combinecrinfo(crinfo1, crinfo2):
#     """
#     Combine two crinfos. First used is crinfo1, second used is crinfo2.
#     """
#     crinfo1 = fix_crinfo(crinfo1)
#     crinfo2 = fix_crinfo(crinfo2)
#
#     crinfo = [
#         [crinfo1[0][0] + crinfo2[0][0], crinfo1[0][0] + crinfo2[0][1]],
#         [crinfo1[1][0] + crinfo2[1][0], crinfo1[1][0] + crinfo2[1][1]],
#         [crinfo1[2][0] + crinfo2[2][0], crinfo1[2][0] + crinfo2[2][1]]
#     ]
#
#     return crinfo
#
#
# def crinfo_from_specific_data(data, margin=0):
#     """
#     Create crinfo of minimum orthogonal nonzero block in input data.
#
#     :param data: input data
#     :param margin: add margin to minimum block
#     :return:
#     """
#     # hledáme automatický ořez, nonzero dá indexy
#     logger.debug('crinfo')
#     logger.debug(str(margin))
#     nzi = np.nonzero(data)
#     logger.debug(str(nzi))
#
#     if np.isscalar(margin):
#         margin = [margin] * 3
#
#     x1 = np.min(nzi[0]) - margin[0]
#     x2 = np.max(nzi[0]) + margin[0] + 1
#     y1 = np.min(nzi[1]) - margin[0]
#     y2 = np.max(nzi[1]) + margin[0] + 1
#     z1 = np.min(nzi[2]) - margin[0]
#     z2 = np.max(nzi[2]) + margin[0] + 1
#
#     # ošetření mezí polí
#     if x1 < 0:
#         x1 = 0
#     if y1 < 0:
#         y1 = 0
#     if z1 < 0:
#         z1 = 0
#
#     if x2 > data.shape[0]:
#         x2 = data.shape[0] - 1
#     if y2 > data.shape[1]:
#         y2 = data.shape[1] - 1
#     if z2 > data.shape[2]:
#         z2 = data.shape[2] - 1
#
#     # ořez
#     crinfo = [[x1, x2], [y1, y2], [z1, z2]]
#     return crinfo
#
#
# def uncrop(data, crinfo, orig_shape, resize=False, outside_mode="constant", cval=0):
#     """
#     Put some boundary to input image.
#
#
#     :param data: input data
#     :param crinfo: array with minimum and maximum index along each axis
#         [[minX, maxX],[minY, maxY],[minZ, maxZ]]. If crinfo is None, the whole input image is placed into [0, 0, 0].
#         If crinfo is just series of three numbers, it is used as an initial point for input image placement.
#     :param orig_shape: shape of uncropped image
#     :param resize: True or False (default). Usefull if the data.shape does not fit to crinfo shape.
#     :param outside_mode: 'constant', 'nearest'
#     :return:
#     """
#
#     if crinfo is None:
#         crinfo = list(zip([0] * data.ndim, orig_shape))
#     elif np.asarray(crinfo).size == data.ndim:
#         crinfo = list(zip(crinfo, np.asarray(crinfo) + data.shape))
#
#     crinfo = fix_crinfo(crinfo)
#     data_out = np.ones(orig_shape, dtype=data.dtype) * cval
#
#     # print 'uncrop ', crinfo
#     # print orig_shape
#     # print data.shape
#     if resize:
#         data = resize_to_shape(data, crinfo[:, 1] - crinfo[:, 0])
#
#     startx = np.round(crinfo[0][0]).astype(int)
#     starty = np.round(crinfo[1][0]).astype(int)
#     startz = np.round(crinfo[2][0]).astype(int)
#
#     data_out[
#     # np.round(crinfo[0][0]).astype(int):np.round(crinfo[0][1]).astype(int)+1,
#     # np.round(crinfo[1][0]).astype(int):np.round(crinfo[1][1]).astype(int)+1,
#     # np.round(crinfo[2][0]).astype(int):np.round(crinfo[2][1]).astype(int)+1
#     startx:startx + data.shape[0],
#     starty:starty + data.shape[1],
#     startz:startz + data.shape[2]
#     ] = data
#
#     if outside_mode == "nearest":
#         # for ax in range(data.ndims):
#         # ax = 0
#
#         # copy border slice to pixels out of boundary - the higher part
#         for ax in range(data.ndim):
#             # the part under the crop
#             start = np.round(crinfo[ax][0]).astype(int)
#             slices = [slice(None), slice(None), slice(None)]
#             slices[ax] = start
#             repeated_slice = np.expand_dims(data_out[slices], ax)
#             append_sz = start
#             if append_sz > 0:
#                 tile0 = np.repeat(repeated_slice, append_sz, axis=ax)
#                 slices = [slice(None), slice(None), slice(None)]
#                 slices[ax] = slice(None, start)
#                 # data_out[start + data.shape[ax] : , :, :] = tile0
#                 data_out[slices] = tile0
#                 # plt.imshow(np.squeeze(repeated_slice))
#                 # plt.show()
#
#             # the part over the crop
#             start = np.round(crinfo[ax][0]).astype(int)
#             slices = [slice(None), slice(None), slice(None)]
#             slices[ax] = start + data.shape[ax] - 1
#             repeated_slice = np.expand_dims(data_out[slices], ax)
#             append_sz = data_out.shape[ax] - (start + data.shape[ax])
#             if append_sz > 0:
#                 tile0 = np.repeat(repeated_slice, append_sz, axis=ax)
#                 slices = [slice(None), slice(None), slice(None)]
#                 slices[ax] = slice(start + data.shape[ax], None)
#                 # data_out[start + data.shape[ax] : , :, :] = tile0
#                 data_out[slices] = tile0
#                 # plt.imshow(np.squeeze(repeated_slice))
#                 # plt.show()
#
#     return data_out
#
#
# def fix_crinfo(crinfo, to='axis'):
#     """
#     Function recognize order of crinfo and convert it to proper format.
#     """
#
#     crinfo = np.asarray(crinfo)
#     if crinfo.shape[0] == 2:
#         crinfo = crinfo.T
#
#     return crinfo
#
#
# def get_one_biggest_object(data):
#     """ Return biggest object """
#     lab, num = scipy.ndimage.label(data)
#     # print ("bum = "+str(num))
#
#     maxlab = max_area_index(lab, num)
#
#     data = (lab == maxlab)
#     return data
#
#
# def max_area_index(labels, num):
#     """
#     Return index of maxmum labeled area
#     """
#     mx = 0
#     mxi = -1
#     for l in range(1, num + 1):
#         mxtmp = np.sum(labels == l)
#         if mxtmp > mx:
#             mx = mxtmp
#             mxi = l
#
#     return mxi
#
#
# def resize_to_shape(data, shape, zoom=None, mode='nearest', order=0):
#     """Resize input data to specific shape.
#
#     :param data: input 3d array-like data
#     :param shape: shape of output data
#     :param zoom: zoom is used for back compatibility
#     :mode: default is 'nearest'
#     """
#     # @TODO remove old code in except part
#
#     if np.array_equal(data.shape, shape):
#         return data
#
#     try:
#         # rint 'pred vyjimkou'
#         # aise Exception ('test without skimage')
#         # rint 'za vyjimkou'
#         import skimage
#         import skimage.transform
#         # Now we need reshape  seeds and segmentation to original size
#
#         segm_orig_scale = skimage.transform.resize(
#             data, shape, order=order,
#             preserve_range=True
#         )
#
#         segmentation = segm_orig_scale
#         logger.debug('resize to orig with skimage')
#     except Exception:
#         logger.warning("Resize by scipy will be removed in the future")
#         import scipy
#         import scipy.ndimage
#         dtype = data.dtype
#         if zoom is None:
#             zoom = np.asarray(data.shape).astype(np.double) / shape
#
#         segm_orig_scale = scipy.ndimage.zoom(
#             data,
#             1.0 / zoom,
#             mode=mode,
#             order=order
#         ).astype(dtype)
#         logger.debug('resize to orig with scipy.ndimage')
#
#         # @TODO odstranit hack pro oříznutí na stejnou velikost
#         # v podstatě je to vyřešeno, ale nechalo by se to dělat elegantněji v zoom
#         # tam je bohužel patrně bug
#         # rint 'd3d ', self.data3d.shape
#         # rint 's orig scale shape ', segm_orig_scale.shape
#         shp = [
#             np.min([segm_orig_scale.shape[0], shape[0]]),
#             np.min([segm_orig_scale.shape[1], shape[1]]),
#             np.min([segm_orig_scale.shape[2], shape[2]]),
#         ]
#         # elf.data3d = self.data3d[0:shp[0], 0:shp[1], 0:shp[2]]
#         # mport ipdb; ipdb.set_trace() # BREAKPOINT
#
#         segmentation = np.zeros(shape, dtype=dtype)
#         segmentation[
#         0:shp[0],
#         0:shp[1],
#         0:shp[2]] = segm_orig_scale[0:shp[0], 0:shp[1], 0:shp[2]]
#
#         del segm_orig_scale
#     return segmentation
#
#
# def resize_to_mm(data3d, voxelsize_mm, new_voxelsize_mm, mode='edge', order=1):
#     """
#     Function can resize data3d or segmentation to specifed voxelsize_mm
#     :new_voxelsize_mm: requested voxelsize. List of 3 numbers, also
#         can be a string 'orig', 'orig*2' and 'orig*4'.
#
#     :voxelsize_mm: size of voxel
#     :mode: default is 'edge'. Modes match the behaviour of numpy.pad
#     """
#
#     if new_voxelsize_mm is 'orig':
#         new_voxelsize_mm = np.array(voxelsize_mm)
#
#     elif new_voxelsize_mm is 'orig*2':
#         new_voxelsize_mm = np.array(voxelsize_mm) * 2
#     elif new_voxelsize_mm is 'orig*4':
#         new_voxelsize_mm = np.array(voxelsize_mm) * 4
#         # vx_size = np.array(metadata['voxelsize_mm']) * 4
#
#     zoom = voxelsize_mm / (1.0 * np.array(new_voxelsize_mm))
#     # data3d_res = scipy.ndimage.zoom(
#     #     data3d,
#     #     zoom,
#     #     mode=mode,
#     #     order=order
#     # ).astype(data3d.dtype)
#
#     # probably better implementation
#     new_shape = data3d.shape * zoom
#     import skimage.transform
#     # Now we need reshape  seeds and segmentation to original size
#
#     data3d_res2 = skimage.transform.resize(
#         data3d, new_shape, order=order,
#         mode=mode,
#         preserve_range=True
#     ).astype(data3d.dtype)
#
#     return data3d_res2
#
#
# def select_objects_by_seeds(binar_data, seeds, ignore_background_seeds=True, background_label=0):
#     """
#     Get N biggest objects from the selection or the object with seed.
#
#     :param binar_data:  binar ndarray
#     :param seeds: ndarray. Objects on non zero positions are returned
#     :return:
#     """
#
#     labeled_data, length = scipy.ndimage.label(binar_data)
#     selected_labels = list(np.unique(labeled_data[seeds > 0]))
#     # selected_labels.pop(0)
#     # pop the background label
#     output = np.zeros_like(binar_data)
#     for label in selected_labels:
#         selection = labeled_data == label
#         # copy from input image to output. If there will be seeds in background, the 0 is copied
#         if ignore_background_seeds and (binar_data[selection][0] == background_label):
#             pass
#         else:
#             # output[selection] = binar_data[selection]
#             output[selection] = 1
#     # import sed3
#     # ed =sed3.sed3(labeled_data, contour=output, seeds=seeds)
#     # ed.show()
#     return output
#
#
# def rotate(data3d, phi_deg, theta_deg=None, phi_axes=(1, 2), theta_axes=(0, 1), order=1, **kwargs):
#     """
#     Rotate 3D data by use angle and its axes or two angles.
#
#     :param data3d: ndimage 3D
#     :param phi_deg: deg
#     :param phi_axes: deg
#     :param theta_deg: deg
#     :param theta_axes: deg
#     :param order: optional, int. Default is 1. The order of the spline interpolation. See scipy for more details.
#     :param kwargs: See scipy.ndimage.interpolation.rotate for more options
#     :return:
#     """
#
#     data3d = scipy.ndimage.interpolation.rotate(data3d, phi_deg, phi_axes, order=order, **kwargs)
#     if theta_deg is not None:
#         data3d = scipy.ndimage.interpolation.rotate(data3d, theta_deg, theta_axes, order=order, **kwargs)
#     return data3d
#     # segmentation = scipy.ndimage.interpolation.rotate(segmentation, angle, axes)
#     # seeds = scipy.ndimage.interpolation.rotate(seeds, angle, axes)
#
#     return data3d
#
#
# def random_rotate_paramteres():
#     """
#     Rotate data3d, segmentation and seeds with random rotation
#     :return:
#     """
#     xi1 = np.random.rand()
#     xi2 = np.random.rand()
#
#     # theta = np.arccos(np.sqrt(1.0-xi1))
#     theta = np.arccos(1.0 - (xi1 * 1))
#     phi = xi2 * 2 * np.pi
#
#     # xs = np.sin(theta) * np.cos(phi)
#     # ys = np.sin(theta) * np.sin(phi)
#     # zs = np.cos(theta)
#
#     phi_deg = np.degrees(phi)
#     theta_deg = np.degrees(theta)
#
#     return phi_deg, theta_deg
#     # TODO independent on voxlelsize (2016-techtest-rotate3d.ipynb)
#
#
# def as_seeds_inds(seeds, datashape):
#     sh1 = datashape
#     sh2 = np.asarray(seeds).shape
#     if np.array_equal(sh1, sh2):
#         seeds_inds = np.nonzero(seeds)
#     else:
#         seeds_inds = seeds
#     return seeds_inds
#
#
# def squeeze_labels(segmentation, try_inplace=True):
#     """
#     Squeeze all labels to int numbers starting from 1
#
#     :param segmentation: labeled image
#     :param try_inplace: try to compute inplace
#     :return:
#     """
#     un = np.unique(segmentation)
#
#     if try_inplace:
#         inplace_possible = True
#         for new_level, level in enumerate(un):
#             # if i == level:
#             #     continue
#             if (new_level > level) and (new_level in un):
#                 # we will rewrite old
#                 inplace_possible = False
#                 break
#     else:
#         inplace_possible = False
#
#     if inplace_possible:
#         output = segmentation
#     else:
#         import copy
#         output = copy.copy(segmentation)
#
#     for new_level, level in enumerate(un):
#         output[segmentation == level] = new_level
#
#     return output
#
#
# def distance_segmentation(seeds, method="edt"):
#     """
#     Separates space based on distance to seeds.
#     :param seeds: ndarray with zeros for background and labeled seeds.
#     :param method: scipy.ndimage.distance_transform function.
#     The `distance_transform_edt` is used if is set to "edt"
#     :return:
#     """
#     if method is "edt":
#         dst_transform = scipy.ndimage.distance_transform_edt
#     else:
#         dst_transform = method
#
#     inds = dst_transform(seeds==0, return_indices=True, return_distances=False)
#
#     lin_inds = []
#     for one_ax in inds:
#         lin_inds.append(one_ax.ravel())
#
#     segm = seeds[lin_inds].reshape(seeds.shape)
#     return segm
#
#
#
#     pass
#

