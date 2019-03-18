from pyparrot.Bebop import Bebop

from model.exceptions import InvalidDroneType
from model.vision.DroneVision import DroneVision


class BebopVision(DroneVision):
    def __init__(self, bebop, buffer, **kwargs):
        super().__init__(buffer)

        if not isinstance(bebop, Bebop):
            raise InvalidDroneType()

        self.bebop = bebop
        bebop.start_video_stream()

        self.sleep = kwargs.get('sleep', 5)

    def start(self):
        self.buffer.start()
        self.bebop.smart_sleep(self.sleep)

        self.vision_loop()

    def hit(self):
        vector = self.box_container.hit(self.get_center())

        if not vector.is_null():
            print(vector.emit())

    def kill(self):
        super().kill()

        self.bebop.stop_video_stream()
        self.bebop.disconnect()
