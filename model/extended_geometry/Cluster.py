import cv2
import numpy as np

from model.geometry.Box import Box


class Cluster(object):
    def __init__(self):
        self.points = []

        self.csize = 0
        self.cdensity = None

        self._color = list(np.random.choice(range(256), size=3))

        self.border = 2

    def add(self, point):
        self.points.append(point)
        self.csize += 1

    @property
    def color(self):
        return [int(c) for c in self._color]

    def cluster_size(self):
        return self.csize

    def cluster_density(self):
        return

    def min(self, lst):
        return int(round(min(lst) - (self.border / 2), 0))

    def max(self, lst):
        return int(round(max(lst) - (self.border / 2), 0))

    def render(self, image):
        points = [p.xy for p in self.points]
        x = [x[0] for x, _ in points]
        y = [y[0] for _, y in points]

        x1, x2 = self.min(x), self.max(x)
        y1, y2 = self.min(y), self.max(y)

        for p in self.points:
            p.render(image)

        cv2.rectangle(image, (x1, y1), (x2, y2), self.color, self.border)

    def density(self):
        if self.cdensity is None:
            points = [p.xy for p in self.points]
            x = [x[0] for x, _ in points]
            y = [y[0] for _, y in points]

            x1, x2 = self.min(x), self.max(x)
            y1, y2 = self.min(y), self.max(y)
            bz = Box(x1, y1, x2, y2)
            if bz.area > 0:
                self.cdensity = self.csize * 2 / bz.area
            else:
                self.cdensity = 0

        return self.cdensity
