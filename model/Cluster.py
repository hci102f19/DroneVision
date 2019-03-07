import numpy as np


class Cluster(object):
    def __init__(self):
        self.points = []
        self.csize = 0
        self.color = list(np.random.choice(range(256), size=3))

        self.dead = False

    def add(self, point):
        self.points.append(point)
        self.csize += 1

    def cluster_size(self):
        return self.csize

    def is_dead(self):
        return self.dead

    def conquer(self, cluser):
        for point in cluser:
            point.set_cluster(self)
        self.dead = True
