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

LabelImgは、PythonとQtを使うアノテーション補助ツールです。

このツールはPascalVOCフォーマットとYOLOとCreateMLをサポートしています。

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo3.jpg
     :alt: Demo Image

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo.jpg
     :alt: Demo Image

`サンプル動画は <https://youtu.be/p0nR2YsCY_U>にあります。`__

インストール方法
-------------------


ソースからビルドする
~~~~~~~~~~~~~~~~~~~~

Linuxまたは、Ubuntuまたは、macOSの場合は

Ubuntuの場合
^^^^^^^^^^^^

Python 3とQt5を使う場合

.. code:: shell

    pip install -r requirements/requirements-linux-python3.txt
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


Python 3 Virtualenv (推奨)

VirtualenvはQtとPythonのバージョン衝突問題を解消できます。

.. code:: shell

    brew install python3
    pip3 install pipenv
    pipenv run pip install pyside6 lxml
    pipenv run make pyside6
    pipenv run python3 labelImg.py
    [Optional] rm -rf build dist; python setup.py py2app -A;mv "dist/labelImg.app" /Applications


Windowsの場合
^^^^^^^^^^^^^


Open cmd and go to the `labelImg <#labelimg>`__ directory

.. code:: shell

    pip install pyside6 lxml
    pyside6-rcc -o libs/resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Windows + Anaconda
^^^^^^^^^^^^^^^^^^

`Anaconda <https://www.anaconda.com/download/#download>`__ をダウンロードしてからインストールしてください。

Anaconda Promptを起動し `labelImg <#labelimg>`__ インストールされているフォルダに移動してから以下のコマンドを実行します。

.. code:: shell

    conda install pyside6
    conda install -c anaconda lxml
    pyside6-rcc -o libs/resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

PyPIから入手する（Python 3以降のみ）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
現代的なLinuxディストリビューションの場合は以下のコマンドを入力するだけでインストールできます。

.. code:: shell

    pip3 install labelImg
    labelImg
    labelImg [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Dockerの場合
~~~~~~~~~~~~~~~~~


定義済みクラスを作成するには？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__
を編集してください。

ショートカット一覧
~~~~~~~~~~~~~~~~~~

+--------------------+--------------------------------------------+
| Ctrl + u           | そのディレクトリの画像を読み込む              |
+--------------------+--------------------------------------------+
| Ctrl + r           | アノテーションの生成ディレクトリを変更         |
+--------------------+--------------------------------------------+
| Ctrl + s           | 保存する                                    |
+--------------------+--------------------------------------------+
| Ctrl + d           | 現在選択している矩形トラベルをコピー          |
+--------------------+--------------------------------------------+
| Ctrl + Shift + d   | 現在表示している画像を削除                   |
+--------------------+--------------------------------------------+
| Space              | 現在の画像に検証済みフラグを立てる            |
+--------------------+--------------------------------------------+
| w                  | 矩形を生成する                              |
+--------------------+--------------------------------------------+
| d                  | 次の画像へ移動する                           |
+--------------------+--------------------------------------------+
| a                  | 前の画像へ移動する                           |
+--------------------+--------------------------------------------+
| del                | 選択した矩形を削除                           |
+--------------------+--------------------------------------------+
| Ctrl++             | 画像を拡大                                  |
+--------------------+--------------------------------------------+
| Ctrl--             | 画像を縮小                                  |
+--------------------+--------------------------------------------+
| ↑→↓←               | 十字キーで矩形を移動する                     |
+--------------------+--------------------------------------------+

開発に参加するには？
~~~~~~~~~~~~~~~~~~~~~

このリポジトリにPull Request を送ってください。
