#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
from pathlib import Path

from libs.constants import DEFAULT_ENCODING
import os

JSON_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING


class CreateMLWriter:
    def __init__(self, foldername, filename, imgsize, shapes, outputfile, databasesrc='Unknown', localimgpath=None):
        self.foldername = foldername
        self.filename = filename
        self.databasesrc = databasesrc
        self.imgsize = imgsize
        self.boxlist = []
        self.localimgpath = localimgpath
        self.verified = False
        self.shapes = shapes
        self.outputfile = outputfile

    def write(self):
        if os.path.isfile(self.outputfile):
            with open(self.outputfile, "r") as file:
                input_data = file.read()
                outputdict = json.loads(input_data)
        else:
            outputdict = []

        outputimagedict = {
            "image": self.filename,
            "annotations": []
        }

        for shape in self.shapes:
            points = shape["points"]

            xmin = points[0][0]
            ymin = points[2][1]
            xmax = points[1][0]
            ymax = points[0][1]

            width = xmax - xmin
            if width < 0:
                width = width * -1
            height = ymax - ymin
            if height < 0:
                height = height * -1
            # x and y from center of rect
            x = xmin + width / 2
            y = ymin + height / 2

            shapedict = {
                "label": shape["label"],
                "coordinates": {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                }
            }
            outputimagedict["annotations"].append(shapedict)

        # check if image already in output
        exists = False
        for i in range(0, len(outputdict)):
            if outputdict[i]["image"] == outputimagedict["image"]:
                exists = True
                outputdict[i] = outputimagedict
                break

        if not exists:
            outputdict.append(outputimagedict)

        Path(self.outputfile).write_text(json.dumps(outputdict), ENCODE_METHOD)


class CreateMLReader:
    def __init__(self, jsonpath, filepath):
        self.jsonpath: str = jsonpath
        self.shapes: list = []
        self.verified = False
        self.filename = filepath.split("/")[-1:][0]
        try:
            self.parse_json()
        except ValueError:
            print("JSON decoding failed")

    def parse_json(self):
        with open(self.jsonpath, "r") as file:
            inputdata = file.read()

        outputdict = json.loads(inputdata)
        self.verified = True

        for image in outputdict:
            if image["image"] == self.filename:
                for shape in image["annotations"]:
                    self.add_shape(shape["label"], shape["coordinates"])

    def add_shape(self, label, bndbox):
        xmin = bndbox["x"] - (bndbox["width"] / 2)
        ymin = bndbox["y"] + (bndbox["height"] / 2)

        xmax = bndbox["x"] + (bndbox["width"] / 2)
        ymax = bndbox["y"] - (bndbox["height"] / 2)

        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None, True))

    def get_shapes(self):
        return self.shapes
