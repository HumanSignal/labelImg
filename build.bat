rd /s /q dist build
del labelImg.spec

pyinstaller --hidden-import=xml --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree --hidden-import=PyQt5.sip -D -F -n labelImg -c "./labelImg.py" -p ./libs -p ./ --paths C:\Users\Administrator\Anaconda3\envs\labelimg\Lib\site-packages\PyQt5\Qt\bin
mkdir dist\data
xcopy data dist\data /s /e /y /i