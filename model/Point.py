import cv2
from shapely.geometry import Point as BasePoint

from model.Cluster import Cluster


class Point(BasePoint):
    def __init__(self, x, y):
        super().__init__([x[0], y[0]])

        self.threshold = 3

        self.cluster = None

    def set_cluster(self, cluster):
        self.cluster = cluster
        self.cluster.add(self)

    def validate_neighborhood(self, points):
        neighborhood = []

        for point in points:
            if point is self:
                continue

            if self.distance(point) < self.threshold:
                neighborhood.append(point)

        if len(neighborhood) > 0:
            neighborhoods = list(set([point.cluster for point in neighborhood if point.cluster is not None]))

            if neighborhoods:
                cluster = neighborhoods[0]
                for cluster_ in neighborhoods[1:]:
                    cluster.conquer(cluster_.points)
            else:
                cluster = Cluster()

            self.set_cluster(cluster)

    def render(self, image):
        cv2.circle(image, (int(self.x), int(self.y)), 1, (0, 0, 0), -1)
        cv2.circle(image, (int(self.x), int(self.y)), self.threshold, (255, 255, 255), 1)

        return
        if self.cluster is not None:
            if len(self.cluster.points) > 0:
                r, g, b = self.cluster.color
                cv2.circle(image, (int(self.x), int(self.y)), 3, (int(b), int(g), int(r)), -1)
