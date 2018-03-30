#!/bin/sh

THIS_SCRIPT_PATH=`readlink -f $0`
THIS_SCRIPT_DIR=`dirname ${THIS_SCRIPT_PATH}`
#OS Ubuntu 14.04
### Common packages for linux/windows
if [ ! -e "pyinstaller" ]; then
    git clone https://github.com/pyinstaller/pyinstaller
    cd pyinstaller
    cd ${THIS_SCRIPT_DIR}
fi

echo "Going to clone and download packages for building windows"
#Pacakges
#>  pyinstaller (2.1)
#>  wine (1.6.2)
#>  virtual-wine (0.1)
#>  python-2.7.8.msi
#>  pywin32-218.win32-py2.7.exe

## tool to install on Ubuntu
#$ sudo apt-get install wine

### Clone a repo to create virtual wine env
if [ ! -e "virtual-wine" ]; then
	git clone https://github.com/htgoebel/virtual-wine.git
fi

apt-get install scons
### Create virtual env
rm -rf venv_wine
./virtual-wine/vwine-setup venv_wine
#### Active virutal env
. venv_wine/bin/activate

### Use wine to install packages to virtual env
if [ ! -e "python-3.6.5.exe" ]; then
    wget "https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe"
fi

if [ ! -e "pywin32-221.win32-py3.6.exe" ]; then
    wget "http://nchc.dl.sourceforge.net/project/pywin32/pywin32/Build%20221/pywin32-221.win32-py3.6.exe"
fi

if [ ! -e "PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe" ]; then
    wget "http://nchc.dl.sourceforge.net/project/pyqt/PyQt5/PyQt-5.6/PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe"
fi

if [ ! -e "lxml-3.8.0.win32-py3.4.exe" ]; then
    wget "https://pypi.python.org/packages/fe/2f/be4904004de282c4a737eae310c9303f1ba275337dc49c7e8308b4c0f301/lxml-3.8.0.win32-py3.4.exe#md5=d6079121430ce01541d701e46ae87523"
fi

