#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import logging
logger = logging.getLogger(__name__)

import unittest
from io3d import dili


class DictListTestCase(unittest.TestCase):
    def test_ditc_flatten(self):
        data = {
            'a': 1,
            'b': 2,
            'c': {
                'aa': 11,
                'bb': 22,
                'cc': {
                    'aaa': 111
                }
            }
        }
        dct = dili.flatten_dict(data)
        dct = dict(dct)
        self.assertIn("cccaaa", dct.keys())

    def test_ditc_flatten_with_separator(self):
        data = {
            'a': 1,
            'b': 2,
            'c': {
                'aa': 11,
                'bb': 22,
                'cc': {
                    'aaa': 111
                }
            }
        }
        dct = dili.flatten_dict(data, separator=";")
        dct = dict(dct)
        self.assertIn("c;cc;aaa", dct.keys())

    def test_list_filter(self):
        lst = ["aa", "sss", "aaron", "rew"]
        output = dili.list_filter(lst, notstartswith="aa")
        self.assertTrue(["sss", "rew"] == output)

    def test_dict_find_key(self):
        slab={"liver": 1, "porta": 2}
        val = dili.dict_find_key(slab, 2)
        self.assertEqual(val, "porta")

    # def test_dict_find_key_error(self):
    #     slab={"liver": 1, "porta": 2}
    #     val = dili.dict_find_key(slab, 3)
    #     self.assertEqual(val, "porta")
    def sort_list_data(self):
        dct = [
            {"name": "mira", "age": 34, "height": 172.0, "weight": 75},
            {"name": "kamca", "age": 25, "height": 152.0, "weight": 55},
            {"name": "bob", "age": 34, "height": 183.0, "weight": 85},
            {"name": "pavel", "age": 34, "height": 179.0, "weight": 98},
            {"name": "veru", "age": 25, "height": 162.0, "weight": 60},
            {"name": "pepa", "age": 39, "height": 182.0, "weight": 130},
        ]
        return dct

    def test_sort_list_of_dicts(self):
        dct = self.sort_list_data()

        dct = dili.sort_list_of_dicts(dct, keys=["age", "height"])
        self.assertEqual(dct[0]["name"], "kamca")
        self.assertEqual(dct[1]["name"], "veru")
        self.assertEqual(dct[2]["name"], "mira")
        self.assertEqual(dct[-1]["name"], "pepa")

    def test_sort_list_of_dicts_single_key(self):
        dct = self.sort_list_data()
        dct = dili.sort_list_of_dicts(dct, keys="height")
        self.assertEqual(dct[0]["name"], "kamca")
        # self.assertEqual(dct[1]["name"], "veru")
        # self.assertEqual(dct[2]["name"], "mira")
        self.assertEqual(dct[-1]["name"], "bob")
def main():
    unittest.main()
