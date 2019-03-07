import numpy as np


class Cluster(object):
    def __init__(self):
        self.points = []
        self.color = list(np.random.choice(range(256), size=3))

    def add(self, point):
        self.points.append(point)

    def conquer(self, cluser):
        for point in cluser:
            point.set_cluster(self)
