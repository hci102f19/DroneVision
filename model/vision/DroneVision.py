from libs import show
from model.Canny import Canny
from model.buffers import Buffer
from model.containers.BoxContainer import BoxContainer


class DroneVision(Canny):
    def __init__(self, buffer):
        if not isinstance(buffer, Buffer):
            raise Exception('Type is not buffer')

        super().__init__(*buffer.size)
        self.buffer = buffer

        self.box_container = BoxContainer(*self.buffer.size)

        self.renders = [
            self.box_container
        ]
        self.tmp_renders = []

        self.view = True

        self.color = (0, 0, 0)

    def start(self):
        self.buffer.start()

        self.vision_loop()

    def vision_loop(self):
        while self.buffer.running():
            self.tmp_renders = []
            frame = self.buffer.pop()
            if frame is not None:
                self.process_frame(frame)
                self.hit()

                self.render(frame)

                if self.view:
                    k = show(frame, fps=True, fps_target=10, wait=1)

                    if k == 27:
                        self.kill()

    def hit(self):
        self.box_container.hit(self.get_center())

    def kill(self):
        self.buffer.kill()

    def render(self, image):
        self.get_center().render(image)
        for element in self.tmp_renders + self.renders:
            element.render(image, self.color)
