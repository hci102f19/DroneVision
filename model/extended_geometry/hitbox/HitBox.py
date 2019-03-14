from model.flight.Vector import Vector
from model.geometry.Box import Box
from model.geometry.Point import Point


class HitBox(Box):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1, y1, x2, y2, **kwargs)
        self.force = kwargs.get('force', 100)

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
            vector.set_roll(self.force)
