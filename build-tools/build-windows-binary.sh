#!/bin/bash
### Window requires pyinstall v2.1
wine python-3.6.4.exe
wine pywin32-221.win32-py3.6.exe
wine PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-22.exe
wine lxml-3.8.0.win32-py3.4.exe

THIS_SCRIPT_PATH=`readlink -f $0`
THIS_SCRIPT_DIR=`dirname ${THIS_SCRIPT_PATH}`
cd pyinstaller
git checkout v2.1
cd ${THIS_SCRIPT_DIR}
echo ${THIS_SCRIPT_DIR}

#. venv_wine/bin/activate
rm -r build
rm -r dist
rm labelImg.spec

wine c:/Python27/python.exe pyinstaller/pyinstaller.py --hidden-import=xml \
            --hidden-import=xml.etree \
            --hidden-import=xml.etree.ElementTree \
            --hidden-import=lxml.etree \
             -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../

FOLDER=$(git describe --abbrev=0 --tags)
FOLDER="windows_"$FOLDER
rm -rf "$FOLDER"
mkdir "$FOLDER"
cp dist/labelImg.exe $FOLDER
cp -rf ../data $FOLDER/data
zip "$FOLDER.zip" -r $FOLDER
