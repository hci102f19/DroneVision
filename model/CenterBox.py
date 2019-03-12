from scipy.interpolate import interp1d

from model.Box import Box
from model.Point import Point


class CenterBox(object):
    def __init__(self, width, height, w_center, h_center, h_offset):
        self.width = width
        self.height = height

        self.w_center = w_center
        self.h_center = h_center
        self.h_offset = h_offset

        self.x1 = width * ((1 - w_center) / 2)
        self.y1 = height * (((1 - h_center) / 2) - h_offset)
        self.x2 = width * (1 - ((1 - w_center) / 2))
        self.y2 = height * ((1 - ((1 - h_center) / 2)) - h_offset)

        self.box = Box(self.x1, self.y1, self.x2, self.y2)

        self.center = Point.points2point(
            self.x1 + ((self.x2 - self.x1) / 2),
            self.y1 + ((self.y2 - self.y1) / 2)
        )

    def intersects(self, other):
        return self.box.intersects(other)

    def render(self, image, point=None):
        self.box.render(image, point)

    def flight(self, point):
        p_x, p_y = point.x_point, point.y_point
        c_x, c_y = self.center.x_point, self.center.y_point

        x_calc = interp1d([-self.center.x_point, self.center.x_point], [-100, 100])
        y_calc = interp1d([-self.center.y_point, self.center.y_point], [-100, 100])

        x_force = p_x - c_x
        y_force = p_y - c_y

        try:
            x_val = x_calc(x_force) - x_force if abs(x_force) > self.center.x_point * self.w_center else 0
            y_val = y_calc(y_force) - y_force if abs(y_force) > self.center.y_point * self.h_center else 0

            return round(x_val, 2), round(y_val, 2)
        except ValueError:
            print("FAK!")
            return 0, 0
