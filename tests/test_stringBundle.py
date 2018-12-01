import os
import sys
import unittest
from stringBundle import StringBundle

class TestStringBundle(unittest.TestCase):

    def test_loadDefaultBundle_withoutError(self):
        strBundle = StringBundle.getBundle('en')
        self.assertEqual(strBundle.getString("openDir"), 'Open Dir', 'Fail to load the default bundle')

    def test_fallback_withoutError(self):
        strBundle = StringBundle.getBundle('zh-TW')
        self.assertEqual(strBundle.getString("openDir"), u'\u958B\u555F\u76EE\u9304', 'Fail to load the zh-TW bundle')

if __name__ == '__main__':
    unittest.main()
