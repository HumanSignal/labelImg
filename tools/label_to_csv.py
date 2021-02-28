#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: label_to_csv.py
Author: Justin Ruan
Contact: justin900429@gmail.com
Time: 2021.02.06
"""

import os
import argparse
import codecs

import pandas as pd


def txt2csv(location, training_dir, path_prefix):
    # Return list
    temp_res = []

    # Run through all the files
    for file in os.listdir(location):
        # Check the file name ends with txt
        #  and not class.txt
        if (not file.endswith(".txt")) | \
                (file == "classes.txt"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Read in txt as csv
        df_txt = pd.read_csv(file_whole_name, sep=" ", header=None)

        # Create data for each labels
        for index, row in df_txt.iterrows():
            # Temp array for csv, initialized by the training types
            temp_csv = [str(training_dir)]

            # gs://prefix/name/{image_name}
            cloud_path = f"{path_prefix}/{os.path.splitext(file)[0]}.jpg"
            temp_csv.append(cloud_path)

            # Class label
            temp_csv.append(class_labels[int(row[0])])

            # Add the upper left coordinate
            x_min = min(max(0.0, row[1] - row[3] / 2), 1.0)
            y_min = min(max(0.0, row[2] - row[4] / 2), 1.0)
            temp_csv.extend([x_min, y_min])

            # Add the lower left coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Add the lower right coordinate
            x_max = min(max(0.0, row[1] + row[3] / 2), 1.0)
            y_max = min(max(0.0, row[2] + row[4] / 2), 1.0)
            temp_csv.extend([x_max, y_max])

            # Add the upper right coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Append to the res
            temp_res.append(temp_csv)

    return temp_res


def xml2csv(location, training_dir, path_prefix):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    temp_res = []

    # Run through all the files
    for file in os.listdir(location):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Open the xml name
        tree = ET.parse(file_whole_name)
        root = tree.getroot()

        # Get the width, height of images
        #  to normalize the bounding boxes
        size = root.find("size")
        width, height = float(size.find("width").text), float(size.find("height").text)

        # Find all the bounding objects
        for label_object in root.findall("object"):
            # Temp array for csv, initialized by the training types
            temp_csv = [str(training_dir)]

            # gs://prefix/name/{image_name}
            cloud_path = f"{path_prefix}/{os.path.splitext(file)[0]}.jpg"
            temp_csv.append(cloud_path)

            # Class label
            temp_csv.append(label_object.find("name").text)

            # Bounding box coordinate
            bounding_box = label_object.find("bndbox")

            # Add the upper left coordinate
            x_min = float(bounding_box.find("xmin").text) / width
            y_min = float(bounding_box.find("ymin").text) / height
            temp_csv.extend([x_min, y_min])

            # Add the lower left coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Add the lower right coordinate
            x_max = float(bounding_box.find("xmax").text) / width
            y_max = float(bounding_box.find("ymax").text) / height
            temp_csv.extend([x_max, y_max])

            # Add the upper right coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Append to the res
            temp_res.append(temp_csv)

    return temp_res


if __name__ == "__main__":
    # Add the argument parse
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-p", "--prefix",
                       required=True,
                       type=str,
                       help="Bucket of the cloud storage path")
    arg_p.add_argument("-l", "--location",
                       type=str,
                       required=True,
                       help="Location of the label files")
    arg_p.add_argument("-m", "--mode",
                       type=str,
                       required=True,
                       help="'xml' for converting from xml and 'txt' for converting from txt")
    arg_p.add_argument("-o", "--output",
                       type=str,
                       default="res.csv",
                       help="Output name of csv file")
    arg_p.add_argument("-c", "--classes",
                       type=str,
                       default=os.path.join("..", "data", "predefined_classes.txt"),
                       help="Label classes path")
    args = vars(arg_p.parse_args())

    # Class labels
    class_labels = []

    # Load in the defined classes
    if os.path.exists(args["classes"]) is True:
        with codecs.open(args["classes"], 'r', 'utf8') as f:
            for line in f:
                line = line.strip()
                class_labels.append(line)
    else:  # Exit if errors occurred
        print(f"File: {args['classes']} not exists")
        exit(1)

    # Prefix of the cloud storage
    ori_prefix = f"gs://{args['prefix']}"

    # Array for final csv file
    res = []
    # Get all the file in dir
    for training_type_dir in os.listdir(args["location"]):
        # Get the dirname
        dir_name = f"{args['location']}/{training_type_dir}"

        # Check whether is dir
        if not os.path.isdir(dir_name):
            continue
            # Process the files

        for class_type_dir in os.listdir(dir_name):

            # Check whether is dir
            if not os.path.isdir(dir_name):
                continue

            prefix = f"{ori_prefix}/{class_type_dir}"

            # Convert the chosen extension to csv
            if args["mode"] == "txt":
                res.extend(txt2csv(f"{dir_name}/{class_type_dir}",
                                   training_type_dir,
                                   prefix))
            elif args["mode"] == "xml":
                res.extend(xml2csv(f"{dir_name}/{class_type_dir}",
                                   training_type_dir,
                                   prefix))
            else:
                print("Wrong argument for convert mode.\n"
                      "'xml' for converting from xml to csv\n"
                      "'txt' for converting from txt to csv")
                exit(1)

    # Write to the result csv
    res_csv = pd.DataFrame(res,
                           columns=["set", "path", "label",
                                    "x_min", "y_min",
                                    "x_max", "y_min",
                                    "x_max", "y_max",
                                    "x_min", "y_max"])
    res_csv.to_csv("res.csv", index=False, header=False)
