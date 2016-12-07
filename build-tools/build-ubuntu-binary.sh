#!/bin/bash
rm -r build
rm -r dist
rm labelImg.spec
python pyinstaller/pyinstaller.py --hidden-import=xml \
            --hidden-import=xml.etree \
            --hidden-import=xml.etree.ElementTree \
            --hidden-import=lxml.etree \
            --hidden-import=json \
            --hidden-import=numpy \
             -D -F -n labelImg -c "../labelImg.py" -p ../libs
