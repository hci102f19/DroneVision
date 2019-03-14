from model.geometry.Box import Box


class BoxContainer(object):
    def __init__(self, x, y, **kwargs):
        height = kwargs.get('height', 0.4)
        width = kwargs.get('width', 0.45)
        w_center = kwargs.get('w_center', 0.1)
        h_center = kwargs.get('h_center', 0.2)
        h_offset = kwargs.get('h_offset', 0.2)

        self.lb = Box(0, y, x * width, y * (1 - height))
        self.rb = Box(x, y, x * (1 - width), y * (1 - height))

        self.center = Box(
            x * ((1 - w_center) / 2),
            y * (((1 - h_center) / 2) - h_offset),
            x * (1 - ((1 - w_center) / 2)),
            y * ((1 - ((1 - h_center) / 2)) - h_offset)
        )

    def render(self, image):
        self.center.render(image)
        self.lb.render(image)
        self.rb.render(image)
