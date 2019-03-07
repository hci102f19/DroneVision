import cv2
import numpy as np
from shapely.geometry import GeometryCollection, LineString

from model.Line import Line
from model.Point import Point
from model.exceptions import IsNan, InvalidLine


class Canny(object):
    def __init__(self):
        self.canny_threshold = 50

        self.theta = 150
        self.theta_modifier = 5

        self.last_frame_count = None

        self.line_max = 100

    def calculate_theta(self, lines):
        if self.last_frame_count is not None:
            modifier = (self.last_frame_count / lines) * 2

            if modifier <= 0:
                modifier = 1
        else:
            modifier = 1

        self.last_frame_count = lines

        if lines < 10 and self.theta > self.theta_modifier:
            self.theta -= int(round(self.theta_modifier * modifier, 0))
            # print(f'Not enough data, decreasing l_theta to {self.theta}')
        elif lines > 50:
            self.theta += int(round(self.theta_modifier * modifier, 0))
            # print(f'Too much data, increasing l_theta to {self.theta}')

        return self.line_max < lines

    def process_frame(self, frame):
        lines_ = []
        edges = cv2.Canny(frame, self.canny_threshold, self.canny_threshold * 3, apertureSize=3)

        lines = cv2.HoughLines(edges, 2, np.pi / 180, self.theta)
        if lines is not None:
            if self.calculate_theta(len(lines)):
                # print(f"WAY TOO MANY LINES: {len(lines)}")
                return []

            for line_data in lines:
                try:
                    line = Line(*line_data.T)
                    lines_.append(line)

                except (IsNan, InvalidLine):
                    pass

        return self.clustering(lines_)

    @staticmethod
    def clustering(lines):
        gc = GeometryCollection(lines)
        clusters = []
        try:
            intersections = gc.intersection(gc)
            if isinstance(intersections, LineString):
                points = [Point(*intersections.xy)]
            else:
                points = [Point(*point.xy) for point in intersections]

            for point in points:
                if not point.is_checked():
                    cluster = point.validate_neighborhood(points)
                    if cluster is not None:
                        clusters.append(cluster)

            if len(clusters) > 0:
                c = [c for c in clusters if not c.is_dead()]
                c = sorted(c, key=lambda c_: c_.cluster_size(), reverse=True)
                cgc = GeometryCollection(c[0].points)
                return [Point(*cgc.centroid.xy)]
            return []
        except TypeError as e:
            print(str(e))
            return []
