LabelImg
========

.. image:: https://img.shields.io/pypi/v/labelimg.svg
        :target: https://pypi.python.org/pypi/labelimg

.. image:: https://img.shields.io/travis/tzutalin/labelImg.svg
        :target: https://travis-ci.org/tzutalin/labelImg

.. image:: https://img.shields.io/badge/lang-en-blue.svg
        :target: https://github.com/tzutalin/labelImg/blob/master/README.zh.rst

.. image:: https://img.shields.io/badge/lang-zh-green.svg
        :target: https://github.com/tzutalin/labelImg/blob/master/readme/README.zh.rst

.. image:: https://img.shields.io/badge/lang-zh--TW-green.svg
    :target: (https://github.com/jonatasemidio/multilanguage-readme-pattern/blob/master/README.pt-br.md

.. image:: /resources/icons/app.png
    :width: 200px
    :align: center

LabelImg 是影像標註工具，它是用python 和 QT 寫成的.

支持的儲存格式包括PASCAL VOC format, YOLO, createML.

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo3.jpg
     :alt: Demo Image

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo.jpg
     :alt: Demo Image

`展示影片 <https://youtu.be/p0nR2YsCY_U>`__

安裝
------------------


透過編譯原始碼
~~~~~~~~~~~~~~~~~

Linux/Ubuntu/Mac 需要 Python 和 `PyQt <https://pypi.org/project/PyQt5/>`__

Ubuntu Linux
^^^^^^^^^^^^

Python 3 + Qt5

.. code:: shell

    sudo pip3 install -r requirements/requirements-linux-python3.txt
    make pyside6
    python3 labelImg.py
    python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

macOS
^^^^^

Python 3 + PySide6

.. code:: shell

    pip3 install pyside6 lxml
    make pyside6
    python3 labelImg.py
    python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]


Python 3 Virtualenv (推薦方法)

Virtualenv 可以避免版本和相依性問題

.. code:: shell

    brew install python3
    pip3 install pipenv
    pipenv run pip install pyside6 lxml
    pipenv run make pyside6
    pipenv run python3 labelImg.py


Windows
^^^^^^^

Open cmd and go to the `labelImg <#labelimg>`__ directory

.. code:: shell

    pip install pyside6 lxml
    pyside6-rcc -o libs/resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Windows + Anaconda
^^^^^^^^^^^^^^^^^^

下載並安裝 `Anaconda <https://www.anaconda.com/download/#download>`__ (Python 3+)

打開 Anaconda Prompt 然後到 `labelImg <#labelimg>`__ 目錄

.. code:: shell

    conda install pyside6
    conda install -c anaconda lxml
    pyside6-rcc -o libs/resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]


使用方法
-----

`你可以參考影片  <https://youtu.be/nw1GexJzbCI>`__

你可以先產生標籤
~~~~~~~~~~~~~~~~~~~~~~~~~~

修改這個檔案
`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__

快捷鍵
~~~~~~~

+--------------------+--------------------------------------------+
| Ctrl + u           | 讀取所有影像從每個目錄                     |
+--------------------+--------------------------------------------+
| Ctrl + r           | 改變標示結果的存檔目錄                     |
+--------------------+--------------------------------------------+
| Ctrl + s           | 存檔                                       |
+--------------------+--------------------------------------------+
| Ctrl + d           | 複製目前的標籤和物件的區塊                 |
+--------------------+--------------------------------------------+
| Ctrl + Shift + d   | 刪除目前影像                               |
+--------------------+--------------------------------------------+
| Space              | 標示目前照片已經處理過                     |
+--------------------+--------------------------------------------+
| w                  | 產生新的物件區塊                           |
+--------------------+--------------------------------------------+
| d                  | 下張影像                                   |
+--------------------+--------------------------------------------+
| a                  | 上張影像                                   |
+--------------------+--------------------------------------------+
| del                | 刪除所選的物件區塊                         |
+--------------------+--------------------------------------------+
| Ctrl++             | 放大影像                                   |
+--------------------+--------------------------------------------+
| Ctrl--             | 縮小影像                                   |
+--------------------+--------------------------------------------+
| ↑→↓←               | 移動所選的物件區塊                         |
+--------------------+--------------------------------------------+

如何貢獻
~~~~~~~~~~~~~~~~~

歡迎上傳程式碼直接貢獻
