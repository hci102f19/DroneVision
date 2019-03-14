from libs import show
from model.Canny import Canny
from model.buffers import Buffer
from model.extended_geometry.BoxContainer import BoxContainer


class DroneVision(Canny):
    def __init__(self, buffer, **kwargs):
        super().__init__()

        if not isinstance(buffer, Buffer):
            raise Exception('Type is not buffer')

        self.buffer = buffer

        self.box_container = BoxContainer(*self.buffer.size)

        self.renders = [
            self.box_container
        ]
        self.tmp_renders = []

        self.color = (0, 0, 0)

        self.kill_function = kwargs.get('kill_function', None)

    def start(self):
        self.buffer.start()

        while self.buffer.running():
            frame = self.buffer.pop()
            if frame is not None:
                self.process_frame(frame)

                self.box_container.hit(self.get_center())

                self.render(frame)
                k = show(frame, fps=True, fps_target=10, wait=1)

                if k == 27:
                    self.kill()

    def kill(self):
        self.buffer.kill()

        if self.kill_function is not None:
            self.kill_function()

    def render(self, image):
        self.get_center().render(image)
        for element in self.renders:
            element.render(image, self.color)
