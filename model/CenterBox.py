from model.Box import Box


class CenterBox(object):
    def __init__(self, width, height, w_center, h_center, h_offset):
        self.width = width
        self.height = height

        self.w_center = w_center
        self.h_center = h_center
        self.h_offset = h_offset

        x1 = int(width * ((1 - w_center) / 2))
        y1 = int(height * (((1 - h_center) / 2) - h_offset))
        x2 = int(width * (1 - ((1 - w_center) / 2)))
        y2 = int(height * ((1 - ((1 - h_center) / 2)) - h_offset))

        self.box = Box(x1, y1, x2, y2)

    def render(self, image):
        self.box.render(image)
