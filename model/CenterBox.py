from model.Box import Box


class CenterBox(object):
    def __init__(self, width, height, w_center, h_center, h_offset):
        self.width = width
        self.height = height

        self.w_center = w_center
        self.h_center = h_center
        self.h_offset = h_offset

        self.x1 = int(width * ((1 - w_center) / 2))
        self.y1 = int(height * (((1 - h_center) / 2) - h_offset))
        self.x2 = int(width * (1 - ((1 - w_center) / 2)))
        self.y2 = int(height * ((1 - ((1 - h_center) / 2)) - h_offset))

        self.box = Box(self.x1, self.y1, self.x2, self.y2)

    def render(self, image):
        self.box.render(image)
