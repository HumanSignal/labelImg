# LabelImg

LabelImg is a graphical image annotation tool

It is written in Python and uses Qt for its graphical interface.

The annotation file will be saved as a XML file. The annotation format is Piscal VOC format, and the format is the same as [ImageNet](http://www.image-net.org/)

## Dependencies
Requires at least [Python 2.6](http://www.python.org/getit/) and has been tested with [PyQt
4.8](http://www.riverbankcomputing.co.uk/software/pyqt/intro).

In order to build the resource and assets, you need to install python-qt4 python-qt4-dev pyqt4-dev-tools ...

## Usage
After cloning the code, you should run `make` to generate the resource file.

You can then start annotating by running `./labelImg.py`. For usage
instructions you can view the screencast tutorial from the `Help` menu.

At the moment annotations are saved as a XML file. The format is Piscal VOC format, and the format is the same as [ImageNet](http://www.image-net.org/)



