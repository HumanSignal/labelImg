import json
import os.path
import numpy
import Image
import sys
from pascal_voc_writer import PascalVocWriter
from base64 import b64encode, b64decode

class LabelFileError(Exception):
    pass

class LabelFile(object):
    # It might be changed as window creates
    suffix = '.lif'

    def __init__(self, filename=None):
        self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = json.load(f)
                imagePath = data['imagePath']
                imageData = b64decode(data['imageData'])
                lineColor = data['lineColor']
                fillColor = data['fillColor']
                shapes = ((s['label'], s['points'], s['line_color'], s['fill_color'])\
                        for s in data['shapes'])
                # Only replace data after everything is loaded.
                self.shapes = shapes
                self.imagePath = imagePath
                self.imageData = imageData
                self.lineColor = lineColor
                self.fillColor = fillColor
        except Exception, e:
            raise LabelFileError(e)

    def save(self, filename, shapes, imagePath, imageData,
            lineColor=None, fillColor=None):
        try:
            with open(filename, 'wb') as f:
                json.dump(dict(
                    shapes=shapes,
                    lineColor=lineColor, fillColor=fillColor,
                    imagePath=imagePath,
                    imageData=b64encode(imageData)),
                    f, ensure_ascii=True, indent=2)
        except Exception, e:
            raise LabelFileError(e)

    def savePascalVocFormat(self, filename, shapes, imagePath, imageData,
            lineColor=None, fillColor=None, databaseSrc=None):
        imgFolderPath = os.path.dirname(imagePath)

        # Folder name is implicitly set to VOC2007 for purpose of annotation
        # used in detection using py_faster_rcnn.
        #imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFolderName = "VOC2007"

        imgFileName = os.path.basename(imagePath)
        imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]
        imageShape = numpy.asarray(Image.open(imagePath)).shape
        # Martin Kersner, 2015/11/03
        writer = PascalVocWriter(imgFolderName, imgFileName,\
                                 imageShape, localImgPath=imagePath)
        bSave = False
        for shape in shapes:
            points = shape['points']
            label = shape['label']
            bndbox = LabelFile.convertPoints2BndBox(points)
            writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3], label)
            bSave = True

        if bSave:
            writer.save(targetFile = filename)
        return

    @staticmethod
    def isLabelFile(filename):
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == LabelFile.suffix

    @staticmethod
    def convertPoints2BndBox(points):
        xmin = sys.maxint
        ymin = sys.maxint
        xmax = -sys.maxint
        ymax = -sys.maxint
        for p in points:
            x = p[0]
            y = p[1]
            xmin = min(x,xmin)
            ymin = min(y,ymin)
            xmax = max(x,xmax)
            ymax = max(y,ymax)
        return (int(xmin), int(ymin), int(xmax), int(ymax))
