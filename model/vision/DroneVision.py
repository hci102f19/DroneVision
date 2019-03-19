from libs import show
from model.Canny import Canny
from model.buffers import Buffer
from model.containers.BoxContainer import BoxContainer
from model.exceptions import InvalidVideoBuffer
from model.key import Key


class DroneVision(Canny):
    def __init__(self, buffer):
        if not isinstance(buffer, Buffer):
            raise InvalidVideoBuffer()

        super().__init__(*buffer.size)
        self.buffer = buffer

        self.box_container = BoxContainer(*self.buffer.size)

        self.renders = [
            self.box_container
        ]
        self.tmp_renders = []

        self.view = True

        self.fly = Key()
        self.send_commands = Key(True)

        self.color = (0, 0, 0)

    def start(self):
        self.buffer.start()

        self.vision_loop()

    def vision_loop(self):
        while self.buffer.running():
            self.tmp_renders.clear()
            frame = self.buffer.pop()

            if frame is not None:
                self.process_frame(frame)
                self.hit()

                if self.get_latest_clusters() is not None:
                    for cluster in self.get_latest_clusters():
                        self.tmp_renders.append(cluster)

                self.render_view(frame)

    def render_view(self, frame):
        if self.view:
            self.render(frame)

            key = show(frame, fps=True, fps_target=10, wait=1, size=(640, 480))

            if key == 27:
                self.kill()

            self.fly.set(key, 119)
            self.send_commands.set(key, 115)

    def hit(self):
        if self.get_center() is not None:
            self.box_container.hit(self.get_center())

    def kill(self):
        self.buffer.kill()

    def render(self, image):

        for element in [self.get_center()] + self.tmp_renders + self.renders:
            if element is not None:
                element.render(image, self.color)
