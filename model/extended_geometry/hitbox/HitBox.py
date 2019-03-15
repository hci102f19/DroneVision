from shapely.affinity import rotate
from shapely.geometry.polygon import geos_polygon_from_py

from model.flight.Vector import Vector
from model.geometry.Box import Box
from model.geometry.Point import Point


class HitBox(Box):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1, y1, x2, y2, **kwargs)
        self.force = kwargs.get('force', 100)
        self.rotation = kwargs.get('rotation', 0)

        shell = rotate(self.boundary, self.rotation)
        self._geom, self._ndim = geos_polygon_from_py(shell, None)

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
            vector.set_roll(self.force)
