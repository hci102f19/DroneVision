import cv2
from shapely.affinity import rotate
from shapely.geometry import Polygon
from shapely.geometry.polygon import geos_polygon_from_py

from model.flight.Vector import Vector
from model.geometry.Point import Point


class Box(Polygon):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        self.color = kwargs.get('color', (0, 255, 0))

        init_geom = [(x2, y1), (x2, y2), (x1, y2), (x1, y1), (x2, y1)]

        super().__init__(init_geom)

    def rotate(self, degrees):
        shell = rotate(self.boundary, degrees)

        ret = geos_polygon_from_py(shell, None)
        if ret is not None:
            self._geom, self._ndim = ret
        else:
            self.empty()

    @staticmethod
    def round(val):
        return int(round(val, 0))

    def render(self, image, color=None):
        cv2.circle(image, (int(self.center[0]), int(self.center[1])), 5, self.color, -1)

        x_coordinates, y_coordinates = self.boundary.coords.xy
        coordinates = [(self.round(x), self.round(y)) for x, y in zip(x_coordinates, y_coordinates)]

        for idx in range(len(coordinates) - 1):
            start = coordinates[idx]
            end = coordinates[idx + 1]
            cv2.line(image, start, end, self.color if color is None else color, 3)

    def hit(self, point: Point, vector: Vector):
        raise NotImplemented()

    @property
    def x_coordinates(self):
        x_coordinates, _ = self.boundary.coords.xy
        return x_coordinates

    @property
    def xmin(self):
        return min(self.x_coordinates)

    @property
    def xmax(self):
        return max(self.x_coordinates)

    @property
    def y_coordinates(self):
        _, y_coordinates = self.boundary.coords.xy
        return y_coordinates

    @property
    def ymin(self):
        return min(self.y_coordinates)

    @property
    def ymax(self):
        return max(self.y_coordinates)

    @property
    def center(self):
        x, y = self.centroid.coords.xy
        return round(x[0], 2), round(y[0], 2)

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin
