import os
import sys
import unittest

class TestPascalVocRW(unittest.TestCase):

    def test_upper(self):
        dir_name = os.path.abspath(os.path.dirname(__file__))
        libs_path = os.path.join(dir_name, '..', 'libs')
        sys.path.insert(0, libs_path)
        from pascal_voc_io import PascalVocWriter
        from pascal_voc_io import PascalVocReader

        # Test Write/Read
        writer = PascalVocWriter('tests', 'test', (512, 512, 1), localImgPath='tests/test.512.512.bmp')
        difficult = 1
        writer.addBndBox(60, 40, 430, 504, 'person', difficult)
        writer.addBndBox(113, 40, 450, 403, 'face', difficult)
        writer.save('tests/test.xml')

        reader = PascalVocReader('tests/test.xml')
        shapes = reader.getShapes()

        personBndBox = shapes[0]
        face = shapes[1]
        self.assertEqual(personBndBox[0], 'person')
        self.assertEqual(personBndBox[1], [(60, 40), (430, 40), (430, 504), (60, 504)])
        self.assertEqual(face[0], 'face')
        self.assertEqual(face[1], [(113, 40), (450, 40), (450, 403), (113, 403)])


class TestCreateMLRW(unittest.TestCase):

    def test_a_write(self):
        dir_name = os.path.abspath(os.path.dirname(__file__))
        libs_path = os.path.join(dir_name, '..', 'libs')
        sys.path.insert(0, libs_path)
        from create_ml_io import CreateMLWriter

        person = {'label': 'person', 'points': ((65, 45), (420, 45), (420, 512), (65, 512))}
        face = {'label': 'face', 'points': ((245, 250), (350, 250), (350, 365), (245, 365))}

        expected_width = 105    # 350-245 -> create_ml_io.py ll 46
        expected_height = 115   # 365-250 -> create_ml_io.py ll 49
        expected_x = 297.5      # 245+105/2 -> create_ml_io.py ll 53
        expected_y = 307.5      # 250+115/2 > create_ml_io.py ll 54

        shapes = [person, face]
        output_file = dir_name + "/tests.json"

        writer = CreateMLWriter('tests', 'test.512.512.bmp', (512, 512, 1), shapes, output_file,
                                localimgpath='tests/test.512.512.bmp')
        writer.write()

        # check written json
        with open(output_file, "r") as file:
            inputdata = file.read()

        import json
        data_dict = json.loads(inputdata)[0]

        self.assertEqual('test.512.512.bmp', data_dict['image'], 'filename not correct in .json')
        self.assertEqual(2, len(data_dict['annotations']), 'outputfile contains to less annotations')
        face = data_dict['annotations'][1]
        self.assertEqual('face', face['label'], 'labelname is wrong')
        face_coords = face['coordinates']
        self.assertEqual(expected_width, face_coords['width'], 'calculated width is wrong')
        self.assertEqual(expected_height, face_coords['height'], 'calculated height is wrong')
        self.assertEqual(expected_x, face_coords['x'], 'calculated x is wrong')
        self.assertEqual(expected_y, face_coords['y'], 'calculated y is wrong')

    def test_b_read(self):
        dir_name = os.path.abspath(os.path.dirname(__file__))
        libs_path = os.path.join(dir_name, '..', 'libs')
        sys.path.insert(0, libs_path)
        from create_ml_io import CreateMLReader

        output_file = dir_name + "/tests.json"
        reader = CreateMLReader(output_file, 'tests/test.512.512.bmp')
        shapes = reader.get_shapes()
        face = shapes[1]

        self.assertEqual(2, len(shapes), 'shape count is wrong')
        self.assertEqual('face', face[0], 'label is wrong')

        face_coords = face[1]
        xmin = face_coords[0][0]
        xmax = face_coords[1][0]
        ymin = face_coords[0][1]
        ymax = face_coords[2][1]

        self.assertEqual(245, xmin, 'xmin is wrong')
        self.assertEqual(350, xmax, 'xmax is wrong')
        self.assertEqual(250, ymin, 'ymin is wrong')
        self.assertEqual(365, ymax, 'ymax is wrong')


if __name__ == '__main__':
    unittest.main()
