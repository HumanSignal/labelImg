#!/bin/sh

#OS Ubuntu 14.04
#Pacakges
#>  pyinstaller (2.1)
#>  wine (1.6.2)
#>  virtual-wine (0.1)
#>  python-2.7.8.msi
#>  pywin32-218.win32-py2.7.exe

## tool to install on Ubuntu
#$ sudo apt-get install pyinstaller
#$ sudo apt-get install wine

wget "https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi"
wget "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpywin32%2Ffiles%2Fpywin32%2FBuild%2520218%2F&ts=1359740579&use_mirror=netcologne"

### Clone a repo to create virtual wine env
git clone https://github.com/htgoebel/virtual-wine.git
apt-get install scons
./virtual-wine/vwine-setup venv_wine

#### Active virutal env
. venv_wine/bin/activate

### Use wine to install packages to virtual env
wine start python-2.7.8.msi
wine pywin32-218.win32-py2.7.exe
