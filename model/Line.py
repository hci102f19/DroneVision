import cv2
import numpy as np
from numpy.linalg import LinAlgError

from model.Point import Point


class Line(object):
    def __init__(self, rho, theta):
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        self.x1 = int(x0 + 1000 * (-b))
        self.y1 = int(y0 + 1000 * a)

        self.x2 = int(x0 - 1000 * (-b))
        self.y2 = int(y0 - 1000 * a)

    @staticmethod
    def abs_list(lst):
        # TODO: Might not work as intented
        return [abs(e) for e in lst]

    @property
    def x_deviation(self):
        return min(self.abs_list([self.x1, self.x2])) / max(self.abs_list([self.x1, self.x2]))

    @property
    def y_deviation(self):
        return min(self.abs_list([self.y1, self.y2])) / max(self.abs_list([self.y1, self.y2]))

    @property
    def start_point(self):
        return np.array([self.x1, self.y1])

    @property
    def end_point(self):
        return np.array([self.x2, self.y2])

    def intersection_point(self, line):
        try:
            t, s = np.linalg.solve(
                np.array([self.end_point - self.start_point, line.start_point - line.end_point]).T,
                line.start_point - self.start_point
            )

            return Point(*((1 - t) * self.start_point + t * self.end_point).T)
        except LinAlgError:
            return None

    def render(self, image):
        cv2.line(image, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)
        return
