import os
import sys
import unittest
import resources
from stringBundle import StringBundle

class TestStringBundle(unittest.TestCase):

    def test_loadDefaultBundle_withoutError(self):
        str_bundle = StringBundle.get_bundle('en')
        self.assertEqual(str_bundle.get_string("openDir"), 'Open Dir', 'Fail to load the default bundle')

    def test_fallback_withoutError(self):
        str_bundle = StringBundle.get_bundle('zh-TW')
        self.assertEqual(str_bundle.get_string("openDir"), u'\u958B\u555F\u76EE\u9304', 'Fail to load the zh-TW bundle')

    def test_setInvaleLocaleToEnv_printErrorMsg(self):
        prev_lc = os.environ['LC_ALL']
        prev_lang = os.environ['LANG']
        os.environ['LC_ALL'] = 'UTF-8'
        os.environ['LANG'] = 'UTF-8'
        str_bundle = StringBundle.get_bundle()
        self.assertEqual(str_bundle.get_string("openDir"), 'Open Dir', 'Fail to load the default bundle')
        os.environ['LC_ALL'] = prev_lc
        os.environ['LANG'] = prev_lang


if __name__ == '__main__':
    unittest.main()
