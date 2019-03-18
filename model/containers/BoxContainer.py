from model.extended_geometry.hitbox.HitBox import HitBox
from model.extended_geometry.hitbox.ReverseHitBox import ReverseHitBox
from model.flight.Vector import Vector
from model.geometry.Point import Point


class BoxContainer(object):
    def __init__(self, x, y, **kwargs):
        hitbox_height = kwargs.get('hitbox_height', 0.70)
        hitbox_width = kwargs.get('hitbox_width', 0.17)
        hitbox_horizontal_offset = kwargs.get('hitbox_horizontal_offset', 0.18)
        hitbox_vertical_offset = kwargs.get('hitbox_vertical_offset', -0.10)
        hitbox_rotation = kwargs.get('hitbox_rotation', 30)

        center_width = kwargs.get('w_center', 0.1)
        center_height = kwargs.get('h_center', 0.2)
        center_height_offset = kwargs.get('h_offset', 0.25)

        self.lb = HitBox(
            hitbox_horizontal_offset * x,
            y - (hitbox_vertical_offset * y),
            x * hitbox_width + (hitbox_horizontal_offset * x),
            y * (1 - hitbox_height) - (hitbox_vertical_offset * y),
            force=50,
            rotation=hitbox_rotation
        )
        self.rb = HitBox(
            x - (hitbox_horizontal_offset * x),
            y - (hitbox_vertical_offset * y),
            x * (1 - hitbox_width) - (hitbox_horizontal_offset * x),
            y * (1 - hitbox_height) - (hitbox_vertical_offset * y),
            force=-50,
            rotation=-hitbox_rotation
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
            box.hit(point, vector)
        return vector

    def render(self, image, color):
        for box in self.boxes:
            box.render(image, color)
