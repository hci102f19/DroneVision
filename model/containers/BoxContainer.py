from model.extended_geometry.hitbox.LeftHitBox import LeftHitBox
from model.extended_geometry.hitbox.ReverseHitBox import ReverseHitBox
from model.extended_geometry.hitbox.RightHitBox import RightHitBox
from model.flight.Vector import Vector
from model.geometry.Point import Point


class BoxContainer(object):
    def __init__(self, x, y, **kwargs):
        # center_width = kwargs.get('w_center', 0.1)
        center_width = kwargs.get('w_center', 0.065)
        center_height = kwargs.get('h_center', 0.2)
        center_height_offset = kwargs.get('h_offset', 0.25)

        self.lb = LeftHitBox(
            x,
            y,
            width_top=0.97,
            width_bottom=0.6,
            height_top=0.6,
            force=-20
        )
        self.rb = RightHitBox(
            x,
            y,
            width_top=0.97,
            width_bottom=0.6,
            height_top=0.6,
            force=20
        )

        self.x = x
        self.y = y

        self.center = ReverseHitBox(
            x * (1 - ((1 - center_width) / 2)),
            y * (((1 - center_height) / 2) - center_height_offset),
            x * ((1 - center_width) / 2),
            y * (1 - ((1 - center_height) / 2) - center_height_offset)
        )

        self.boxes = [
            self.lb,
            self.rb,
            self.center,
        ]

    def hit(self, point: Point):
        vector = Vector()
        for box in self.boxes:
            if box.hit(point, vector):
                return vector
        return vector

    def render(self, image, color):
        for box in self.boxes:
            box.render(image, color)
