from model.geometry.Box import Box
from model.geometry.Point import Point


class HitBox(Box):
    def hit(self, point: Point):
        return self.intersects(point)
