#!/usr/bin/env python
from subprocess import call
call(["pyinstaller", "--onefile", "--windowed", "labelImg.py"])

# Now it is a workaround. It should use hook file
def readlines(filename):
    result = []
    with open(filename, "r") as ins:
        for line in ins:
            result.append(line)
    return result

lines = readlines('labelImg.spec')
for ind, line in enumerate(lines):
    if 'hiddenimports' in line:
        lines[ind] = "\t\t\t hiddenimports = ['cv2', 'json', 'lxml.etree', 'lxml', 'etree', 'xml.etree.ElementTree'],\n"
        print lines[ind]

FILE = open('labelImg.spec', "w")
FILE.writelines(lines)
FILE.close()

call(["pyinstaller", "labelImg.spec"])
