import abc

class FileWriter(metaclass=abc.ABCMeta):

    def __init__(self, img_folder_name, img_file_name,
                 img_shape, shapes, filename):
        self.folder_name = img_folder_name
        self.filename = img_file_name
        self.img_size = img_shape
        self.box_list = []
        self.verified = False
        self.shapes = shapes
        self.output_file = filename

    @abc.abstractmethod
    def save(self):
        # save labelfile format at location file path
        pass

class FileReader(metaclass=abc.ABCMeta):
    
    def __init__(self, file_path):
        self.shapes = []
        self.file_path = file_path
        self.verified = False

        try:
            self.parse_file()
        except:
            pass

    @abc.abstractmethod
    def add_shape(self):
        # append the shape to self.shapes
        pass

    @abc.abstractmethod
    def parse_file(self):
        # parse the label file then add all the shapes into self.shapes
        pass

    def get_shapes(self):
        # return the shapes of bounding boxes
        return self.shapes


