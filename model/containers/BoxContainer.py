import json
from json import JSONDecodeError

from model.extended_geometry.hitbox.HitBox import HitBox
from model.extended_geometry.hitbox.ReverseHitBox import ReverseHitBox
from model.flight.Vector import Vector
from model.geometry.Point import Point


class BoxContainer(object):
    def __init__(self, x, y, **kwargs):
        height = kwargs.get('height', 1.000)
        width = kwargs.get('width', 0.40)

        center_width = kwargs.get('w_center', 0.1)
        center_height = kwargs.get('h_center', 0.2)
        center_height_offset = kwargs.get('h_offset', 0.2)

        self.lb = HitBox(0, y, x * width, y * (1 - height), force=50, rotation=45)
        self.rb = HitBox(x, y, x * (1 - width), y * (1 - height), force=-50, rotation=-45)

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

    def hit(self, point: Point, frame):
        # self.load_config()
        vector = Vector()
        for box in self.boxes:
            if box.hit(point, vector):
                box.render(frame, (255, 255, 255))

        if not vector.is_null():
            print("WE NEED TO MOVE BOIZ!")
            print(json.dumps(vector.emit(), indent=4))
        return None

    def render(self, image, color):
        for box in self.boxes:
            box.render(image, color)

    def load_config(self):
        try:
            data = json.load(open('./config.json', 'r'))

            for k, v in data.items():
                setattr(self, k, v)

            self.lb = HitBox(0, self.y, self.x * data.get('width'), self.y * (1 - data.get('height')), force=50)
            self.rb = HitBox(self.x, self.y, self.x * (1 - data.get('width')), self.y * (1 - data.get('height')),
                             force=-50)

            self.center = ReverseHitBox(
                self.x * (1 - ((1 - data.get('center_width')) / 2)),
                self.y * (((1 - data.get('center_height')) / 2) - data.get('center_height_offset')),
                self.x * ((1 - data.get('center_width')) / 2),
                self.y * (1 - ((1 - data.get('center_height')) / 2) - data.get('center_height_offset'))
            )

            self.boxes = [
                self.lb,
                self.rb,
                self.center,
            ]
        except (JSONDecodeError, PermissionError):
            print("JSONDecodeError!")
