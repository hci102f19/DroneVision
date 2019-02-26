import math

import cv2


class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

        self._coord_x = int(round(self._x, 0))
        self._coord_y = int(round(self._y, 0))

        self.threshold = 15
        self.neighbours = []
        self.c_neighbours = 0

        self.exported = False

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        self.c_neighbours += 1

    @property
    def count_neighbour(self):
        return self.c_neighbours

    @property
    def x(self):
        return self._coord_x

    @property
    def y(self):
        return self._coord_y

    def render(self, image):
        cv2.circle(image, (self.x, self.y), 3, (255, 0, 0), -1)

    @staticmethod
    def near(point1, point2):
        if point1 > point2:
            return point1 - point2
        return point2 - point1

    def count_neighbours(self, points):
        for point in points:
            if self.near(point.x, self.x) <= self.threshold and self.near(point.y, self.y) <= self.threshold:
                if self.threshold >= math.hypot(point.x - self.x, point.y - self.y):
                    self.add_neighbour(point)

    def export(self):
        # TODO: Rewrite, more readable
        self.exported = True

        t = [self]

        for n in self.neighbours:
            if not n.exported:
                t.extend(n.export())

        return t
