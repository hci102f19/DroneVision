from model.exceptions import Quit
from model.geometry.Box import Box
from model.geometry.Point import Point


class ReverseHitBox(Box):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1, y1, x2, y2, **kwargs)

        # self.y_calc_pos = interp1d([0, self.height - self.center.y_point], [0, 100])
        # self.y_calc_neg = interp1d([-self.center.y_point, 0], [-100, 0])

    def hit(self, point: Point):
        if self.intersects(point):
            return False

        x, y = point.x_point, point.y_point

        print(self.min_x < x < self.max_x)
        print(self.min_y < y < self.max_y)

        print("Woops")
        raise Quit()
