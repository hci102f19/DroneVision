import cv2


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def render(self, image):
        return cv2.circle(image, (self.x, self.y), 5, (255, 0, 0), -1)
