#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import copy
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from libs.constants import DEFAULT_ENCODING
from libs.ustr import ustr


XML_EXT = '.xml'
ENCODE_METHOD = DEFAULT_ENCODING


class Component(object):
    def __init__(self,name,w,h,location:tuple,difficult):
        self.name = name
        self.w = w
        self.h = h
        self.location = location
        self.difficult = difficult
    
    def __eq__(self, other) -> bool:
        return self.name == other.name and self.w == other.w and self.h == other.h and self.location == other.location
    
    def __str__(self):  # unnecessary
        return str(self.name)
    
    def __hash__(self) -> int:
        return hash(self.name) + hash(self.w) + hash(self.h) + hash(self.location)


class PascalVocWriter:

    def __init__(self, foldername, filename, imgSize,databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        '''reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        if self.verified:
            top.set('verified', 'yes')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        if self.localImgPath is not None:
            localImgPath = SubElement(top, 'path')
            localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = ustr(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            if int(float(each_object['ymax'])) == int(float(self.imgSize[0])) or (int(float(each_object['ymin']))== 1):
                truncated.text = "1" # max == height or min
            elif (int(float(each_object['xmax']))==int(float(self.imgSize[1]))) or (int(float(each_object['xmin']))== 1):
                truncated.text = "1" # max == width or min
            else:
                truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = str( bool(each_object['difficult']) & 1 )
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + XML_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


class PascalVocReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.components = []
        self.filepath = filepath
        self.verified = False
        try:
            self.parseXML()
        except:
            pass
    
    def sortShapes(self):
        heights = []
        for i in self.shapes:
            heights.append(i[1][2][1]-i[1][0][1])

        maxHeight = max(heights)
        resList = copy.deepcopy(self.components)
        t = 0
        sps = []

        while len(resList)>0:
            tt = t + 0.5
            f1 = list(filter(lambda x:x.location[1]<maxHeight*tt,resList))
            f1.sort(key=lambda x:x.location[0])
            for i in f1:
                xmin = i.location[0]
                ymin = i.location[1]
                xmax = xmin + i.w 
                ymax = ymin + i.h
                points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
                sps.append((i.name,points,None,None,i.difficult))
            resList = list(set(resList).difference(set(f1)))
            t = t + 1       
        return sps

    def getShapes(self):
        if len(self.shapes)<3:
            return self.shapes
        else:
            return self.sortShapes()

    def addShape(self, label, bndbox, difficult):
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        component = Component(label,xmax-xmin,ymax-ymin,(xmin,ymin),difficult)
        self.components.append(component)
        self.shapes.append((label, points, None, None, difficult))

    def parseXML(self):
        assert self.filepath.endswith(XML_EXT), "Unsupport file format"
        parser = etree.XMLParser(encoding=ENCODE_METHOD)
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text
            # Add chris
            difficult = False
            if object_iter.find('difficult') is not None:
                difficult = bool(int(object_iter.find('difficult').text))
            self.addShape(label, bndbox, difficult)
        return True
