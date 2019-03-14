import cv2
from shapely.geometry import Polygon

from model.flight.Vector import Vector
from model.geometry.Point import Point


class Box(Polygon):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

        self.min_x = min([x1, x2])
        self.min_y = min([y1, y2])
        self.max_x = max([x1, x2])
        self.max_y = max([y1, y2])

        self.width = abs(x2 - x1)
        self.height = abs(y2 - y1)

        self.center = (min([x1, x2]) + self.width / 2, min([y1, y2]) + self.height / 2)

        self.color = kwargs.get('color', (0, 255, 0))

        init_geom = [(x2, y1), (x2, y2), (x1, y2), (x1, y1), (x2, y1)]

        super().__init__(init_geom)

    def render(self, image, color=None):
        cv2.circle(image, (int(self.center[0]), int(self.center[1])), 5, self.color, -1)
        cv2.rectangle(image, (self.x1, self.y1), (self.x2, self.y2), self.color if color is None else color, 3)

    def hit(self, point: Point, vector: Vector):
        raise NotImplemented()
