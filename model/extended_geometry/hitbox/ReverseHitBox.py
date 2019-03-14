from model.flight.Vector import Vector
from model.geometry.Box import Box
from model.geometry.Point import Point


class ReverseHitBox(Box):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1, y1, x2, y2, **kwargs)

        # self.y_calc_pos = interp1d([0, self.height - self.center.y_point], [0, 100])
        # self.y_calc_neg = interp1d([-self.center.y_point, 0], [-100, 0])

    def hit(self, point: Point, vector: Vector):
        if self.intersects(point):
            return False

        if not self.min_x <= point.x_point <= self.max_x:
            vector.set_yaw(self.calculate_horizontal(point.x_point))

        if not self.min_y <= point.y_point <= self.max_y:
            vector.set_vertical_movement(self.calculate_vertical(point.y_point))

        return vector

    def calculate_horizontal(self, x):
        center_x, _ = self.center
        return self.clamp(((x - center_x) / center_x) * 100, -100, 100) * -1

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
