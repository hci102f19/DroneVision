from shapely.geometry import GeometryCollection

from model.extended_geometry.Cluster import Cluster
from model.geometry.Point import Point


class Clusters(object):
    def __init__(self):
        self.clusters = {}

    def get_cluster(self, idx):
        if idx not in self.clusters:
            self.clusters[idx] = Cluster()
        return self.clusters[idx]

    def as_list(self):
        return [cluster for _, cluster in self.clusters.items()]

    def best_cluster_as_point(self):
        clusters = sorted(self.as_list(), key=lambda cluster: cluster.density(), reverse=True)

        cgc = GeometryCollection(clusters[0].points)

        return Point(*cgc.centroid.xy)

    def is_empty(self):
        return len(self.clusters) == 0
