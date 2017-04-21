#!/usr/bin/env python
# -*- coding: utf8 -*-
import _init_path
import sys
from lxml import etree
import codecs

XML_EXT = '.xml'


class PascalVocWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
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
        rough_string = etree.tostring(elem, encoding='UTF-8')
        rough_string = str(rough_string, encoding="UTF-8")
        root = etree.XML(rough_string)
        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = etree.Element('annotation')
        top.set('verified', 'yes' if self.verified else 'no')

        folder = etree.SubElement(top, 'folder')
        folder.text = self.foldername

        filename = etree.SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = etree.SubElement(top, 'path')
        localImgPath.text = self.localImgPath

        source = etree.SubElement(top, 'source')
        database = etree.SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = etree.SubElement(top, 'size')
        width = etree.SubElement(size_part, 'width')
        height = etree.SubElement(size_part, 'height')
        depth = etree.SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = etree.SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = etree.SubElement(top, 'object')
            name = etree.SubElement(object_item, 'name')
            try:
                name.text = unicode(each_object['name'])
            except NameError:
                # Py3: NameError: name 'unicode' is not defined
                name.text = each_object['name']
            pose = etree.SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = etree.SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = etree.SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = etree.SubElement(object_item, 'bndbox')
            xmin = etree.SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = etree.SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = etree.SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = etree.SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + XML_EXT, 'w', encoding='utf-8')
        else:
            out_file = codecs.open(targetFile, 'w', encoding='utf-8')

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


class PascalVocReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        content = None
        with open(self.filepath, 'r') as xmlFile:
            content = xmlFile.read()

        if content is None:
            return False

        xmltree = etree.XML(content)
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
            self.addShape(label, bndbox)
        return True


# tempParseReader = PascalVocReader('test.xml')
# print tempParseReader.getShapes()
"""
# Test
tmp = PascalVocWriter('temp','test', (10,20,3))
tmp.addBndBox(10,10,20,30,'chair')
tmp.addBndBox(1,1,600,600,'car')
tmp.save()
"""
