#!/bin/bash
### Window requires pyinstall v2.1
THIS_SCRIPT_PATH=`readlink -f $0`
THIS_SCRIPT_DIR=`dirname ${THIS_SCRIPT_PATH}`
cd pyinstaller
git checkout v2.1
cd ${THIS_SCRIPT_DIR}

. venv_wine/bin/activate
rm -r build
rm -r dist
rm labelImg.spec
wine c:/Python27/python.exe pyinstaller/pyinstaller.py --hidden-import=xml \
            --hidden-import=xml.etree \
            --hidden-import=xml.etree.ElementTree \
            --hidden-import=lxml.etree \
             -D -F -n labelImg -c "../labelImg.py" -p ../libs

FOLDER=$(git describe --abbrev=0 --tags)
FOLDER="windows_"$FOLDER
rm -rf "$FOLDER"
mkdir "$FOLDER"
cp dist/labelImg.exe $FOLDER
cp -rf ../data $FOLDER/data
zip "$FOLDER.zip" -r $FOLDER
