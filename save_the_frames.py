import numpy as np
from sklearn.cluster import KMeans as BaseKMeans


class KMeans(object):
    def __init__(self):
        self.history = []
        self.max_history = 10

    def get_history(self):
        hst = []

        for hst_ in self.history[-self.max_history:]:
            hst.extend(hst_)

        return np.array(hst)

    def get_kmeans(self, coordinates):
        self.history.append(coordinates)

        points = self.get_history()

        kmeans = BaseKMeans(n_clusters=5 if len(points) > 5 else 1)
        kmeans.fit(points)

        center = kmeans.cluster_centers_[0]

        return int(round(center[0], 0)), int(round(center[1], 0))
