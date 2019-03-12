import numpy as np

from model.Point import Point


class SFiltering(object):
    """
    Small Filtering
    An Naïve approach to GPS smoothing
    """

    def __init__(self, history_size=6, xmax=640, ymax=480):
        self.points = []
        self.rejected_list = []

        self.history_size = history_size

        self.xmax = xmax
        self.ymax = ymax

        self.deviation_max = 0.1

    def point2percent(self, point):
        return point.x_point / self.xmax, point.y_point / self.ymax

    def add(self, point):
        if 0 > point.y_point or point.y_point > self.ymax or 0 > point.x_point or point.x_point > self.xmax:
            return
        if not self.points:
            self.points.append(point)
            return

        if not self.deviate(self.points, point):
            self.points = self.points[-(self.history_size - 1):] + [point]
            self.rejected_list.clear()
        else:
            # self.rejected_list.append(point)
            self.rejected_list = self.rejected_list[-(self.history_size - 1):] + [point]
            if len(self.rejected_list) > int(self.history_size / 2) and not self.deviate(self.rejected_list, point):
                print("SETTING NEW POINTS LIST!")
                self.points.clear()
                for p in self.rejected_list:
                    self.points.append(p)
                self.rejected_list.clear()

    def deviate(self, lst, point):
        x2, y2 = self.point2percent(point)
        for p in lst:
            x1, y1 = self.point2percent(p)
            if abs(x1 - x2) >= self.deviation_max or abs(y1 - y2) >= self.deviation_max:
                return True
        return False

    @staticmethod
    def mean(val):
        return int(round(np.mean(val), 0))

    def get_mean(self):
        x = [point.x_point for point in self.points]
        y = [point.y_point for point in self.points]
        return Point.points2point(self.mean(x), self.mean(y))

    def get_point(self):
        if self.points:
            return self.get_mean()
        return None
