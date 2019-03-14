import math

import cv2
import numpy as np

from model.geometry.Box import Box


class Cluster(object):
    def __init__(self):
        self.points = []

        self.csize = 0
        self.cluster_density = None

        self.color = [int(c) for c in list(np.random.choice(range(256), size=3))]

        self.border = 1
        self.modifier = 3

    def add(self, point):
        self.points.append(point)
        self.csize += 1

    def cluster_size(self):
        return self.csize

    def min(self, lst):
        return int(round(min(lst) - (self.border / 2), 0))

    def max(self, lst):
        return int(round(max(lst) - (self.border / 2), 0))

    def get_corners(self):
        points = [p.xy for p in self.points]
        x = [x[0] for x, _ in points]
        y = [y[0] for _, y in points]

        return self.min(x), self.min(y), self.max(x), self.max(y)

    def render(self, image, color=None):
        for p in self.points:
            p.render(image, color)

        x1, y1, x2, y2 = self.get_corners()

        cv2.rectangle(image, (x1, y1), (x2, y2), self.color if color is None else color, self.border)

    def density(self):
        if self.cluster_density is None:
            x1, y1, x2, y2 = self.get_corners()

            area = Box(x1, y1, x2, y2).area

            if area > 0 and math.log(area) > 0:
                # self.cluster_density = self.csize * self.modifier / cluster_container.area
                self.cluster_density = math.log(self.csize) * self.modifier / math.log(area)
            else:
                self.cluster_density = 0

        return self.cluster_density
