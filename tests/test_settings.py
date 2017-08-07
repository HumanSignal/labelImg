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

    def test_write(self):
        wSetting = Settings()
        wSetting['test0'] = 'hello'
        wSetting['test1'] = 10
        wSetting['test2'] = [0, 2, 3]
        # asyc call ?
        wSetting.save()
        time.sleep(1)
        self.assertEqual(os.path.exists('.settings.pkl'), True)

    def test_read(self):
        rSetting = Settings()
        rSetting.load()

        self.assertEqual(rSetting.get('test0'), 'hello')
        self.assertEqual(rSetting.get('test1'), 10)
        self.assertEqual(rSetting.get('test2'), [0, 2, 3])
        self.assertEqual(rSetting.get('test3', 3), 3)


if __name__ == '__main__':
    unittest.main()
