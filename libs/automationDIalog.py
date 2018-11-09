import os

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


class AutomationDialog(QDialog):

    def __init__(self, text="Automation", modelRoot=None, imgList=None, parent=None):
        super(AutomationDialog, self).__init__(parent)
        # 布局
        container = QVBoxLayout()
        list_container = QHBoxLayout()
        # 左侧检测模型列表
        left_side = QVBoxLayout()
        left_side.addWidget(QLabel('Choose Detector Model'))
        self.model_list = QListWidget()
        # 添加项目
        if modelRoot:
            for model_path in os.listdir(modelRoot):
                self.model_list.addItem(QListWidgetItem(model_path))
        self.model_list.setCurrentRow(0)
        self.model_list.itemSelectionChanged.connect(self.updateStatus)
        left_side.addWidget(self.model_list)
        self.lbl_status = QTextBrowser()
        left_side.addWidget(self.lbl_status)
        # 右侧文件列表
        right_side = QVBoxLayout()
        right_side.addWidget(QLabel('Choose Detecting Files'))
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_list.itemSelectionChanged.connect(self.updateStatus)
        if imgList:
            for img_path in imgList:
                self.file_list.addItem(QListWidgetItem(img_path))
        right_side.addWidget(self.file_list)
        # 整体布局
        list_container.addLayout(left_side)
        list_container.addLayout(right_side)
        container.addLayout(list_container)
        self.btn_start = QPushButton('Start')
        self.btn_start.clicked.connect(self.start_detector)
        container.addWidget(self.btn_start)
        self.setLayout(container)
        # 设置默认status显示
        self.updateStatus()
        self.resize(640, 480)

    def updateStatus(self):
        if not self.model_list.selectedItems():
            self.model = None
        else:
            self.model = self.model_list.selectedItems()[0].text()
        self.img_list = [item.text() for item in self.file_list.selectedItems()]
        self.lbl_status.setText(
            'Using {} model.\n{} imgs chosen.'.format(self.model, len(self.img_list))
        )

    def start_detector(self):
        if not self.img_list:
            QMessageBox.warning(self, "Warning", self.tr("No files chosen!!"), QMessageBox.Ok)
            return
        if not self.model:
            QMessageBox.warning(self, "Warning", self.tr("No detector model chosen!!"), QMessageBox.Ok)
            return

        print(
            self.model,
            self.img_list
        )
