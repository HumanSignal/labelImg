import os
import sys
import unittest
from libs.utils import Struct, new_action, new_icon, add_actions, format_shortcut, generate_color_by_text, natural_sort

class TestUtils(unittest.TestCase):

    def test_generateColorByGivingUniceText_noError(self):
        res = generate_color_by_text(u'\u958B\u555F\u76EE\u9304')
        self.assertTrue(res.green() >= 0)
        self.assertTrue(res.red() >= 0)
        self.assertTrue(res.blue() >= 0)

    def test_nautalSort_noError(self):
        l1 = ['f1', 'f11', 'f3']
        expected_l1 = ['f1', 'f3', 'f11']
        natural_sort(l1)
        for idx, val in enumerate(l1):
            self.assertTrue(val == expected_l1[idx])

if __name__ == '__main__':
    unittest.main()
