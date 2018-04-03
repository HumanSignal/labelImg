#!/usr/bin/env python
import os
import sys
import time
import unittest

__author__ = 'TzuTaLin'

dir_name = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(dir_name, '..', 'libs')
sys.path.insert(0, libs_path)
from settings import Settings

class TestSettings(unittest.TestCase):

    def test_basic(self):
        wSetting = Settings()
        wSetting['test0'] = 'hello'
        wSetting['test1'] = 10
        wSetting['test2'] = [0, 2, 3]
        self.assertEqual(wSetting.get('test3', 3), 3)
        self.assertEqual(wSetting.save(), True)


if __name__ == '__main__':
    unittest.main()
