import cv2
from shapely.geometry import Polygon


class Box(Polygon):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        init_geom = [(x2, y1), (x2, y2), (x1, y2), (x1, y1), (x2, y1)]

        super().__init__(init_geom)

    def render(self, image):
        cv2.rectangle(image, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 0), 3)
