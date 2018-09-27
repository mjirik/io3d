#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module is provides funcions for dict lists and functions processing
"""
import logging
logger = logging.getLogger(__name__)
import collections
import inspect
import copy
import numpy as np


def get_default_args(obj):
    if ("__init__" in dir(obj)):
        if inspect.isfunction(obj.__init__) or inspect.ismethod(obj.__init__):
            argspec = inspect.getargspec(obj.__init__)
        else:
            argspec = inspect.getargspec(obj)
    else:
        argspec = inspect.getargspec(obj)

    args = argspec.args[1:]
    defaults = argspec.defaults
    dc = collections.OrderedDict(zip(args, defaults))
    return dc

def subdict(dct, keys):
    if type(dct) == collections.OrderedDict:
        p = collections.OrderedDict()
    else:
        p = {}
    for key, value in dct.items():
        if key in keys:
            p[key] = value
    # p = {key: value for key, value in dct.items() if key in keys}
    return p


def list_filter(lst, startswith=None, notstartswith=None,
                contain=None, notcontain=None):
    """ Keep in list items according to filter parameters.

    :param lst: item list
    :param startswith: keep items starting with
    :param notstartswith: remove items starting with
    :return:
    """
    keeped = []
    for item in lst:
        keep = False
        if startswith is not None:
            if item.startswith(startswith):
                keep = True
        if notstartswith is not None:
            if not item.startswith(notstartswith):
                keep = True
        if contain is not None:
            if contain in item:
                keep = True
        if notcontain is not None:
            if not notcontain in item:
                keep = True

        if keep:
            keeped.append(item)
    return keeped

def kick_from_dict(dct, keys):
    if type(dct) == collections.OrderedDict:
        p = collections.OrderedDict()
    else:
        p = {}
    for key, value in dct.items():
        if key not in keys:
            p[key] = value

    # p = {key: value for key, value in dct.items() if key not in keys}
    return p

def split_dict(dct, keys):
    """
    Split dict into two subdicts based on keys.

    :param dct:
    :param keys:
    :return: dict_in, dict_out
    """
    if type(dct) == collections.OrderedDict:
        dict_in = collections.OrderedDict()
        dict_out = collections.OrderedDict()
    else:
        dict_in = {}
        dict_out = {}

    for key, value in dct.items:
        if key in keys:
            dict_in[key] = value
        else:
            dict_out[key] = value
    return dict_in, dict_out

def recursive_update(d, u):
    """
    Dict recursive update.

    Based on Alex Martelli code on stackoverflow
    http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth?answertab=votes#tab-top

    :param d: dict to update
    :param u: dict with new data
    :return:
    """
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

from collections import Mapping
from operator import add

_FLAG_FIRST = object()

def flatten_dict_join_keys(dct, join_symbol=" "):
    """ Flatten dict with defined key join symbol.

    :param dct: dict to flatten
    :param join_symbol: default value is " "
    :return:
    """
    return dict( flatten_dict(dct, join=lambda a,b:a+join_symbol+b) )


def flatten_dict(dct, separator=None, join=add, lift=lambda x:x):
    """

    Based on ninjagecko code on stackoveflow
    http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys

    :param dct: dict to flatten
    :param separator: use preset values for join and lift.
    Use empty list or tuple [], () for key hierarchy stored in list.
    If simple_mode is string it is used as a separator.
    :param join: join operation. To join keys with '_' use join=lambda a,b:a+'_'+b
    :param lift:  to have all hierarchy keys in lise use lift=lambda x:(x,))
    :return:

    For all keys from above hierarchy in list use:
    dict( flattenDict(testData, lift=lambda x:(x,)) )

    For all keys from abve hierarchy separated by '_' use:
    dict( flattenDict(testData, join=lambda a,b:a+'_'+b) )
    """

    if type(separator) is str:
        join = lambda a, b: a + separator + b
    elif type(separator) in (list, tuple):
        lift = lambda x:(x,)

    results = []
    def visit(subdict, results, partialKey):
        for k,v in subdict.items():
            newKey = lift(k) if partialKey==_FLAG_FIRST else join(partialKey,lift(k))
            if isinstance(v,Mapping):
                visit(v, results, newKey)
            else:
                results.append((newKey,v))
    visit(dct, results, _FLAG_FIRST)
    return results


def list_contains(list_of_strings, substring, return_true_false_array=False):
    """ Get strings in list which contains substring.

    """
    key_tf = [keyi.find(substring) != -1 for keyi in list_of_strings]
    if return_true_false_array:
        return key_tf
    keys_to_remove = list_of_strings[key_tf]
    return keys_to_remove


def df_drop_duplicates(df, ignore_key_pattern="time"):
    """
    Drop duplicates from dataframe ignore columns with keys containing defined pattern.

    :param df:
    :param noinfo_key_pattern:
    :return:
    """

    keys_to_remove = list_contains(df.keys(), ignore_key_pattern)
    #key_tf = [key.find(noinfo_key_pattern) != -1 for key in df.keys()]
    # keys_to_remove
    # remove duplicates
    ks = copy.copy(list(df.keys()))
    for key in keys_to_remove:
        ks.remove(key)

    df = df.drop_duplicates(ks)
    return df


def ndarray_to_list_in_structure(item, squeeze=True):
    """ Change ndarray in structure of lists and dicts into lists.
    """
    tp = type(item)

    if tp == np.ndarray:
        if squeeze:
            item = item.squeeze()
        item = item.tolist()
    elif tp == list:
        for i in range(len(item)):
            item[i] = ndarray_to_list_in_structure(item[i])
    elif tp == dict:
        for lab in item:
            item[lab] = ndarray_to_list_in_structure(item[lab])

    return item


def dict_find_key(dd, value):
    """ Find first suitable key in dict.

    :param dd:
    :param value:
    :return:
    """
    key = next(key for key, val in dd.items() if val == value)
    return key


def sort_list_of_dicts(lst_of_dct, keys, reverse=False, **sort_args):
    """
    Sort list of dicts by one or multiple keys.

    If the key is not available, sort these to the end.

    :param lst_of_dct: input structure. List of dicts.
    :param keys: one or more keys in list
    :param reverse:
    :param sort_args:
    :return:
    """

    if type(keys) != list:
        keys = [keys]
    # dcmdir = lst_of_dct[:]
    # lst_of_dct.sort(key=lambda x: [x[key] for key in keys], reverse=reverse, **sort_args)
    lst_of_dct.sort(key=lambda x: [((False, x[key]) if key in x else (True, 0)) for key in keys], reverse=reverse, **sort_args)
    return lst_of_dct

def ordered_dict_to_dict(config):
    """
    Use dict instead of ordered dict in structure.
    """

    if type(config) == collections.OrderedDict:
        config = dict(config)
    if type(config) == list:
        for i in range(0, len(config)):
            config[i] = ordered_dict_to_dict(config[i])
    elif type(config) == dict:
        for key in config:
            config[key] = ordered_dict_to_dict(config[key])

    return config


# def struct_to_yaml(cfg):
#     """
#     write complex struct with dicts and lists into yaml
#     :param cfg:
#     :return:
#     """
#     import yaml
#     # convert values to json
#     isconverted = {}
#     for key, value in cfg.iteritems():
#         if type(value) in (str, int, float, bool):
#
#             isconverted[key] = False
#             if type(value) is str:
#                 pass
#
#         else:
#             isconverted[key] = True
#             cfg[key] = yaml.dump(value, default_flow_style=True)
#     return cfg

