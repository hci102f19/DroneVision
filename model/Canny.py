import cv2
import numpy as np

from model.Cluster import Cluster
from model.Line import Line
from model.Lines import Lines
from model.Point import Point
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
        self.lines = Lines()

        self.cluster_points = Cluster()

    def process_frame(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        v = np.median(self.image)

        lower = int(max(0, (1.0 - self.sigma) * v))
        upper = int(min(255, (1.0 + self.sigma) * v))

        # print(lower, upper)
        # exit(1)

        # edges = cv2.Canny(gray, 75, 170, apertureSize=3)
        edges = cv2.Canny(gray, 50, 100, apertureSize=3)

        for line_data in cv2.HoughLines(edges, 1, np.pi / 180, 100, self.min_line_length, self.max_line_gap):
            try:
                line = Line(*line_data.T)

                if 1 - self.line_deviation < line.x_deviation or 1 - self.line_deviation < line.y_deviation:
                    continue
            except Exception:
                continue

            for line_ in self.lines.get():
                intersection_point = line.intersection_point(line_)
                if intersection_point is not None:
                    self.points.add(intersection_point)

            self.lines.add(line)

        self.calculate_cluster()

    def calculate_cluster(self):
        for point in self.points.get():
            point.count_neighbours(self.points.get())

        nodes = sorted(self.points.get(), key=lambda x: x.count_neighbour, reverse=True)
        if len(nodes) > 0:
            max_node = nodes[0]

            for point in list(set(max_node.export())):
                self.cluster_points.add(point)

    def get_center(self):
        x, y = self.cluster_points.center

        if x is None or y is None:
            return None

        return Point(x, y)

    def render(self, image):
        # self.points.render(image)
        # self.lines.render(image)
        self.cluster_points.render(image)
