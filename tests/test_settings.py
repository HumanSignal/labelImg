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
        settings = Settings()
        settings['test0'] = 'hello'
        settings['test1'] = 10
        settings['test2'] = [0, 2, 3]
        self.assertEqual(settings.get('test3', 3), 3)
        self.assertEqual(settings.save(), True)

        settings.load()
        self.assertEqual(settings.get('test0'), 'hello')
        self.assertEqual(settings.get('test1'), 10)

        settings.reset()
        


if __name__ == '__main__':
    unittest.main()
