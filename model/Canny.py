import logging
from time import time

import cv2
import numpy as np
from shapely.geometry import GeometryCollection, LineString
from sklearn.cluster import DBSCAN

from model.containers.Clusters import Clusters
from model.dampening.SFiltering import SFiltering
from model.exceptions import IsNan, InvalidLine, TooManyLines, TooManyPoints
from model.geometry.Line import Line
from model.geometry.Point import Point
from model.logging import log


class Canny(object):
    def __init__(self, x, y):
        self.canny_threshold = 50

        self.theta = 150
        self.theta_modifier = 5

        self._latest_clusters = None
        self.last_frame_count = None
        self.last_time_count = time()

        self.edges = None
        self.lines = []

        self.line_max = 100

        self.filtering = SFiltering(x, y, history_size=6)
        self.newest_center = None

    def calculate_theta(self, lines):
        if self.last_frame_count is not None:
            modifier = (self.last_frame_count / lines) * 2

            if modifier <= 0:
                modifier = 1
        else:
            modifier = 1

        timestamp = time()

        # Our DEADLINE is 10 fps, so if a tick took more then 0.1 sec, increase l_theta
        if timestamp - self.last_time_count > 1 / 10:
            log(f'Too slow, increasing l_theta to {self.theta}', logging.INFO)
            self.theta += int(self.theta_modifier * 0.5)
        elif lines < 10 and self.theta > int(round(self.theta_modifier * modifier, 0)):
            self.theta -= int(round(self.theta_modifier * modifier, 0))
            log(f'Not enough data, decreasing l_theta to {self.theta}', logging.INFO)
        elif lines > 50:
            log(f'Too much data, increasing l_theta to {self.theta}', logging.INFO)
            self.theta += int(round(self.theta_modifier * modifier, 0))

        self.last_frame_count = lines
        self.last_time_count = timestamp

        if self.line_max < lines:
            raise TooManyLines()

    def process_frame(self, frame):
        self.lines.clear()
        self.edges = cv2.Canny(frame, self.canny_threshold, self.canny_threshold * 3, apertureSize=3)

        lines = cv2.HoughLines(self.edges, 2, np.pi / 180, self.theta)
        if lines is not None:
            try:
                self.calculate_theta(len(lines))

                for line_data in lines:
                    try:
                        line = Line(*line_data.T)
                        self.lines.append(line)

                    except (IsNan, InvalidLine):
                        pass
            except (TooManyLines, TooManyPoints):
                pass

        self.clustering()

    def clustering(self):
        gc = GeometryCollection(self.lines)

        try:
            intersections = gc.intersection(gc)
            if isinstance(intersections, LineString):
                points = [Point(*intersections.xy)]
            else:
                points = [Point(*point.xy) for point in intersections]

            if points:
                points_ = [(p.x_point, p.y_point) for p in points]
                min_samples = int(round(len(points_) * 0.05, 0))

                clustering = DBSCAN(eps=20, min_samples=min_samples).fit(points_)

                clusters = Clusters()

                for idx, kl in enumerate(clustering.labels_):
                    # All points marked with -1 is noise
                    if kl == -1:
                        continue
                    points[idx].set_cluster(clusters.get_cluster(kl))

                if clusters:
                    self._latest_clusters = clusters.as_list()

                    self.newest_center = clusters.best_cluster_as_point()
                    self.filtering.add(self.newest_center)
            else:
                self.newest_center = None
            return
        except TypeError as e:
            log(str(e), logging.ERROR)
            return

    def get_latest_clusters(self):
        return self._latest_clusters

    def get_center(self):
        return self.filtering.get_point()

    def get_newest_center(self):
        return self.newest_center
