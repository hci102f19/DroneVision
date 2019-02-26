import cv2
import numpy as np

from model.Line import Line
from model.Points import Points


class Canny(object):
    def __init__(self, image):
        self.image = image

        self.height, self.width, _ = image.shape

        self.sigma = 0.33

        self.min_line_length = 5
        self.max_line_gap = 10

        self.line_deviation = 0.15

        self.points = Points()

    def process_frame(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        v = np.median(self.image)

        lower = int(max(0, (1.0 - self.sigma) * v))
        upper = int(min(255, (1.0 + self.sigma) * v))

        edges = cv2.Canny(gray, lower, upper, apertureSize=3)

        lines = []

        for line_data in cv2.HoughLines(edges, 1, np.pi / 180, 100, self.min_line_length, self.max_line_gap):
            line = Line(*line_data.T)

            if 1 - self.line_deviation < line.x_deviation or 1 - self.line_deviation < line.y_deviation:
                continue

            for line_ in lines:
                intersection_point = line.intersection_point(line_)
                if intersection_point is not None:
                    self.points.add(intersection_point)

            lines.append(line)
