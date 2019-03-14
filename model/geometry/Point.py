import cv2
from shapely.geometry import Point as BasePoint


class Point(BasePoint):
    def __init__(self, x, y):
        super().__init__([x[0], y[0]])
        self.x_point = float(x[0])
        self.y_point = float(y[0])

        self.threshold = 5

        self.valid = True
        self.checked = False
        self.cluster = None

    @staticmethod
    def points2point(x, y):
        return Point([x], [y])

    def is_checked(self):
        return self.checked

    def set_cluster(self, cluster):
        self.checked = True
        self.cluster = cluster
        self.cluster.add(self)

    def render(self, image):
        if self.valid:
            if self.cluster is not None:
                cv2.circle(image, (int(self.x), int(self.y)), 1, self.cluster.color, -1)
            else:
                cv2.circle(image, (int(self.x), int(self.y)), 5, (255, 255, 255), -1)
                cv2.circle(image, (int(self.x), int(self.y)), 3, (0, 0, 0), -1)
