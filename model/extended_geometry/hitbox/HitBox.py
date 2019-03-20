import cv2
from shapely.geometry import Polygon

from model.flight.Vector import Vector
from model.geometry.Point import Point


class HitBox(Polygon):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get('geom'))
        self.force = kwargs.get('force', 100)
        self.color = kwargs.get('color', (0, 255, 0))

    @staticmethod
    def round(val):
        return int(round(val, 0))

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
            print(self.force)
            vector.set_roll(self.force)
            return True
        return False

    @property
    def center(self):
        x, y = self.centroid.coords.xy
        return round(x[0], 2), round(y[0], 2)

    def render(self, image, color=None):
        # Center
        cv2.circle(image, (int(self.center[0]), int(self.center[1])), 5, self.color, -1)

        x_coordinates, y_coordinates = self.boundary.coords.xy
        coordinates = [(self.round(x), self.round(y)) for x, y in zip(x_coordinates, y_coordinates)]

        # Make a line between each of the nodes
        for idx in range(len(coordinates) - 1):
            start = coordinates[idx]
            end = coordinates[idx + 1]
            cv2.line(image, start, end, (0, 0, 0), 3)
