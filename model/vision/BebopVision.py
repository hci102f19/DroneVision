from pyparrot.Bebop import Bebop

from model.drone_wrappers.BebopWrapper import BebopWrapper
from model.exceptions import InvalidDroneType
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
        self.bebop.run()

        self.vision_loop()

    def hit(self):
        vector = self.box_container.hit(self.get_center())
        # vector.set_pitch(50)

        if not vector.is_null():
            self.bebop.enqueue_vector(vector)

    def kill(self):
        super().kill()

        self.bebop.stop_video_stream()
        self.bebop.disconnect()
