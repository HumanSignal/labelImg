import os

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import newIcon, labelValidator, generateColorByText
from libs.darknet import detect_generate

BB = QDialogButtonBox


class AutomationDialog(QDialog):

    def __init__(self, text='Automation', modelRoot=None, imgList=None, parent=None):
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
                if os.path.isdir(os.path.join(modelRoot, model_path)):
                    self.model_list.addItem(QListWidgetItem(model_path))
        self.mode_root = modelRoot
        self.model_list.setCurrentRow(0)
        self.model_list.itemSelectionChanged.connect(self.updateStatus)
        left_side.addWidget(self.model_list)
        self.txt_total_classes = QLineEdit()
        self.txt_total_classes.setValidator(QIntValidator())
        self.txt_total_classes.setText('1')
        left_side.addWidget(QLabel('Total Label Num'))
        left_side.addWidget(self.txt_total_classes)
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
        # 判断输入合法性
        if not self.img_list:
            QMessageBox.warning(self, 'Warning', self.tr('No files chosen!!'), QMessageBox.Ok)
            return
        if not self.model:
            QMessageBox.warning(self, 'Warning', self.tr('No detector model chosen!!'), QMessageBox.Ok)
            return
        if self.txt_total_classes.text() == '' or int(self.txt_total_classes.text()) < 1:
            QMessageBox.warning(self, 'Warning', self.tr('Please input correct label num(total label num >=1)!!'),
                                QMessageBox.Ok)
            return
        labels_list_path = os.path.join(self.mode_root, self.model, 'labels.list')
        names_list_path = os.path.join(self.mode_root, self.model, 'names.list')
        cfg_path = os.path.join(self.mode_root, self.model, 'model.cfg')
        weight_path = os.path.join(self.mode_root, self.model, 'model.weights')
        meta_path = os.path.join(self.mode_root, self.model, 'model.data')
        # 检查是否有对应的配置文件
        for path in [labels_list_path, names_list_path, cfg_path, weight_path]:
            if not os.path.exists(path):
                QMessageBox.warning(self, 'Warning', self.tr('Can\'t find "%s"' % path),
                                    QMessageBox.Ok)
                return
        # 写入data配置文件 用于模型读取类别数 以及标签位置
        with open(meta_path, 'w') as f_data:
            f_data.writelines([
                "classes = %s\n" % int(self.txt_total_classes.text()),
                "labels = %s\n" % labels_list_path,
                "names = %s\n" % names_list_path,
            ])
        # 初始化模型并检测
        detect_generate(
            img_abspath_list=self.img_list,
            configPath=cfg_path,
            weightPath=weight_path,
            metaPath=meta_path,
        )
        QMessageBox.information(self, 'Ok', self.tr('Generate annotation done.'),
                                QMessageBox.Ok)
        self.close()
