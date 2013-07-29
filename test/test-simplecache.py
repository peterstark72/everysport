#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport.simplecache as simplecache

class TestSimpleCache(unittest.TestCase):

    def test_add(self):
        simplecache.add("foo", "bar")
        d = simplecache.get("foo")
        self.assertEqual(d, "bar")


    def test_add2(self):
        self.assertTrue(not simplecache.get("test"))        


    def test_addurl(self):
        url = "http://example.com?key=y3gy3&shsh=shsh#shs"
        simplecache.add(url, "bar")
        response = simplecache.get(url)
        self.assertEqual(response, "bar")

        


if __name__ == '__main__': 
    unittest.main()