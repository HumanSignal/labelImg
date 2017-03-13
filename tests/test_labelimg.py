#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_labelimg
----------------------------------

Tests for `labelimg` module.
"""

from labelimg.__main__ import get_main_app


def test_launch_window():
    app, win = get_main_app()
    win.close()
    app.quit()
