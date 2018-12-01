import os
import sys
import unittest
from libs.lib import struct, newAction, newIcon, addActions, fmtShortcut, generateColorByText

class TestLib(unittest.TestCase):

    def test_generateColorByGivingUniceText_noError(self):
        res = generateColorByText(u'\u958B\u555F\u76EE\u9304')
        self.assertTrue(res.green() >= 0)
        self.assertTrue(res.red() >= 0)
        self.assertTrue(res.blue() >= 0)

if __name__ == '__main__':
    unittest.main()
