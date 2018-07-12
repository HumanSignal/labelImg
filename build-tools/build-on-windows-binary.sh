#!/bin/bash

rm -r build
rm -r dist
rm labelImg.spec

pyrcc5 -o ../resources.py ../resources.qrc

pyinstaller --hidden-import=xml \
            --hidden-import=xml.etree \
            --hidden-import=xml.etree.ElementTree \
            --hidden-import=lxml.etree \
            --hidden-import=PyQt5.sip \
             -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../
