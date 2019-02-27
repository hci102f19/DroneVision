import math

import cv2
from numpy import mean


class Cluster(object):
    def __init__(self):
        self.points = []

    def add(self, point):
        self.points.append(point)

    @property
    def center(self):
        if len(self.points) == 0:
            return None, None

        x = mean([point.x for point in self.points])
        y = mean([point.y for point in self.points])

        if math.isnan(x) or math.isnan(y):
            return None, None

        return int(round(x, 0)), int(round(y, 0))

    def render(self, image):
        for point in self.points:
            point.render(image)

        if len(self.points) > 0:
            cv2.circle(image, self.center, 3, (255, 255, 0), -1)
