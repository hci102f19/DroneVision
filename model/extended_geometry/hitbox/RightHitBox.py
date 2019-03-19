import cv2
from shapely.geometry import Polygon

from model.flight.Vector import Vector
from model.geometry.Point import Point


class RightHitBox(Polygon):
    def __init__(self, width, height, **kwargs):
        width_top = width - ((width / 2) * kwargs.get('width_top', 0.97))
        width_bottom = width - ((width / 2) * kwargs.get('width_bottom', 0.6))
        height_top = height * (1 - kwargs.get('height_top', 0.6))

        init_geom = [(width, height), (width, height_top), (width_top, height_top), (width_bottom, height)]

        self.force = kwargs.get('force', 100)
        self.color = kwargs.get('color', (0, 255, 0))

        super().__init__(init_geom)

    @staticmethod
    def round(val):
        return int(round(val, 0))

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
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
