from model.extended_geometry.hitbox.HitBox import HitBox
from model.extended_geometry.hitbox.ReverseHitBox import ReverseHitBox


class BoxContainer(object):
    def __init__(self, x, y, **kwargs):
        height = kwargs.get('height', 0.4)
        width = kwargs.get('width', 0.45)

        center_width = kwargs.get('w_center', 0.1)
        center_height = kwargs.get('h_center', 0.2)
        center_height_offset = kwargs.get('h_offset', 0.2)

        self.lb = HitBox(0, y, x * width, y * (1 - height))
        self.rb = HitBox(x, y, x * (1 - width), y * (1 - height))

        self.center = ReverseHitBox(
            x * ((1 - center_width) / 2),
            y * (((1 - center_height) / 2) - center_height_offset),
            x * (1 - ((1 - center_width) / 2)),
            y * (1 - ((1 - center_height) / 2) - center_height_offset)
        )

        self.boxes = [
            self.lb,
            self.rb,
            self.center,
        ]

    def render(self, image, color):
        for box in self.boxes:
            box.render(image, color)
