from libs import show
from model.buffers import Buffer
from model.extended_geometry.BoxContainer import BoxContainer


class DroneVision(object):
    def __init__(self, buffer):
        if not isinstance(buffer, Buffer):
            raise Exception('Type is not buffer')

        self.buffer = buffer

        self.box_container = BoxContainer(*self.buffer.size)

        self.renders = [
            self.box_container
        ]

    def start(self):
        self.buffer.start()

        while self.buffer.running():
            frame = self.buffer.pop()
            if frame is not None:

                self.render(frame)
                k = show(frame, fps=True, fps_target=10, wait=1)

                if k == 27:
                    self.buffer.kill()

    def render(self, image):
        for element in self.renders:
            element.render(image)
