from math import atan2

import cv2
import numpy as np
from shapely.geometry import LineString

from model.exceptions import IsNan, InvalidLine


class Line(LineString):
    def __init__(self, rho, theta):
        if np.isnan(rho):
            raise IsNan("Rho is NAN!")

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        self.x1 = int(x0 + 1000 * (-b))
        self.y1 = int(y0 + 1000 * a)

        self.x2 = int(x0 - 1000 * (-b))
        self.y2 = int(y0 - 1000 * a)

        self.angle_threshold = 20

        super().__init__([[self.x1, self.y1], [self.x2, self.y2]])

        self.__validate()

    def __validate(self):
        c_angle = round(abs(np.degrees(atan2((self.y2 - self.y1), (self.x2 - self.x1)))), 0)

        if 180 - self.angle_threshold <= c_angle or c_angle <= 0 + self.angle_threshold:
            raise InvalidLine('Line not within angle scope')
        if 90 - self.angle_threshold <= c_angle <= 90 + self.angle_threshold:
            raise InvalidLine('Line not within angle scope')

    def render(self, image):
        cv2.line(image, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)
