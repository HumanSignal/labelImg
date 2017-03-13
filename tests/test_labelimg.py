#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_labelimg
----------------------------------

Tests for `labelimg` module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from labelimg.__main__ import get_main_app


def test_launch_window():
    app, win = get_main_app()
    win.close()
    app.quit()
