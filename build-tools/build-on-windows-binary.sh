rm -rf build
rm -rf dist
rm labelImg.spec

#--noupx \
pyinstaller --hidden-import=xml \
            --hidden-import=xml.etree \
            --hidden-import=xml.etree.ElementTree \
            --hidden-import=lxml.etree \
             -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../ \
             -p "C:/Users/u225426/AppData/Local/Continuum/anaconda3/Lib/site-packages/PyQt5/"