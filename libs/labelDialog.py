from libs.colorDialog import ColorDialog

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import newIcon, labelValidator, generateColorByText

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item_label in listItem:
                item = QListWidgetItem(self.listWidget)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                color = parent.labelColor[item_label][0]
                item.setBackground(color)
                # Set default label list height
                item.setSizeHint(QSize(item.sizeHint().width(), 35))
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, CustomQWidget(item_label, color, item, parent))
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        # Get the label from the label of item widget
        origin_text = self.listWidget.itemWidget(tQListWidgetItem).label.text()
        try:
            text = origin_text.trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = origin_text.strip()
        self.edit.setText(text)
        
    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()


class CustomQWidget(QWidget):
    def __init__(self, label, color, parent_item, parent=None):
        super(CustomQWidget, self).__init__(parent)
        self.colorDialog = ColorDialog(parent=self)
        self.color = color
        self.label = QLabel(label)
        self.parent_item = parent_item
        # as the parent of labelImg, sharing data
        self.parent = parent
        button = QPushButton()
        button.setIcon(newIcon('color'))
        button.setFixedWidth(35)
        button.clicked.connect(self.get_color)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setLayout(layout)

    def get_color(self):
        color = self.colorDialog.getColor(None, u'Choose line color', default=QColor(0, 255, 0, 128))
        if color:
            self.parent_item.setBackground(color)
            print(self.parent.canvas.shapes)
            # update color of this label category
            line_color = color
            fill_color = QColor(color)
            fill_color.setAlpha(100)
            self.parent.labelColor[self.label.text()] = (line_color, fill_color)
            for shape in self.parent.canvas.shapes:
                if shape.label == self.label.text():
                    shape.line_color = line_color
                    shape.fill_color = fill_color
