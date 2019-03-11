import cv2
from shapely.geometry import Point as BasePoint


class Point(BasePoint):
    def __init__(self, x, y):
        super().__init__([x[0], y[0]])
        self.x_point = float(x[0])
        self.y_point = float(y[0])

        self.threshold = 5

        self.valid = True
        self.checked = False
        self.cluster = None

    def is_checked(self):
        return self.checked

    def set_cluster(self, cluster):
        self.checked = True
        self.cluster = cluster
        self.cluster.add(self)
    #
    # def point_validator(self, point):
    #     return (
    #             abs(self.x_point - point.x_point) < self.threshold and
    #             abs(self.y_point - point.y_point) < self.threshold and
    #             self.distance(point) < self.threshold
    #     )
    #
    # def validate_neighborhood(self, points):
    #     neighborhood = [point for point in points if self.point_validator(point)]
    #
    #     if neighborhood:
    #         neighborhoods = list(set([point.cluster for point in neighborhood if point.cluster is not None]))
    #
    #         if neighborhoods:
    #             cluster = neighborhoods[0]
    #             for cluster_ in neighborhoods[1:]:
    #                 cluster.conquer(cluster_.points)
    #         else:
    #             cluster = Cluster()
    #
    #         for neighbor in neighborhood:
    #             neighbor.set_cluster(cluster)
    #
    #         self.set_cluster(cluster)
    #     else:
    #         self.valid = False
    #         cluster = None
    #     return cluster

    def render(self, image):
        if self.valid:
            if self.cluster is not None:
                cv2.circle(image, (int(self.x), int(self.y)), 1, self.cluster.color, -1)
            else:
                cv2.circle(image, (int(self.x), int(self.y)), 3, (0, 0, 0), -1)
