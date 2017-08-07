#!/usr/bin/env python
from unittest import TestCase
import time
import sys
import os
__author__ = 'TzuTaLin'

dir_name = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(dir_name, '..', 'libs')
sys.path.insert(0, libs_path)
from settings import Settings

class TestSettings(TestCase):

    def test_basic(self):
        wSetting = Settings()
        wSetting['test0'] = 'hello'
        wSetting['test1'] = 10
        wSetting['test2'] = [0, 2, 3]
        self.assertEqual(wSetting.get('test3', 3), 3)
        self.assertEqual(wSetting.save(), True)


if __name__ == '__main__':
    unittest.main()
