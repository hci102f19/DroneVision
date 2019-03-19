from pyparrot.Bebop import Bebop

from model.drone_wrappers.BebopWrapper import BebopWrapper
from model.exceptions import InvalidDroneType
from model.logging import log
from model.vision.DroneVision import DroneVision


class BebopVision(DroneVision):
    def __init__(self, bebop, buffer, **kwargs):
        super().__init__(buffer)

        if not isinstance(bebop, Bebop):
            raise InvalidDroneType()

        self.bebop = BebopWrapper(bebop)
        bebop.start_video_stream()

        self.sleep = kwargs.get('sleep', 5)

    def start(self):
        self.buffer.start()
        self.bebop.smart_sleep(self.sleep)
        self.bebop.start()

        self.vision_loop()

    def hit(self):
        if self.get_center() is None or self.get_center().is_empty:
            return

        vector = self.box_container.hit(self.get_center())

        if self.fly:
            if vector.is_null():
                vector.set_pitch(10)

        if self.send_commands:
            if not vector.is_null():
                self.bebop.enqueue_vector(vector)
        else:
            log.info("Command ignored")

    def kill(self):
        super().kill()

        self.bebop.stop_video_stream()
        self.bebop.disconnect()
