# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:18:00 2017

@author: JiancunWang
"""

import os
import xml.etree.ElementTree as ET

im_dir = r'C:\Users\Administrator\Desktop\data'

files = os.listdir(im_dir)
files=[file for file in files if file.find('.xml')!=-1]
listname=['xmin','ymin','xmax','ymax']


for file0 in files:
    fi=os.path.join(im_dir,file0)
    tree = ET.ElementTree(file=fi)
    txtfile=fi.replace('.xml','.txt')
    f = open(txtfile,'w')
    #打开xml文档
    
    for elem in tree.iter(tag='object'):
        print(elem[0].tag, elem[0].text)
        f.write(elem[0].text)
        
        for bnd in elem[4].iter():
            if bnd.tag=='xmin':
                xmin=bnd.text
                f.write(' '+bnd.text)
                print(xmin)
            if bnd.tag=='ymin':
                ymin=bnd.text
                f.write(' '+bnd.text)
                print(ymin)
            if bnd.tag=='xmax':
                width=int(bnd.text)-int(xmin)
                f.write(' '+str(width))
                print(str(width))
            if bnd.tag=='ymax':
                height=int(bnd.text)-int(ymin)
                f.write(' '+str(height))
                print(str(height))
                
            
        f.write('\n')
    f.close()
