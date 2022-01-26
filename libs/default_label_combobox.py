import sys
try:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import QWidget, QHBoxLayout, QComboBox


class DefaultLabelComboBox(QWidget):
    def __init__(self, parent=None, items=[]):
        super(DefaultLabelComboBox, self).__init__(parent)

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.items = items
        self.cb.addItems(self.items)

        self.cb.currentIndexChanged.connect(parent.default_label_combo_selection_changed)

        layout.addWidget(self.cb)
        self.setLayout(layout)
