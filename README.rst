LabelImg
========

.. image:: https://img.shields.io/pypi/v/labelimg.svg
        :target: https://pypi.python.org/pypi/labelimg

.. image:: https://img.shields.io/travis/tzutalin/labelImg.svg
        :target: https://travis-ci.org/tzutalin/labelImg

LabelImg is a graphical image annotation tool.

It is written in Python and uses Qt for its graphical interface.

Annotations are saved as XML files in PASCAL VOC format, the format used
by `ImageNet <http://www.image-net.org/>`__.

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo3.jpg
     :alt: Demo Image

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo.jpg
     :alt: Demo Image

`Watch a demo video <https://youtu.be/p0nR2YsCY_U>`__

Installation
------------------

Download prebuilt binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Windows & Linux <https://tzutalin.github.io/labelImg/>`__

-  macOS. Binaries for macOS are not yet available. Help would be appreciated. At present, it must be `built from source <#macos>`__.

Build from source
~~~~~~~~~~~~~~~~~

Linux/Ubuntu/Mac requires at least `Python
2.6 <https://www.python.org/getit/>`__ and has been tested with `PyQt
4.8 <https://www.riverbankcomputing.com/software/pyqt/intro>`__.


Ubuntu Linux
^^^^^^^^^^^^
Python 2 + Qt4

.. code::

    sudo apt-get install pyqt4-dev-tools
    sudo pip install lxml
    make qt4py2
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Python 3 + Qt5

.. code::

    sudo apt-get install pyqt5-dev-tools
    sudo pip3 install lxml
    make qt5py3
    python3 labelImg.py
    python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

macOS
^^^^
Python 2 + Qt4

.. code::

    brew install qt qt4
    brew install libxml2
    make qt4py2
    python labelImg.py
    python  labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Python 3 + Qt5 (Works on macOS High Sierra)

.. code::

    brew install qt  # will install qt-5.x.x
    brew install libxml2
    make qt5py3
    python labelImg.py
    python  labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

**NEW** Python 3 Virtualenv + Binary  
This avoids a lot of the QT / Python version issues,
and gives you a nice .app file with a new SVG Icon
in your /Applications folder.

.. code::
    
    brew install python3
    pip install pipenv
    pipenv --three
    pipenv shell
    pip install pyqt5 lxml
    make qt5py3
    rm -rf build dist
    python setup.py py2app
    cp -rf dist/labelImg.app /Applications

Windows
^^^^^^^

Download and setup `Python 2.6 or
later <https://www.python.org/downloads/windows/>`__,
`PyQt4 <https://www.riverbankcomputing.com/software/pyqt/download>`__
and `install lxml <http://lxml.de/installation.html>`__.

Open cmd and go to `labelImg <#labelimg>`__ directory

.. code::

    pyrcc4 -o resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
    
Windows + anaconda
^^^^^^^

Download and install anaconda (python 3+)

Open cmd and go to `labelImg <#labelimg>`__ directory

.. code::

    conda install pyqt=4
    pyrcc4 -py3 -o resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Get from PyPI
~~~~~~~~~~~~~~~~~
.. code::

    pip install labelImg
    labelImg
    labelImg [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

I tested pip on Ubuntu 14.04 and 16.04. However, I didn't test pip on macOS and Windows

Use Docker
~~~~~~~~~~~~~~~~~
.. code::

    docker run -it \
    --user $(id -u) \
    -e DISPLAY=unix$DISPLAY \
    --workdir=$(pwd) \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    tzutalin/py2qt4

    make qt4py2;./labelImg.py

You can pull the image which has all of the installed and required dependencies. `Watch a demo video <https://youtu.be/nw1GexJzbCI>`__


Usage
-----

Steps (PascalVOC)
~~~~~

1. Build and launch using the instructions above.
2. Click 'Change default saved annotation folder' in Menu/File
3. Click 'Open Dir'
4. Click 'Create RectBox'
5. Click and release left mouse to select a region to annotate the rect
   box
6. You can use right mouse to drag the rect box to copy or move it

The annotation will be saved to the folder you specify.

You can refer to the below hotkeys to speed up your workflow.

Steps (YOLO)
~~~~~

1. In ``data/predefined_classes.txt`` define the list of classes that will be used for your training.

2. Build and launch using the instructions above.

3. Right below "Save" button in toolbar, click "PascalVOC" button to switch to YOLO format.

4. You may use Open/OpenDIR to process single or multiple images. When finished with single image, click save.

A txt file of yolo format will be saved in the same folder as your image with same name. A file named "classes.txt" is saved to that folder too. "classes.txt" defines the list of class names that your yolo label refers to.

Note:

- Your label list shall not change in the middle of processing a list of images. When you save a image, classes.txt will also get updated, while previous annotations will not be updated.

- You shouldn't use "default class" function when saving to YOLO format, it will not be referred.

- When saving as YOLO format, "difficult" flag is discarded.

Create pre-defined classes
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can edit the
`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__
to load pre-defined classes

Hotkeys
~~~~~~~

+------------+--------------------------------------------+
| Ctrl + u   | Load all of the images from a directory    |
+------------+--------------------------------------------+
| Ctrl + r   | Change the default annotation target dir   |
+------------+--------------------------------------------+
| Ctrl + s   | Save                                       |
+------------+--------------------------------------------+
| Ctrl + d   | Copy the current label and rect box        |
+------------+--------------------------------------------+
| Space      | Flag the current image as verified         |
+------------+--------------------------------------------+
| w          | Create a rect box                          |
+------------+--------------------------------------------+
| d          | Next image                                 |
+------------+--------------------------------------------+
| a          | Previous image                             |
+------------+--------------------------------------------+
| del        | Delete the selected rect box               |
+------------+--------------------------------------------+
| Ctrl++     | Zoom in                                    |
+------------+--------------------------------------------+
| Ctrl--     | Zoom out                                   |
+------------+--------------------------------------------+
| ↑→↓←       | Keyboard arrows to move selected rect box  |
+------------+--------------------------------------------+

How to contribute
~~~~~~~~~~~~~~~~~

Send a pull request

License
~~~~~~~
`Free software: MIT license <https://github.com/tzutalin/labelImg/blob/master/LICENSE>`_

Citation: Tzutalin. LabelImg. Git code (2015). https://github.com/tzutalin/labelImg

Related
~~~~~~~

1. `ImageNet Utils <https://github.com/tzutalin/ImageNet_Utils>`__ to
   download image, create a label text for machine learning, etc
2. `Use Docker to run labelImg <https://hub.docker.com/r/tzutalin/py2qt4>`__
3. `Generating the PASCAL VOC TFRecord files <https://github.com/tensorflow/models/blob/4f32535fe7040bb1e429ad0e3c948a492a89482d/research/object_detection/g3doc/preparing_inputs.md#generating-the-pascal-voc-tfrecord-files>`__
4. `App Icon based on Icon by Nick Roach (GPL)` <https://www.elegantthemes.com/> <https://www.iconfinder.com/icons/1054978/shop_tag_icon> __

