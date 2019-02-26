from model.Point import Point


class Points(object):
    def __init__(self):
        self.points = []

    def add(self, point: Point):
        self.points.append(point)
