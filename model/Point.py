import cv2


class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        return

    @property
    def x(self):
        return int(round(self._x, 0))

    @property
    def y(self):
        return int(round(self._y, 0))

    def render(self, image):
        return cv2.circle(image, (self.x, self.y), 5, (255, 0, 0), -1)
