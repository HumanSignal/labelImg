
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

#from PyQt4.QtOpenGL import *

from libs.shape import Shape
from libs.lib import distance
from math import acos, cos, sin, pi, sqrt
from time import *

CURSOR_DEFAULT = Qt.ArrowCursor
CURSOR_POINT = Qt.PointingHandCursor
CURSOR_DRAW = Qt.CrossCursor
CURSOR_MOVE = Qt.ClosedHandCursor
CURSOR_GRAB = Qt.OpenHandCursor
CURSOR_ROTATE = Qt.SizeAllCursor

# class Canvas(QGLWidget):


class Canvas(QWidget):
    zoomRequest = pyqtSignal(int)
    scrollRequest = pyqtSignal(int, int)
    newShape = pyqtSignal()
    selectionChanged = pyqtSignal(bool)
    shapeMoved = pyqtSignal()
    drawingPolygon = pyqtSignal(bool)

    CREATE, EDIT = list(range(2))

    epsilon = 11.0

    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        # Initialise local state.
        self.mode = self.EDIT
        self.shapes = []
        self.current = None
        self.selectedShape = None  # save the selected shape here
        self.selectedShapeCopy = None
        self.drawingLineColor = QColor(0, 0, 255)
        self.drawingRectColor = QColor(0, 0, 255) 
        self.line = Shape(line_color=self.drawingLineColor)
        self.prevPoint = QPointF()
        self.scale = 1.0
        self.pixmap = QPixmap()
        self.visible = {}
        self._hideBackround = False
        self.hideBackround = False
        self.hShape = None
        self.hVertex = None
        self._painter = QPainter()
        self._cursor = CURSOR_DEFAULT
        # Menus:
        self.menus = (QMenu(), QMenu())
        # Set widget options.
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)
        self.verified = False

    def setDrawingColor(self, qColor):
        self.drawingLineColor = qColor
        self.drawingRectColor = qColor

    def enterEvent(self, ev):
        self.overrideCursor(self._cursor)

    def leaveEvent(self, ev):
        self.restoreCursor()

    def focusOutEvent(self, ev):
        self.restoreCursor()

    def isVisible(self, shape):
        return self.visible.get(shape, True)

    def drawing(self):
        return self.mode == self.CREATE

    def editing(self):
        return self.mode == self.EDIT

    def setEditing(self, value=True):
        self.mode = self.EDIT if value else self.CREATE
        if not value:  # Create
            self.unHighlight()
            self.deSelectShape()
        self.prevPoint = QPointF()
        self.repaint()

    def unHighlight(self):
        if self.hShape:
            self.hShape.highlightClear()
        self.hVertex = self.hShape = None

    def selectedVertex(self):
        return self.hVertex is not None

    def mouseMoveEvent(self, ev):
        """Update line with last point and current coordinates."""
        pos = self.transformPos(ev.pos())

        # Update coordinates in status bar if image is opened
        window = self.parent().window()
        if window.filePath is not None:
            self.parent().window().labelCoordinates.setText(
                'X: %d; Y: %d' % (pos.x(), pos.y()))

        # Polygon drawing.
        if self.drawing():
            self.overrideCursor(CURSOR_DRAW)
            if self.current:
                color = self.drawingLineColor
                if self.outOfPixmap(pos):
                    # Don't allow the user to draw outside the pixmap.
                    # Project the point to the pixmap's edges.
                    pos = self.intersectionPoint(self.current[-1], pos)
                elif len(self.current) > 1 and self.closeEnough(pos, self.current[0]):
                    # Attract line to starting point and colorise to alert the
                    # user:
                    pos = self.current[0]
                    color = self.current.line_color
                    self.overrideCursor(CURSOR_POINT)
                    self.current.highlightVertex(0, Shape.NEAR_VERTEX)
                self.line[1] = pos
                self.line.line_color = color
                self.prevPoint = QPointF()
                self.current.highlightClear()
            else:
                self.prevPoint = pos
            self.repaint()
            return

        # Polygon copy moving.
        if Qt.RightButton & ev.buttons():
            if self.selectedShapeCopy and self.prevPoint:
                self.overrideCursor(CURSOR_MOVE)
                self.boundedMoveShape(self.selectedShapeCopy, pos)
                self.repaint()
            elif self.selectedShape:
                self.selectedShapeCopy = self.selectedShape.copy()
                self.repaint()
            return

        # Polygon/Vertex moving.
        if Qt.LeftButton & ev.buttons():
            if self.selectedVertex():
                self.boundedMoveVertex(pos)
                self.shapeMoved.emit()
                self.repaint()
            elif self.selectedShape and self.prevPoint:
                self.overrideCursor(CURSOR_MOVE)
                self.boundedMoveShape(self.selectedShape, pos)
                self.shapeMoved.emit()
                self.repaint()
            return

        # Just hovering over the canvas, 2 possibilities:
        # - Highlight shapes
        # - Highlight vertex
        # Update shape/vertex fill and tooltip value accordingly.
        self.setToolTip("Image")

        # Declaration of variables storing selection criterion and information and the selected items themselves:
        vertex_selected = None
        vertex_min_dist = 0
        shape_selected = None
        shape_min_len = 0
        for shape in self.shapes:
            if self.isVisible(shape):

                # Iteratively find the vertex that is closest to the
                # specified point. Vertices are prioritised to shapes
                vertex_info = shape.getClosestVertex(pos, self.epsilon)

                if vertex_info:
                    index, dist = vertex_info
                    if vertex_selected is None or dist < vertex_min_dist:
                        vertex_selected = index, shape
                        vertex_min_dist = dist

                # In case no vertex has been found yet, check if the
                # current shape contains the point. Select the shape
                # with the smallest length (as length indicates whether
                # the shape is likely to to be completely covered by
                # a different shape.
                elif not vertex_selected:
                    path = shape.makePath()
                    contains = path.contains(pos)
                    if contains:
                        length = path.length()
                        if not shape_selected or length < shape_min_len:
                            shape_selected = shape
                            shape_min_len = length

        # update the graphical user interface accordingly
        if vertex_selected is not None:
            if self.selectedVertex():
                self.hShape.highlightClear()

            self.hVertex, self.hShape = vertex_selected
            self.hShape.highlightVertex(self.hVertex, self.hShape.MOVE_VERTEX)
            self.setToolTip("Click & drag to move point")
            if self.hVertex == Shape.INDEX_ROTATION_ENTITY:
                self.overrideCursor(CURSOR_ROTATE)
            else:
                self.overrideCursor(CURSOR_POINT)
            self.setStatusTip(self.toolTip())
            self.update()

        elif shape_selected is not None:

            if self.selectedVertex():
                self.hShape.highlightClear()

            self.hVertex, self.hShape = None, shape_selected
            self.setToolTip(
                "Click & drag to move shape '%s'" % shape_selected.label)
            self.setStatusTip(self.toolTip())
            self.overrideCursor(CURSOR_GRAB)
            self.update()
        else:
            # Nothing found, clear highlights, reset state.
            if self.selectedVertex():
                self.hShape.highlightClear()
            self.hVertex, self.hShape = None, None
            self.overrideCursor(CURSOR_DEFAULT)
            self.update()

    def mousePressEvent(self, ev):
        pos = self.transformPos(ev.pos())

        if ev.button() == Qt.LeftButton:
            if self.drawing():
                self.handleDrawing(pos)
            else:
                self.selectShapePoint(pos)
                self.prevPoint = pos
                self.repaint()
                pass
        elif ev.button() == Qt.RightButton and self.editing():
            self.selectShapePoint(pos)
            self.prevPoint = pos
            self.repaint()

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.RightButton:
            menu = self.menus[bool(self.selectedShapeCopy)]
            self.restoreCursor()
            if not menu.exec_(self.mapToGlobal(ev.pos()))\
               and self.selectedShapeCopy:
                # Cancel the move by deleting the shadow copy.
                self.selectedShapeCopy = None
                self.repaint()
        elif ev.button() == Qt.LeftButton and self.selectedShape:
            if self.selectedVertex():
                self.overrideCursor(CURSOR_POINT)
            else:
                self.overrideCursor(CURSOR_GRAB)
        elif ev.button() == Qt.LeftButton:
            pos = self.transformPos(ev.pos())
            if self.drawing():
                self.handleDrawing(pos)

    def endMove(self, copy=False):
        assert self.selectedShape and self.selectedShapeCopy
        shape = self.selectedShapeCopy
        #del shape.fill_color
        #del shape.line_color
        if copy:
            self.shapes.append(shape)
            self.selectedShape.selected = False
            self.selectedShape = shape
            self.repaint()
        else:
            self.selectedShape.points = [p for p in shape.points]
        self.selectedShapeCopy = None

    def hideBackroundShapes(self, value):
        self.hideBackround = value
        if self.selectedShape:
            # Only hide other shapes if there is a current selection.
            # Otherwise the user will not be able to select a shape.
            self.setHiding(True)
            self.repaint()

    def handleDrawing(self, pos):
        if self.current and self.current.reachMaxPoints() is False:
            initPos = self.current[0]
            minX = initPos.x()
            minY = initPos.y()
            targetPos = self.line[1]
            maxX = targetPos.x()
            maxY = targetPos.y()
            self.current.addPoint(QPointF(maxX, minY))
            self.current.addPoint(targetPos)
            self.current.addPoint(QPointF(minX, maxY))
            self.finalise()
        elif not self.outOfPixmap(pos):
            self.current = Shape()
            self.current.addPoint(pos)
            self.line.points = [pos, pos]
            self.setHiding()
            self.drawingPolygon.emit(True)
            self.update()

    def setHiding(self, enable=True):
        self._hideBackround = self.hideBackround if enable else False

    def canCloseShape(self):
        return self.drawing() and self.current and len(self.current) > 2

    def mouseDoubleClickEvent(self, ev):
        # We need at least 4 points here, since the mousePress handler
        # adds an extra one before this handler is called.
        if self.canCloseShape() and len(self.current) > 3:
            self.current.popPoint()
            self.finalise()

    def selectShape(self, shape):
        shape.selected = True
        self.selectedShape = shape
        self.setHiding()
        self.selectionChanged.emit(True)
        self.update()

    def selectShapePoint(self, point):
        """Select the first shape created which contains this point."""
        self.deSelectShape()
        if self.selectedVertex():
            index, shape = self.hVertex, self.hShape
            shape.highlightVertex(index, shape.MOVE_VERTEX)
            self.selectShape(shape)
        elif self.hShape is not None:
            self.selectShape(self.hShape)



    def boundedMoveVertex(self, pos):
        """
        Code executed when dragging a vertex.
        This can imply two different operations:
        1.  Rotation of the vertex
        2.  Stretch the vertex
        :param pos:         the 'new' position of the vertex in question
        """
        index, shape = self.hVertex, self.hShape
        if index == Shape.INDEX_ROTATION_ENTITY:
            self.rotateShape(pos, shape)
        else:
            self.resizeShape(pos, index, shape)


    def getClosestValid(self, point):
        """
        Return the point that is closest to any point inside the rectangle.
        Especially, if the point itself is inside, return the point.
        """
        return QPointF(max(min(point.x(), self.pixmap.width() - 1), 0), 
                max(min(point.y(),self.pixmap.height() - 1),0))

    def rotateShape(self, pos, shape, debug=True):
        """
        Rotates a shape by dragging the shape-rotation-button to the position 
        `pos`.

        Checks if the resulting shape is completely inside the image in the 
        image. If not, rotate by an angle that is closest to the desired angle
        but still yielding a shape inside the image.
        """

        # Case 1: Rotate the shape
        vertex_not_rotated = shape.getShapeRotationVertex(False)
        if vertex_not_rotated is not None:
            eucl_sq = lambda a : a.x()**2 + a.y()**2

            # Fetch the original (=not rotated) vertex-position for movement
            # and the center of mass of the shape (once again according to 
            # the coordinates that are not rotated)
            vertex_point = vertex_not_rotated[0]
            vertex_mirrored = vertex_not_rotated[2]
            shape_center = shape.getCenter(False)

            # Compute the vector and distance between both aforementioned points
            vec_old_center = vertex_point - shape_center# - vertex_point
            dist_old_center_square = eucl_sq(vec_old_center)

            # Compute the vector and distance between the new position and the center
            vec_new_center = pos - shape_center# - pos
            dist_new_center_square = eucl_sq(vec_new_center)

            # Now compute the angle between both the vector pointing to the new
            # position of the rotation vertex and the one pointing to its 
            # original position.
            # Make completely sure that no rounding errors can cause 
            # mathematical errors for the input value by checking bounds.
            val = QPointF.dotProduct(vec_new_center, vec_old_center) / \
                (dist_new_center_square * dist_old_center_square) **.5
            val = min(max(val, -1), 1)
            angle = acos(val)

            # The direction of movement has to be adapted depending on the
            # current state of the vertex.
            # First condition:  vertex is 'mirrored':
            #                   the initially topmost line is dragged under line 
            #                   at the bottom; In this case the sign must be
            #                   swapped.
            # Second condition: as the shape-move vertex is always
            #                   directly above or beneath the shape's center
            #                   it is succicent to check the x coordinate for
            #                   checking if the rotation is 'in the second
            #                   half'. In that case, rotate by 2pi -angle
            transform_angle = lambda a, posx :  \
                    (-1 if vertex_mirrored else 1)  \
                    * (a if (posx >= vertex_point.x()) else 2. * pi - a)
            angle = transform_angle(angle, pos.x())

            # Not all angles are valid. Find out which angles are leading to
            # coordiantes outside the image:
            # Step 1)       find (x,y) with \|(x,y) - c \| = \|x_1 - x_3\|
            #               and (x,y) on image's borders
            # Step 2)       find the associated rotation angles and store them
            #               in a sorted way
            width, height = self.pixmap.width(), self.pixmap.height()
            # get the radius of the circle
            p_c = shape.pointsWithoutRotation[0] - shape_center
            len_p_c = eucl_sq(p_c)
            # list all the support vectors indicating image border alongside 
            # with their directions
            support_direction = [
                    [QPointF(0,0), QPointF(width-1,0)],
                    [QPointF(0,0), QPointF(0,height-1)],
                    [QPointF(width-1,0), QPointF(0,height-1)],
                    [QPointF(0,height-1), QPointF(width-1,0)]]
            forbiddenAngleIntervals = []
            for s, d in support_direction:
                # find intersections between the circle (defined by the center
                # and its radius) and the currently considered image border.
                #
                # In case there is only one (or none) intersection, 
                # no conditions are imposed in this step on the anlge as the
                # image borders are selected to be the last line of pixels
                # inside the image. 
                #
                # If there are two intersections, the space in between them is
                # forbidden
                intersects = Canvas.intersectionLineCircle(s - shape_center, d, 
                        sqrt(len_p_c))
                if intersects is not None:

                    # In case debugging is enabled, add new shapes that show
                    # the intersections with the borders in the image. 
                    # Attention: debugging cannot be used in a productive mode.
                    # Results in a bunch of new vertices.
                    if debug:
                        deb = Shape()
                        deb.addPoint(intersects[0] + shape_center)
                        deb.addPoint(intersects[1] + shape_center)
                        deb.close()
                        self.shapes.append(deb)

                        deb = Shape()
                        deb.addPoint(p_c + shape_center)
                        deb.close()
                        self.shapes.append(deb)

                    # the corresponding angle is the angle between the
                    # intersection point and the  vertex_point (shifted by
                    # center)
                    if len(intersects) == 2:

                        angles = [[transform_angle(acos(
                            QPointF.dotProduct(spwr - shape_center, a)
                            / (len_p_c * eucl_sq(a)) **.5), spwr.x())
                            for a in intersects] 
                            for spwr in shape.pointsWithoutRotation]

                        for i, (a, b) in enumerate(angles):
                            # find the min and max value and compute the
                            # min and max value that are still allowed.
                            # if the angle might be affected by them
                            t = 0
                            if a < 0: a += 2*pi; 
                            if b < 0: b += 2*pi
                            mx, mi = max(a, b), min(a,b)
                            if mx - mi > pi:
                                forbiddenAngleIntervals.append([mx, 2*pi])
                                forbiddenAngleIntervals.append([0, mi])
                            else:
                                forbiddenAngleIntervals.append([mi, mx])

                            #if a < b:
                            #    forbiddenAngleIntervals.append([a, b])
                            #elif b < a:
                            #    forbiddenAngleIntervals.append([a, 2*pi])
                            #    forbiddenAngleIntervals.append([0, b])

                            # paint vector (forbidden area) based on the
                            # computed angle
                            if debug:
                                p1 = Shape.rotatePoint(
                                        shape.pointsWithoutRotation[i], 
                                        shape_center, a)
                                p2 = Shape.rotatePoint(
                                        shape.pointsWithoutRotation[i], 
                                        shape_center, b)

                                deb = Shape()
                                deb.addPoint(p1)
                                deb.addPoint(p2)
                                deb.close()
                                self.shapes.append(deb)


            # XXX: There most likely is a better solution to this.
            #      The code below is supposed to unite all forbidden intervals.
            #      This is necessary for being able to pick the closest point
            #      to the forbidden area.
            if len(forbiddenAngleIntervals):
                unionInterval = [forbiddenAngleIntervals[0]]
                uiid = 0
                # starts before other.end and stops after other.start
                checkIntersect = lambda a, b: a[1] >= b[0] and a[0] <= b[1]
                checkIntersectMutual = lambda a, b: checkIntersect(a, b) \
                        or checkIntersect(b, a)
                # need to check multiple times as there might be an array that
                # unites two other arrays.
                for k in range(len(forbiddenAngleIntervals)-1):
                    for i in range(1, len(forbiddenAngleIntervals)):
                        # check if there is already is an interval comprising me
                        inters = False
                        for ui in range(len(unionInterval)):
                            # end union > start this
                            if (checkIntersectMutual(
                                unionInterval[ui], forbiddenAngleIntervals[i])):
                                unionInterval[ui][0] = min(unionInterval[ui][0], 
                                        forbiddenAngleIntervals[i][0])
                                unionInterval[ui][1] = max(unionInterval[ui][1], 
                                        forbiddenAngleIntervals[i][1])
                                inters = True
                                break;
                        if not inters:
                            unionInterval.append(forbiddenAngleIntervals[i])

                print(forbiddenAngleIntervals, unionInterval)

                # Check if there is some intersection and use the closest point
                # as corrected angle.
                if angle < 0: angle += 2*pi
                for i in unionInterval:
                    if i[0] < angle and angle < i[1]:
                        angle = i[0] if angle-i[0]< i[1]- angle else i[1]
                        break

            # Apply the rotation for the shape (computes new location of rotated
            # values and stores the current angle for future reference):
            shape.applyRotationAngle(angle, shape_center)


    def resizeShape(self, pos, index, shape):
        """
        Resize shape of rectangle, enforcing rectangular form in the original 
        coordinates


        """

        dot = lambda x, y: x.x() * y.x() + x.y() * y.y()
        eucl = lambda a : 1.*a.x()**2 + 1.*a.y()**2
        rot = lambda p, a: Shape.rotatePoint(p, QPointF(0, 0), a)
        rotShapeLine = lambda i, ia, s: rot(
                s.pointsWithoutRotation[ia] - s.pointsWithoutRotation[i], 
                s.currentAngle)

        if shape.points[index] != pos:

            # give reasonable names to the vectices that are affected ('left'
            # and 'right' and to the vertex that remains unaffected 'other')
            rindex, lindex, oindex = [(index + o) % 4 for o in [1, 3, 2]]

            # A) compute the offset defining the movement to be applied in this 
            #    step at the vertex in question.
            pos = self.getClosestValid(pos)
            offset_rotated = shape.points[index] - pos
            shape.points[index] = pos

            # B) Find new location of affected points (lindex and rindex)
            #    1) w,h = rotate back vector from dragged vertex (=: i) to other
            #       vertex (=: o)
            #    2) cos(w or h), sin(w or h) -> vector from i to lindex (=:l) 
            #       or rindex (=: r) 
            vec_involved = shape.points[oindex] - shape.points[index]

            size = -rot(vec_involved, -shape.currentAngle)
            w, h = size.x(), size.y()

            vec_il = QPointF(cos(shape.currentAngle)*w, 
                    sin(shape.currentAngle)*w)
            vec_ir = QPointF(-sin(shape.currentAngle)*h, 
                    cos(shape.currentAngle)*h)

            # C) Correct locations accordingly
            #    1) compute  position 1, 3
            #    2) compute intersection in rotated space, such that it is 
            #       ensured that the resulting values are rounded inside the 
            #       coordinates. 
            #       Subtract the resulting value directly from i and 1 or 3
            #    3) Use the projection vector to move both the currently
            #       dragged point and the point that is out of bounds to the 
            #       last valid location.
            if index % 2 == 0: 
                rind = vec_ir
                vec_ir = vec_il
                vec_il = rind
            shape.points[rindex] = shape.points[index] - vec_ir
            shape.points[lindex] = shape.points[index] - vec_il

            # apply the rotation angle to the data that is uk
            shape_center = shape.getCenter(rotated=True)
            shifts = self.checkBorders(shape, index, lindex, vec_ir),  \
                    self.checkBorders(shape, index, rindex, vec_il)
            for shift in shifts: 
                if shift is not None:
                    shape.points[index] += shift

            # apply the new coordinates to the latent (unrotated) array
            shape.applyRotationAngle(shape.currentAngle, shape_center, False)

    def checkBorders(self, shape, index, aindex, direction):
        width, height = self.pixmap.width(), self.pixmap.height()
        a1, a2 = shape[aindex].y() < 0, shape[aindex].y() >= height

        if shape[aindex].y() < 0 or shape[aindex].y() >= height:
            
            lam = self.intersectionParametrized(shape[aindex], direction, 
                    QPointF(0, (shape[aindex].y()>=height)*height), 
                    QPointF(width, 0))
            if lam is not None:
                shift = lam * direction
                res = shape[aindex] + shift
                if round(res.x()) >= 0 and round(res.x()) < width:
                    shape[aindex] = res
                    return shift
            
        if shape[aindex].x() < 0 or shape[aindex].x() >= width:
            
            lam = self.intersectionParametrized(shape[aindex], direction, 
                    QPointF((shape[aindex].x()>=width)*width,0), 
                    QPointF(0, height))
            shift = lam * direction
            res = shape[aindex] + shift
            if round(res.y()) >= 0 and round(res.y()) < height:
                shape[aindex] = res
                return shift
        return None
            


    @staticmethod
    def intersectionParametrized(s_1, d_1, s_2, d_2):
        """
        Return the multiplier \lambda of d_1 such that \exists \mu s.th.
            s_1 + \lambda d_1 = s_2 + \mu d_2.
        Otherwise return None.

        :param s_1: first support vector
        :param d_1: first direction vector that is multiplied by \lambda. \lambda is to be returned
        :param s_2: second support
        :param d_2: second direction. Multiplier is irrelevant and not required.
        :return:    the multiplier \lambda of d_1 such that the two lines intersect
        """
        denominator = d_2.y() * d_1.x() - d_2.x() * d_1.y()
        return None if denominator == 0 else 1. * (d_2.x() * (s_1.y() - s_2.y()) 
                - d_2.y() * (s_1.x() - s_2.x())) / denominator

    
    @staticmethod
    def intersectionLineCircle(s, d, radius):
        signStar = lambda x : -1 if x < 0 else 1
        s2 = s + d
        dx = d.x()
        dy = d.y()
        dr = sqrt(dx**2. + dy**2.)
        D = s.x() * s2.y() - s2.x() * s.y()
        delta = radius**2. * dr**2. - D**2.
        
        if delta >= 0:
            p1 = QPointF((1.* D * dy + signStar(dy) * dx * sqrt(delta))/dr**2,
                    (-1.* D * dx     + abs(dy) * sqrt(delta))/dr**2)
            p2 = QPointF((1.* D * dy - signStar(dy) * dx * sqrt(delta))/dr**2,
                    (-1.* D * dx     - abs(dy) * sqrt(delta))/dr**2)
            if delta == 0: return p1 
            return p1, p2
        return None

        

    def boundedMoveShape(self, shape, pos):
        dp = pos - self.prevPoint
        self.prevPoint = pos
        return self.boundedMoveShapeBy(shape, dp)

    def boundedMoveShapeBy(self, shape, dp):
        minx, miny = shape.points[0].x(), shape.points[0].y()
        maxx, maxy = minx, miny
        for p in shape.points[1:]:
            minx = min(p.x(), minx)
            miny = min(p.y(), miny)
            maxx = max(p.x(), maxx)
            maxy = max(p.y(), maxy)
        
        maxx = self.pixmap.width() - maxx
        maxy = self.pixmap.height() - maxy
        dp = QPointF(max(min(maxx, dp.x()), -minx),
                max(min(maxy, dp.y()), -miny))

        if dp:
            shape.shift(dp)
            return True
        return False

    def deSelectShape(self):
        if self.selectedShape:
            self.selectedShape.selected = False
            self.selectedShape = None
            self.setHiding(False)
            self.selectionChanged.emit(False)
            self.update()

    def deleteSelected(self):
        if self.selectedShape:
            shape = self.selectedShape
            self.shapes.remove(self.selectedShape)
            self.selectedShape = None
            self.update()
            return shape

    def copySelectedShape(self):
        if self.selectedShape:
            shape = self.selectedShape.copy()
            self.deSelectShape()
            self.shapes.append(shape)
            shape.selected = True
            self.selectedShape = shape
            self.boundedShiftShape(shape)
            return shape

    def boundedShiftShape(self, shape):
        # Try to move in one direction, and if it fails in another.
        # Give up if both fail.
        point = shape[0]
        offset = QPointF(2.0, 2.0)
        self.prevPoint = point
        if not self.boundedMoveShape(shape, point - offset):
            self.boundedMoveShape(shape, point + offset)

    def paintEvent(self, event):
        if not self.pixmap:
            return super(Canvas, self).paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.scale(self.scale, self.scale)
        p.translate(self.offsetToCenter())

        p.drawPixmap(0, 0, self.pixmap)
        Shape.scale = self.scale
        for shape in self.shapes:
            if (shape.selected or not self._hideBackround) and self.isVisible(shape):
                shape.fill = shape.selected or shape == self.hShape
                shape.paint(p)
        if self.current:
            self.current.paint(p)
            self.line.paint(p)
        if self.selectedShapeCopy:
            self.selectedShapeCopy.paint(p)

        # Paint rect
        if self.current is not None and len(self.line) == 2:
            leftTop = self.line[0]
            rightBottom = self.line[1]
            rectWidth = rightBottom.x() - leftTop.x()
            rectHeight = rightBottom.y() - leftTop.y()
            p.setPen(self.drawingRectColor)
            brush = QBrush(Qt.BDiagPattern)
            p.setBrush(brush)
            p.drawRect(leftTop.x(), leftTop.y(), rectWidth, rectHeight)

        if self.drawing() and not self.prevPoint.isNull() and not self.outOfPixmap(self.prevPoint):
            p.setPen(QColor(0, 0, 0))
            p.drawLine(self.prevPoint.x(), 0, self.prevPoint.x(), self.pixmap.height())
            p.drawLine(0, self.prevPoint.y(), self.pixmap.width(), self.prevPoint.y())

        self.setAutoFillBackground(True)
        if self.verified:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(184, 239, 38, 128))
            self.setPalette(pal)
        else:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(232, 232, 232, 255))
            self.setPalette(pal)

        p.end()

    def transformPos(self, point):
        """Convert from widget-logical coordinates to painter-logical coordinates."""
        return point / self.scale - self.offsetToCenter()

    def offsetToCenter(self):
        s = self.scale
        area = super(Canvas, self).size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPointF(x, y)

    def outOfPixmap(self, p):
        w, h = self.pixmap.width(), self.pixmap.height()
        return not (0 <= p.x() < w and 0 <= p.y() < h)

    def finalise(self):
        assert self.current
        if self.current.points[0] == self.current.points[-1]:
            self.current = None
            self.drawingPolygon.emit(False)
            self.update()
            return

        self.current.close()
        self.shapes.append(self.current)
        self.current = None
        self.setHiding(False)
        self.newShape.emit()
        self.update()

    def closeEnough(self, p1, p2):
        #d = distance(p1 - p2)
        #m = (p1-p2).manhattanLength()
        # print "d %.2f, m %d, %.2f" % (d, m, d - m)
        return distance(p1 - p2) < self.epsilon

    def intersectionPoint(self, p1, p2):
        # Cycle through each image edge in clockwise fashion,
        # and find the one intersecting the current line segment.
        # http://paulbourke.net/geometry/lineline2d/
        size = self.pixmap.size()
        points = [(0, 0),
                  (size.width(), 0),
                  (size.width(), size.height()),
                  (0, size.height())]
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()

        d, i, (x, y) = min(self.intersectingEdges((x1, y1), (x2, y2), points))
        x3, y3 = points[i]
        x4, y4 = points[(i + 1) % 4]
        if (x, y) == (x1, y1):
            # Handle cases where previous point is on one of the edges.
            if x3 == x4:
                return QPointF(x3, min(max(0, y2), max(y3, y4)))
            else:  # y3 == y4
                return QPointF(min(max(0, x2), max(x3, x4)), y3)
        return QPointF(x, y)

    def intersectingEdges(self, x1y1, x2y2, points):
        """For each edge formed by `points', yield the intersection
        with the line segment `(x1,y1) - (x2,y2)`, if it exists.
        Also return the distance of `(x2,y2)' to the middle of the
        edge along with its index, so that the one closest can be chosen."""
        x1, y1 = x1y1
        x2, y2 = x2y2
        for i in range(len(points)):
            x3, y3 = points[i]
            x4, y4 = points[(i + 1) % 4]
            denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            nua = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
            nub = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
            if denom == 0:
                # This covers two cases:
                #   nua == nub == 0: Coincident
                #   otherwise: Parallel
                continue
            ua, ub = nua / denom, nub / denom
            if 0 <= ua <= 1 and 0 <= ub <= 1:
                x = x1 + ua * (x2 - x1)
                y = y1 + ua * (y2 - y1)
                m = QPointF((x3 + x4) / 2, (y3 + y4) / 2)
                d = distance(m - QPointF(x2, y2))
                yield d, i, (x, y)

    # These two, along with a call to adjustSize are required for the
    # scroll area.
    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        if self.pixmap:
            return self.scale * self.pixmap.size()
        return super(Canvas, self).minimumSizeHint()

    def wheelEvent(self, ev):
        qt_version = 4 if hasattr(ev, "delta") else 5
        if qt_version == 4:
            if ev.orientation() == Qt.Vertical:
                v_delta = ev.delta()
                h_delta = 0
            else:
                h_delta = ev.delta()
                v_delta = 0
        else:
            delta = ev.angleDelta()
            h_delta = delta.x()
            v_delta = delta.y()

        mods = ev.modifiers()
        if Qt.ControlModifier == int(mods) and v_delta:
            self.zoomRequest.emit(v_delta)
        else:
            v_delta and self.scrollRequest.emit(v_delta, Qt.Vertical)
            h_delta and self.scrollRequest.emit(h_delta, Qt.Horizontal)
        ev.accept()

    def keyPressEvent(self, ev):
        key = ev.key()
        if key == Qt.Key_Escape and self.current:
            print('ESC press')
            self.current = None
            self.drawingPolygon.emit(False)
            self.update()
        elif key == Qt.Key_Return and self.canCloseShape():
            self.finalise()
        elif key == Qt.Key_Left and self.selectedShape:
            self.moveOnePixel(QPointF(-1,0))
        elif key == Qt.Key_Right and self.selectedShape:
            self.moveOnePixel(QPointF(1,0))
        elif key == Qt.Key_Up and self.selectedShape:
            self.moveOnePixel(QPointF(0,-1))
        elif key == Qt.Key_Down and self.selectedShape:
            self.moveOnePixel(QPointF(0,1))

    def moveOnePixel(self, direction):
        self.boundedMoveShapeBy(self.selectedShape, direction)
        self.shapeMoved.emit()
        self.repaint()

    def setLastLabel(self, text, line_color  = None, fill_color = None):
        assert text
        self.shapes[-1].label = text
        if line_color:
            self.shapes[-1].line_color = line_color
        
        if fill_color:
            self.shapes[-1].fill_color = fill_color

        return self.shapes[-1]

    def undoLastLine(self):
        assert self.shapes
        self.current = self.shapes.pop()
        self.current.setOpen()
        self.line.points = [self.current[-1], self.current[0]]
        self.drawingPolygon.emit(True)

    def resetAllLines(self):
        assert self.shapes
        self.current = self.shapes.pop()
        self.current.setOpen()
        self.line.points = [self.current[-1], self.current[0]]
        self.drawingPolygon.emit(True)
        self.current = None
        self.drawingPolygon.emit(False)
        self.update()

    def loadPixmap(self, pixmap):
        self.pixmap = pixmap
        self.shapes = []
        self.repaint()

    def loadShapes(self, shapes):
        self.shapes = list(shapes)
        self.current = None
        self.repaint()

    def setShapeVisible(self, shape, value):
        self.visible[shape] = value
        self.repaint()

    def currentCursor(self):
        cursor = QApplication.overrideCursor()
        if cursor is not None:
            cursor = cursor.shape()
        return cursor

    def overrideCursor(self, cursor):
        self._cursor = cursor
        if self.currentCursor() is None:
            QApplication.setOverrideCursor(cursor)
        else:
            QApplication.changeOverrideCursor(cursor)

    def restoreCursor(self):
        QApplication.restoreOverrideCursor()

    def resetState(self):
        self.restoreCursor()
        self.pixmap = None
        self.update()
