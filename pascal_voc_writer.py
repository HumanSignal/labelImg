import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from lxml import etree

class PascalVocWriter:
    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem,'utf8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None or \
                len(self.boxlist) <= 0:
                    return None

        top = Element('annotation')
        folder = SubElement(top,'folder')
        folder.text = self.foldername

        filename = SubElement(top,'filename')
        filename.text = self.filename

        localImgPath = SubElement(top,'path')
        localImgPath.text = self.localImgPath

        source = SubElement(top,'source')
        database = SubElement(source,'database')
        database.text = self.databaseSrc

        size_part = SubElement(top,'size')
        width = SubElement(size_part,'width')
        height = SubElement(size_part,'height')
        depth = SubElement(size_part,'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize)==3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top,'segmented')
        segmented.text ='0'

        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name):
        bndbox = {'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax}
        bndbox['name'] = name
        self.boxlist.append(bndbox);

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top,'object')
            name = SubElement(object_item, 'name')
            name.text = str(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile = None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = open(self.filename + '.xml','w')
        else:
            out_file = open(targetFile, 'w')

        out_file.write(self.prettify(root))
        out_file.close()

"""
# Test
tmp = PascalVocWriter('temp','test', (10,20,3))
tmp.addBndBox(10,10,20,30,'chair')
tmp.addBndBox(1,1,600,600,'car')
tmp.save()
"""

