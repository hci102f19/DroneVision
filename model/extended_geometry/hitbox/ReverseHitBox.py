from model.flight.Vector import Vector
from model.geometry.Box import Box
from model.geometry.Point import Point


class ReverseHitBox(Box):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1, y1, x2, y2, **kwargs)

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
            return False

        if not self.xmin <= point.x_point <= self.xmax:
            vector.set_yaw(self.calculate_horizontal(point.x_point))

        """
        TODO: We dont do vertical movements
        if not self.ymin <= point.y_point <= self.ymax:
            vector.set_vertical_movement(self.calculate_vertical(point.y_point))
        """

        return True

    def rotate(self, degrees):
        # This element should not be rotateable
        return

    def calculate_horizontal(self, x):
        center_x, _ = self.center
        return self.clamp(((x - center_x) / center_x) * 100, -100, 100)

    def calculate_vertical(self, y):
        _, center_y = self.center
        return self.clamp(((y - center_y) / center_y) * 100, -100, 100)

    @staticmethod
    def clamp(val, min_val, max_val):
        if val < min_val:
            return min_val
        if val > max_val:
            return max_val
        return val
