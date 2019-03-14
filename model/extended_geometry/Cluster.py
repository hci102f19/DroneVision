import cv2
import numpy as np

from model.geometry.Box import Box


class Cluster(object):
    def __init__(self):
        self.points = []

        self.csize = 0
        self.cluster_density = None

        self._color = [int(c) for c in list(np.random.choice(range(256), size=3))]

        self.border = 2
        self.modifier = 2

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

    def render(self, image):
        for p in self.points:
            p.render(image)

        x1, y1, x2, y2 = self.get_corners()

        cv2.rectangle(image, (x1, y1), (x2, y2), self._color, self.border)

    def density(self):
        if self.cluster_density is None:
            x1, y1, x2, y2 = self.get_corners()

            cluster_container = Box(x1, y1, x2, y2)

            if cluster_container.area > 0:
                self.cluster_density = self.csize * self.modifier / cluster_container.area
            else:
                self.cluster_density = 0

        return self.cluster_density
