#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
if items were added in files in the resources/strings folder,
then execute "pyrcc5 resources.qrc -o resources.py" in the root directory
and execute "pyrcc5 ../resources.qrc -o resources.py" in the libs directory
"""
import re
import os
import sys
import locale
from libs.ustr import ustr

try:
    from PyQt5.QtCore import *
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import *


class StringBundle:

    __create_key = object()

    def __init__(self, create_key, locale_str):
        assert(create_key == StringBundle.__create_key), "StringBundle must be created using StringBundle.getBundle"
        self.id_to_message = {}
        paths = self.__create_lookup_fallback_list(locale_str)
        for path in paths:
            self.__load_bundle(path)

    @classmethod
    def get_bundle(cls, locale_str=None):
        if locale_str is None:
            try:
                locale_str = locale.getlocale()[0] if locale.getlocale() and len(
                    locale.getlocale()) > 0 else os.getenv('LANG')
            except:
                print('Invalid locale')
                locale_str = 'en'

        return StringBundle(cls.__create_key, locale_str)

    def get_string(self, string_id):
        assert(string_id in self.id_to_message), "Missing string id : " + string_id
        return self.id_to_message[string_id]

    def __create_lookup_fallback_list(self, locale_str):
        result_paths = []
        base_path = ":/strings"
        result_paths.append(base_path)
        if locale_str is not None:
            # Don't follow standard BCP47. Simple fallback
            tags = re.split('[^a-zA-Z]', locale_str)
            for tag in tags:
                last_path = result_paths[-1]
                result_paths.append(last_path + '-' + tag)

        return result_paths

    def __load_bundle(self, path):
        PROP_SEPERATOR = '='
        f = QFile(path)
        if f.exists():
            if f.open(QIODevice.ReadOnly | QFile.Text):
                text = QTextStream(f)
                text.setCodec("UTF-8")

            while not text.atEnd():
                line = ustr(text.readLine())
                key_value = line.split(PROP_SEPERATOR)
                key = key_value[0].strip()
                value = PROP_SEPERATOR.join(key_value[1:]).strip().strip('"')
                self.id_to_message[key] = value

            f.close()
