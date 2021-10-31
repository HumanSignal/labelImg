#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox



class ComboBox(QWidget):
    def __init__(self, parent=None, items=[]):
        super(ComboBox, self).__init__(parent)

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.items = items
        self.cb.addItems(self.items)

        self.cb.currentIndexChanged.connect(parent.combo_selection_changed)

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def update_items(self, items):
        self.items = items

        self.cb.clear()
        self.cb.addItems(self.items)