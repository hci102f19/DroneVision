from numpy import mean

from model.Point import Point


class CoordinateDampner(object):
    def __init__(self, limit=10):
        self.history = []
        self.limit = limit

        self.latest = None

    def enqueue(self, point):
        self.history = self.history[-self.limit:] + [point]

        self.latest = point

    def point(self):
        if len(self.history) <= self.limit:
            return self.latest

        hst = self.history[-(self.limit + 1):]
        hst.pop()

        k = [True in self.latest.max_deviation(p) for p in hst]

        if k == [True for _ in range(self.limit)]:
            x = mean([point.x for point in hst])
            y = mean([point.y for point in hst])
            return Point(x, y)

        return self.latest
