===============================
LabelImg
===============================

.. image:: https://img.shields.io/pypi/v/labelimg.svg
        :target: https://pypi.python.org/pypi/labelimg

.. image:: https://img.shields.io/travis/tzutalin/labelImg.svg
        :target: https://travis-ci.org/tzutalin/labelImg

.. image:: https://readthedocs.org/projects/labelimg/badge/?version=latest
        :target: https://labelimg.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tzutalin/labelImg/shield.svg
     :target: https://pyup.io/repos/github/tzutalin/labelImg/
     :alt: Updates

LabelImg is a graphical image annotation tool.

It is written in Python and uses Qt for its graphical interface.

Annotations are saved as XML files in PASCAL VOC format, the format used by [ImageNet](http://www.image-net.org/).


* Free software: MIT license
* Documentation: https://labelimg.readthedocs.io.

.. image:: https://github.com/tzutalin/labelImg/raw/master/docs/images/demo.png
     :alt: Demo Image

Installation
============

Stable release
--------------

To install LabelImg, run this command in your terminal:

.. code-block:: console

    $ pip install labelimg

This is the preferred method to install LabelImg, as it will always install the most recent stable release. 

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

We also provide downloadable compiled versions. You can get the last stable version here:

* `Download LabelImg 1.2.2 for Windows`_
* `Download LabelImg 1.2.2 for Linux`_
* We do not provide binaries for macOS yet. Please install from with pip or from sources.

.. _Download LabelImg 1.2.2 for Windows: https://raw.githubusercontent.com/tzutalin/LabelImg/gh-pages/windows/windows_v1.2.2.zip
.. _Download LabelImg 1.2.2 for Linux: https://raw.githubusercontent.com/tzutalin/LabelImg/gh-pages/linux/linux_v1.2.2.zip

From sources
------------

The sources for LabelImg can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/tzutalin/labelImg

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/tzutalin/labelImg/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make qt
    $ python setup.py install


Once installed, LabelImg can be used by using the following command line:

.. code-block:: console

    $ labelimg

.. _Github repo: https://github.com/tzutalin/labelImg
.. _tarball: https://github.com/tzutalin/labelImg/tarball/master

See Also
========

1. `ImageNet Utils`_: Download image, create a label text for machine learning, etc

.. _ImageNet Utils: https://github.com/tzutalin/ImageNet_Utils
