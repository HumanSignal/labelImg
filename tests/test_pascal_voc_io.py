# -*- coding: utf8 -*-

from unittest import TestCase

from xml.etree.ElementTree import Element

from pascal_voc_io import PascalVocWriter


class TestPascalVocWriter(TestCase):
    def test_prettify_utf8_chinese(self):
        w = PascalVocWriter(None, None, None)
        s = u'中华人民共和国'
        x = w.prettify(Element(s))
        expected = '<{}/>\n'.format(s.encode('utf8'))
        self.assertEqual(expected, x)
