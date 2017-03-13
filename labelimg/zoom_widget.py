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
    from PyQt5.QtWidgets import *
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


class ZoomWidget(QSpinBox):

    def __init__(self, value=100):
        super(ZoomWidget, self).__init__()
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setRange(1, 500)
        self.setSuffix(' %')
        self.setValue(value)
        self.setToolTip(u'Zoom Level')
        self.setStatusTip(self.toolTip())
        self.setAlignment(Qt.AlignCenter)

    def minimumSizeHint(self):
        height = super(ZoomWidget, self).minimumSizeHint().height()
        fm = QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QSize(width, height)
