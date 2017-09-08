import cv2
import numpy as np
import PIL.Image as Image
try:
    from PyQt5.QtGui import *
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *

CLASS_PALETTE = [
    0,  0,  0,
    80, 0,  0,
    0,  80, 0,
    80, 80, 0,
    0,  0,  80,
    80, 0,  80,
    0,  80, 80,
    80, 80, 80,
    125, 0,   0,
    0,   125, 0,
    125, 125, 0,
    0,   0,   125,
    125, 0,   125,
    0,   125, 125,
    125, 125, 125,
    255, 0,   0,
    0,   255, 0,
    255, 255, 0,
    0,   0,   255,
    255, 0,   255,
    0,   255, 255,
    255, 255, 255,
]
MAX_CLASSES = len(CLASS_PALETTE)

class Segmentation(object):
    """Image segmentation class."""

    def __init__(self, seg_label_path='data/labels.txt', img=None, size_thres=100):
        self._rect = (0, 0, 0, 0)
        self.radius = 3
        self._size_thres = size_thres
        self._img = None
        self._mask = None
        self.current_segment = []
        self._segments = {}
        self._labels = {}

    @staticmethod
    def _convertQImg(img):
        """Converts QImage to Numpy Array.
        This function is used internally for image conversion.
        """
        if isinstance(img, QPixmap):
            img_Q = img.toImage()
            img_size = (img_Q.size().height(), img_Q.size().width(), 4)
            buffer = img_Q.constBits()
            buffer.setsize(img_Q.byteCount())
            img_cv = np.ndarray(img_size, buffer=buffer, dtype=np.uint8)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGRA2BGR)
            return img_cv
        return None

    def update(self, img):
        """Updates with an image"""
        img_cv = self._convertQImg(img)
        self._img = img_cv
        self._mask = np.zeros(img_cv.shape[:2], dtype=np.uint8)
        self.clear()

    def save_seg(self, save_path, category_path=None):
        """Saves as a png image in 'P' mode of PIL.Image"""
        if self._segments is None:
            return

        base = np.zeros(self._img.shape[:2], dtype=np.uint8)
        for label, contour in sorted(self._segments.items()):
            index = self._get_index(label)
            cv2.drawContours(base, contour, -1, color=index, thickness=cv2.FILLED)
        img_pil = Image.fromarray(base, 'P')
        img_pil.putpalette(CLASS_PALETTE)
        img_pil.save(save_path)

    def get_current_segment(self):
        """Returns currently working segment"""
        return self.current_segment

    def get_all_segments(self):
        """Returns all segments"""
        return self._segments

    def create_mask(self, rect=None, init_with_rect=False):
        """Creates/Updates currently working segment with a newly drawn mask"""
        if init_with_rect and rect is None:
            raise ValueError('rect should be given when init_with_rect is True')

        bg_model = np.zeros((1, 65), dtype=np.float64)
        fg_model = np.zeros((1, 65), dtype=np.float64)
        init_mode = cv2.GC_INIT_WITH_RECT if init_with_rect else cv2.GC_INIT_WITH_MASK
        try:
            cv2.grabCut(self._img, self._mask, rect, bg_model, fg_model, 1, init_mode)
        except:
            raise ValueError("No mask is drawn priorly")
        segment = np.where((self._mask == 0) | (self._mask == 2), 0, 255).astype(np.uint8)

        contours = cv2.findContours(segment, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[1]
        if contours:
            current_contours = []
            for contour in contours:
                if cv2.arcLength(contour, False) > self._size_thres or cv2.contourArea(contour) > self._size_thres:
                    current_contours.append(contour)
            self.current_segment = current_contours

    def draw_fgmask(self, x, y):
        """Draw a foreground mask"""
        cv2.circle(self._mask, (int(x), int(y)), self.radius, cv2.GC_FGD, self.radius)

    def draw_bgmask(self, x, y):
        """Draw a background mask"""
        cv2.circle(self._mask, (int(x), int(y)), self.radius, cv2.GC_BGD, self.radius)

    def clear(self):
        self.current_segment = []
        self._segments = {}

    def _get_index(self, label):
        raise NotImplementedError()

    def _get_label(self, index=None):
        raise NotImplementedError()

    def load_seg(self, seg_path):
        """Loads a segmentation image"""
        raise NotImplementedError()

    def load_seg_label(self, seg_label_path):
        """Loads a label from a label file at the given path"""
        raise NotImplementedError()

    def freeze_segment(self, label=None):
        """Freezes currently working segment to save later"""
        raise NotImplementedError()


class SegmentationObject(Segmentation):
    def __init__(self, seg_label_path='', img=None, size_thres=100):
        super(SegmentationObject, self).__init__(seg_label_path, img, size_thres)

    def _get_index(self, label):
        if label in self._labels:
            index = self._labels[label]
        else:
            index = int(max(self._labels)) + 1
            self._labels[str(index)] = index
        return index

    def _get_label(self, index=None):
        if str(index) in self._labels:
            label = str(index)
        else:
            index = int(max(self._labels, key=(lambda key: self._labels[key]))) + 1
            label = str(index)
            self._labels[label] = index
        return label

    def load_seg(self, seg_path):
        if seg_path is None:
            return

        img_pil = Image.open(seg_path)
        img_cv = np.asarray(img_pil.getdata(), dtype=np.uint8).reshape((img_pil.size[1], img_pil.size[0]))
        base = np.zeros((img_pil.size[1], img_pil.size[0]), dtype=np.uint8)
        nb_category = img_pil.getextrema()[1]
        for index in range(1, nb_category+1):
            base[img_cv == index] = 255
            base[img_cv != index] = 0
            contours = cv2.findContours(base, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[1]
            if contours:
                label = self._get_label(index)
                self._labels[label] = index
                self._segments[label] = contours
        print(self._labels)

    def load_seg_label(self, seg_label_path):
        return

    def freeze_segment(self, label=None):
        if not self.current_segment:
            return

        label = self._get_label()
        self._segments[label] = self.current_segment
        self.current_segment = []

    def clear(self):
        super(SegmentationObject, self).clear()
        self._labels = {'0': 0}


class SegmentationClass(Segmentation):
    def __init__(self, seg_label_path='', img=None, size_thres=100):
        super(SegmentationClass, self).__init__(seg_label_path, img, size_thres)
        self.load_seg_label(seg_label_path)

    def _get_index(self, label):
        if label in self._labels:
            index = self._labels[label]
        else:
            raise KeyError('Label[%s] is not found. Check the label file.' % label)
        return index

    def _get_label(self, index=None):
        for key, val in self._labels.items():
            if val == index:
                label = key
                return label
        raise EOFError("Label for index[%d] is not found. Check the label file." % index)

    def load_seg(self, seg_path):
        if seg_path is None:
            return

        img_pil = Image.open(seg_path)
        img_cv = np.asarray(img_pil.getdata(), dtype=np.uint8).reshape((img_pil.size[1], img_pil.size[0]))
        base = np.zeros((img_pil.size[1], img_pil.size[0]), dtype=np.uint8)

        for label, index in self._labels.items():
            if index is 0:
                continue
            base[img_cv == index] = 255
            base[img_cv != index] = 0
            contours = cv2.findContours(base, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[1]
            if contours:
                self._segments[label] = contours
        print(self._labels)

    def load_seg_label(self, seg_label_path):
        import os
        if not os.path.exists(seg_label_path):
            return

        with open(seg_label_path, 'r') as f:
            for line in f:
                label, index = line.split()
                self._labels[label] = int(index)

    def freeze_segment(self, label=None):
        if label is None:
            raise ValueError("Label should be given when segmentation mode is in 'class'")
        if not self.current_segment:
            return

        if label in self._segments:
            contours = self._segments[label]
            for contour in self.current_segment:
                contours.append(contour)
            self._segments[label] = contours
        else:
            self._segments[label] = self.current_segment
        self.current_segment = []
