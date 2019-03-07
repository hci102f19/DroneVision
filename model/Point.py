from time import time

import cv2
from shapely.geometry import Point as BasePoint


class Point(BasePoint):
    def __init__(self, x, y):
        super().__init__([x[0], y[0]])

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

    def validate_neighborhood(self, points):
        start = time()
        neighborhood = [point for point in points if self.distance(point) < self.threshold]
        print(round(time() - start, 2))
        return

        if neighborhood:
            # neighborhoods = list(set([point.cluster for point in neighborhood if point.cluster is not None]))
            #
            # if neighborhoods:
            #     cluster = neighborhoods[0]
            #     for cluster_ in neighborhoods[1:]:
            #         cluster.conquer(cluster_.points)
            # else:
            #     cluster = Cluster()
            #
            # self.set_cluster(cluster)
            self.valid = True
        else:
            self.valid = False

    def render(self, image):
        render = 2
        if self.valid:
            if render == 1:
                cv2.circle(image, (int(self.x), int(self.y)), 1, (0, 0, 0), -1)
                cv2.circle(image, (int(self.x), int(self.y)), self.threshold, (255, 255, 255), 1)
            else:
                if self.cluster is not None:
                    if len(self.cluster.points) > 0:
                        r, g, b = self.cluster.color
                        cv2.circle(image, (int(self.x), int(self.y)), 1, (int(b), int(g), int(r)), -1)
