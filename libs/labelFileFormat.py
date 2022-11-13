from libs.pascal_voc_io import PascalVocReader, PascalVocWriter, XML_EXT
from libs.yolo_io import YoloReader, YOLOWriter, TXT_EXT
from libs.create_ml_io import CreateMLReader, CreateMLWriter, JSON_EXT

class LabelFileFormat(object):
    def __init__(self, reader, writer, suffix, text, icon):
        self.reader = reader
        self.writer = writer
        self.suffix = suffix
        self.text = text
        self.icon = icon

    def read(*args, **kwargs):
        #! todo: implement read method
        pass

    def write(*args, **kwargs):
        writer.write(*args, **kwargs)


PascalVoc = LabelFileFormat(PascalVocReader,
                            PascalVocWriter,
                            XML_EXT,
                            'PascalVOC',
                            'format_voc')

Yolo = LabelFileFormat(YoloReader,
                       YOLOWriter,
                       TXT_EXT,
                       'Yolo',
                       'format_yolo')

CreateML = LabelFileFormat(CreateMLReader,
                           CreateMLWriter,
                           JSON_EXT,
                           'CreateML',
                           'format_createml')
