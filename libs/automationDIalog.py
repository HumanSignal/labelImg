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
        self.parent = parent
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
        num_classes = 0
        # 获取类别数目 以及类别列表
        origin_mapping = {}
        with open(names_list_path, 'r') as f_name:
            for line in f_name.readlines():
                if line != '\n':
                    new_label = line.replace('\n', '')
                    # 模型中的同名label在原用户标注中的位置 同名则融合进去 否则添加
                    if self.parent.labelHist.count(new_label) > 0:
                        origin_position = self.parent.labelHist.index(new_label)
                        origin_mapping[num_classes] = origin_position
                    else:
                        origin_mapping[num_classes] = len(self.parent.labelHist)
                        # 将模型中的新label添加到原本的label中去
                        self.parent.labelHist.append(new_label)
                        self.parent.labelColor[new_label] = (generateColorByText(new_label),
                                                             generateColorByText(new_label, 100))
                    num_classes += 1

            self.parent.persistLabelList()

        # 写入data配置文件 用于模型读取类别数 以及标签位置
        with open(meta_path, 'w') as f_data:
            f_data.writelines([
                "classes = %s\n" % num_classes,
                "labels = %s\n" % labels_list_path,
                "names = %s\n" % names_list_path,
            ])
        # 初始化模型并检测 这里offset是原有的用户添加的类别数目
        detect_generate(
            img_abspath_list=self.img_list,
            configPath=cfg_path,
            weightPath=weight_path,
            metaPath=meta_path,
            origin_mapping=origin_mapping
        )
        self.parent.labeledImgList += self.img_list
        self.parent.persistLabeledImgList(self.parent.labeledImgList, 0)
        print('Done.')
        QMessageBox.information(self, 'Ok', self.tr('Generate annotation done.'),
                                QMessageBox.Ok)
        self.close()
        self.parent.openNextImg()
        self.parent.openPrevImg()
