from model.vision.DroneVision import DroneVision


class BebopVision(DroneVision):
    def __init__(self, bebop, buffer):
        super().__init__(buffer)

        self.bebop = bebop
        bebop.start_video_stream()

    def kill(self):
        super().kill()

        self.bebop.stop_video_stream()
        self.bebop.disconnect()
