from model.Point import Point


class Points(object):
    def __init__(self):
        self.points = []

    def add(self, point: Point):
        self.points.append(point)

    def render(self, image):
        for point in self.points:
            point.render(image)
