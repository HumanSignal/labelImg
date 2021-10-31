
from PySide6.QtCore import QSize,Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QSpinBox, QAbstractSpinBox


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
        #width = fm.width(str(self.maximum()))
        width = fm.maxWidth()
        return QSize(width, height)