#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" TODO: Complete documentation
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import sys

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import QColorDialog, QDialogButtonBox
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

__author__ = 'TzuTa Lin <tzu.ta.lin@gmail.com>'
__copyrights__ = 'Copyright 2017 TzuTa Lin'
__license__ = 'MIT'

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
_logger = logging.getLogger(__name__)

BB = QDialogButtonBox


class ColorDialog(QColorDialog):

    def __init__(self, parent=None):
        super(ColorDialog, self).__init__(parent)
        self.setOption(QColorDialog.ShowAlphaChannel)
        # The Mac native dialog does not support our restore button.
        self.setOption(QColorDialog.DontUseNativeDialog)
        # Add a restore defaults button.
        # The default is set at invocation time, so that it
        # works across dialogs for different elements.
        self.default = None
        self.bb = self.layout().itemAt(1).widget()
        self.bb.addButton(BB.RestoreDefaults)
        self.bb.clicked.connect(self.checkRestore)

    def getColor(self, value=None, title=None, default=None):
        self.default = default
        if title:
            self.setWindowTitle(title)
        if value:
            self.setCurrentColor(value)
        return self.currentColor() if self.exec_() else None

    def checkRestore(self, button):
        if self.bb.buttonRole(button) & BB.ResetRole and self.default:
            self.setCurrentColor(self.default)
