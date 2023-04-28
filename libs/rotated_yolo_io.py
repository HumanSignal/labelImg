#!/usr/bin/env python
# -*- coding: utf8 -*-
import math
import codecs
from libs.constants import DEFAULT_ENCODING


TXT_EXT = '.txt'
ENCODE_METHOD = DEFAULT_ENCODING


class RotatedYOLOWriter:

    def __init__(self, folder_name, filename, img_size, database_src='Unknown', local_img_path=None):
        self.folder_name = folder_name
        self.filename = filename
        self.database_src = database_src
        self.img_size = img_size
        self.box_list = []
        self.local_img_path = local_img_path
        self.verified = False

    def add_bnd_box(self, points, name, difficult):
        flat_points = []
        for x, y in points:
            flat_points.extend([x, y])
        bndbox = {'points': flat_points, 'name': name, 'difficult': difficult}
        self.box_list.append(bndbox)

    def save(self, target_file=None):
        out_file = None
        if target_file is None:
            out_file = codecs.open(
                self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(target_file, 'w', encoding=ENCODE_METHOD)

        for box in self.box_list:
            x1, y1, x2, y2, x3, y3, x4, y4 = box['points']
            out_file.write("%.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %s %s\n" % 
                (x1, y1, x2, y2, x3, y3, x4, y4, box['name'], box['difficult']))
        out_file.close()


class RotatedYOLOReader:

    def __init__(self, file_path):
        self.shapes = []
        self.file_path = file_path
        self.verified = False

        self.parse_rotated_yolo_format()

    def get_shapes(self):
        return self.shapes

    def get_angle(self, x1, y1, x2, y2):
        return math.degrees(math.atan2(y2 - y1, x2 - x1))
    
    def add_shape(self, x1, y1, x2, y2, x3, y3, x4, y4, label, difficult):
        angle = self.get_angle(x1, y1, x2, y2)
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.shapes.append((label, points, None, None, difficult, angle))

    def parse_rotated_yolo_format(self):
        bnd_box_file = open(self.file_path, 'r')
        for bndBox in bnd_box_file:
            x1, y1, x2, y2, x3, y3, x4, y4, label, difficult = bndBox.strip().split(' ')
            self.add_shape(float(x1), float(y1), float(x2), float(y2), float(x3), float(y3),
                float(x4), float(y4), label, int(difficult))
