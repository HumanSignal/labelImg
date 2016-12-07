#!/bin/sh

#OS Ubuntu 14.04
### Common packages for linux/windows
if [ ! -e "pyinstaller" ]; then
    git clone https://github.com/pyinstaller/pyinstaller
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
if [ ! -e "python-2.7.8.msi" ]; then
    wget "https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi"
fi

if [ ! -e "pywin32-218.win32-py2.7.exe" ]; then
    wget "http://nchc.dl.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe"
fi

wine msiexec -i python-2.7.8.msi
wine pywin32-218.win32-py2.7.exe
