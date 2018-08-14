#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from math import cos, sin, pi
from libs.lib import distance
from functools import reduce
import sys

DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QColor(255, 0, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 128, 255, 155)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 0, 0)
MIN_Y_LABEL = 10


class Shape(object):
    P_SQUARE, P_ROUND = range(2)

    MOVE_VERTEX, NEAR_VERTEX = range(2)

    # The following class variables influence the drawing
    # of _all_ shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    point_type = P_ROUND
    point_size = 8
    scale = 1.0

    # const index that yields the index - identifier of the
    # rotation shape.
    INDEX_ROTATION_ENTITY = -1

    def __init__(self, label=None, line_color=None, difficult=False, paintLabel=False):
        self.label = label
        self.points = []
        self.pointsWithoutRotation= []
        self.currentAngle = 0 #< basically meta information
        self.fill = False
        self.selected = False
        self.difficult = difficult
        self.paintLabel = paintLabel

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }


        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

    def close(self):
        self._closed = True

    def reachMaxPoints(self):
        if len(self.points) >= 4:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)
            self.pointsWithoutRotation.append(point)

    def popPoint(self):
        """
        Removes a point from list and returns the point with currently applied rotation
        :return:
        """
        if self.points:
            self.pointsWithoutRotation.pop()
            return self.points.pop()

        return None

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def paint(self, painter):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QPainterPath()
            vrtx_path = QPainterPath()

            line_path.moveTo(self.points[0])
            # Uncommenting the following line will draw 2 paths
            # for the 1st vertex, and make it non-filled, which
            # may be desirable.
            #self.drawVertex(vrtx_path, 0)



            # in case this shape is selected, display the rotate
            # tool
            if self.selected:
                self.drawRotateVertex(vrtx_path)

            for i, p in enumerate(self.points):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)
            if self.isClosed():
                line_path.lineTo(self.points[0])

            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.fillPath(vrtx_path, self.vertex_fill_color)

            # Draw text at the top-left
            if self.paintLabel:
                min_x = sys.maxsize
                min_y = sys.maxsize
                for point in self.points:
                    min_x = min(min_x, point.x())
                    min_y = min(min_y, point.y())
                if min_x != sys.maxsize and min_y != sys.maxsize:
                    font = QFont()
                    font.setPointSize(8)
                    font.setBold(True)
                    painter.setFont(font)
                    if(self.label == None):
                        self.label = ""
                    if(min_y < MIN_Y_LABEL):
                        min_y += MIN_Y_LABEL
                    painter.drawText(min_x, min_y, self.label)

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)


    def getShapeRotationVertex(self, rotated=True):
        """
        :rotated: whether to use the rotated coordinates that are currently displayed
                  on the canvas or the unrotated ones (for mathematical computations).
        :return:  the location and the diameter of the rotation vertex.
        """
        # for the specified class of points, continue with the computation
        pts = self.points if rotated else self.pointsWithoutRotation
        if pts[0].x() > pts[1].x(): id1, id2 = 1, 0
        else: id1, id2 = 0, 1


        if len(pts) >= 4:
            eucl = lambda a : (a.x()**2. + a.y()**2.)**.5
            vec_points = pts[id1] - pts[id2]
            dist_points = eucl(vec_points)
            if dist_points > 0:
                # compute size of the shape
                d = self.point_size / self.scale
                des_len = 5 * d
                # compute the normal vector and add it to the center of the two points
                nrm = QPointF(-(vec_points.y() * des_len / dist_points),
                             vec_points.x() * des_len / dist_points)
                center_shape = self.getCenter()
                center_points = (pts[id1] + pts[id2])/2
                # find the candidate that lies farest from the center
                candidate1 = center_points + nrm
                candidate2 = center_points - nrm
                d1 = eucl(candidate1 - center_shape)
                d2 = eucl(candidate2 - center_shape)
                c2 = d1 < d2
                return (candidate2 if c2 else candidate1), d, c2, center_shape
        return None


    def drawRotateVertex(self, path):
        vertex_info_orig= self.getShapeRotationVertex(False)
        vertex_info= self.getShapeRotationVertex(True)
        if vertex_info is not None:
            path.addEllipse(vertex_info[0], vertex_info[1], vertex_info[1])
            path.moveTo(vertex_info[3])
            path.lineTo(vertex_info[0])
            path.moveTo(vertex_info[3])
            if vertex_info_orig is not None:
                path.lineTo(vertex_info_orig[0])

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Shape.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"


    def getCenter(self, rotated=True):
        """
        :param rotated: whether to use the original parameters or the rotated ones.
                        best choice depends on which operation is currently executed.
                        In case a rotation is executed, use the original data as the
        :return:        the center of mass of the vertex
        """
        p = self.points if rotated else self.pointsWithoutRotation
        return reduce((lambda x, y: x + y), p) / len(p)


    def getClosestVertex(self, point, epsilon):
        """
        Returns the index and distance of shape's nearest vertex to a specified :point:
        in case the distance is smaller or equal to the threshold :epsilon:.
        Otherwise return None.

        :param point:       the position to which the vertices are to be comapred
        :param epsilon:     a threshold that indicates when to accept a point as
                            close enough to be considered to be returned.
        :return:            index, distance to the closest element if distance < epsilon, else none.
        """
        default_index = -2
        sel_distance, sel_index = default_index, default_index
        for i, p in enumerate(self.points):
            d = distance(p-point)
            if d <= epsilon:
                if sel_distance == default_index or sel_distance > d:
                    sel_index, sel_distance, = i, d

        # Only in case the current element is selected,
        # check the position of the rotate element.
        if self.selected:
            rot_info = self.getShapeRotationVertex(True)
            if rot_info is not None:
                d = distance(point-rot_info[0])
                d = distance(point-rot_info[0])
                if d <= epsilon*2:
                    if sel_distance == default_index or sel_distance > d:
                        sel_index, sel_distance, = Shape.INDEX_ROTATION_ENTITY, d



        return (sel_index, sel_distance) if sel_index != default_index else None

    def containsPoint(self, point):
        return self.makePath().contains(point)


    def makePath(self):
        path = QPainterPath(self.points[0])
        for p in self.points[1:]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def shift(self, offset):
        self.pointsWithoutRotation = list(map(lambda a : a + offset, self.pointsWithoutRotation))
        self.points = list(map(lambda a : a + offset, self.points))

    def moveBy(self, offset):
        self.pointsWithoutRotation = list(map(lambda a : a + offset, self.pointsWithoutRotation))

    def applyRotationAngle(self, angle, shape_center, fromUnrotated=True):
        """
        Applies a rotation angle either based on the unrotated data (standard)
        or on the basis of the rotated data for resetting the unrotated data.

        In case the boundaries of the image are not met, the shape is  resized
        to fit into the image boundaries. That way, in-range values are guaranteed.

        :param angle:           angle for rotation
        :param shape_center:    the point around which all points are rotated
        :param fromUnrotated:   true, if the unrotated coordinates are up to data and
                                the rotated ones are to be updated accordingly.
                                If false the other way around
        """
        # It might be best if there is some discretisation for the rotation that can be configured.
        # Comment the following code in for an angle discretisation
        #
        # amountOfSteps = 50
        # angle = int(angle * amountOfSteps / pi)
        # angle = angle / amountOfSteps * pi

        self.currentAngle = angle
        if not fromUnrotated: angle *= -1

        for i in range(len(self.points)):
            if fromUnrotated:
                dc = self.pointsWithoutRotation[i] - shape_center
                self.points[i] = QPointF(shape_center.x() + cos(angle) * dc.x() - sin(angle) * dc.y(),
                                         shape_center.y() + sin(angle) * dc.x() + cos(angle) * dc.y())
            else:
                dc = self.points[i] - shape_center
                self.pointsWithoutRotation[i] = QPointF(shape_center.x() + cos(angle) * dc.x() - sin(angle) * dc.y(),
                                                        shape_center.y() + sin(angle) * dc.x() + cos(angle) * dc.y())


    @staticmethod
    def rotatePoint(toRotate, center, angle):
        """Utility function"""
        dc = toRotate - center
        return QPointF(center.x() + cos(angle) * dc.x() - sin(angle) * dc.y(),
                       center.y() + sin(angle) * dc.x() + cos(angle) * dc.y())


    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action


    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        shape = Shape("%s" % self.label)
        shape.points = [p for p in self.points]
        shape.pointsWithoutRotation = [p for p in self.pointsWithoutRotation]
        shape.fill = self.fill
        shape.selected = self.selected
        shape._closed = self._closed
        if self.line_color != Shape.line_color:
            shape.line_color = self.line_color
        if self.fill_color != Shape.fill_color:
            shape.fill_color = self.fill_color
        shape.difficult = self.difficult
        return shape

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
