from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import newIcon, labelValidator

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, predefined_classes=[]):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)

        # Martin Kersner, 2015/10/13
        if predefined_classes:
            self.edit.setDisabled(True)
            widget = QWidget(self)
            letter_group = QButtonGroup(widget)
            radio_button = []
            for label, label_idx in zip(predefined_classes, range(len(predefined_classes))):
                radio_button.append(QRadioButton(label))
                radio_button[label_idx].clicked.connect(self.changeClass)
                layout.addWidget(radio_button[label_idx])

        layout.addWidget(bb)
        self.setLayout(layout)

    # Martin Kersner, 2015/10/13
    def changeClass(self):
        sender = self.sender()
        self.edit.setText(sender.text())

    def validate(self):
        if self.edit.text().trimmed():
            self.accept()

    def postProcess(self):
        self.edit.setText(self.edit.text().trimmed())

    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None
