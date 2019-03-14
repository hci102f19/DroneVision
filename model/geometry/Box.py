import cv2
from shapely.geometry import Polygon


class Box(Polygon):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

        self.color = kwargs.get('color', (0, 255, 0))

        init_geom = [(x2, y1), (x2, y2), (x1, y2), (x1, y1), (x2, y1)]

        super().__init__(init_geom)

    def render(self, image, color=None):
        cv2.rectangle(image, (self.x1, self.y1), (self.x2, self.y2), self.color if color is None else color, 3)
