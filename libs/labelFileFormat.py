from libs.pascal_voc_io import PascalVocReader, PascalVocWriter, XML_EXT
from libs.yolo_io import YoloReader, YOLOWriter, TXT_EXT
from libs.create_ml_io import CreateMLReader, CreateMLWriter, JSON_EXT

class LabelFileFormat(object):

    formats = []
    suffixes = []

    def __init__(self, reader, writer, suffix, text, icon):
        self.reader = reader
        self.writer = writer
        self.suffix = suffix
        self.text = text
        self.icon = icon
        self.formats.append(self)
        self.suffixes.append(self.suffix)

    def read(self, *args, **kwargs):
        self.file_reader = self.reader(*args, **kwargs)
        return self.file_reader.get_shapes()

    def write(self, *args, **kwargs):
        self.file_writer = self.writer(*args, **kwargs)
        self.file_writer.save()

    def __eq__(self, other):
        return (self.reader == other.reader and self.writer == other.writer)


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
