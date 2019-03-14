from time import time, sleep

import cv2

from model.buffers import Buffer


class FrameBuffer(Buffer):
    def __init__(self, stream, x=640, y=360):
        if not isinstance(stream, cv2.VideoCapture):
            raise Exception("Not video stream")

        super().__init__(stream, x, y)

        self.fps = self.stream.get(cv2.CAP_PROP_FPS)

        self.overflow = 0
        self.sleep_timer = 1 / self.fps

    def sleep(self, exec_time):
        exec_time = exec_time + self.overflow + 0.002  # Magic 0.002 overflow number, for dat magic match

        if exec_time >= self.sleep_timer:
            self.overflow = exec_time - self.sleep_timer
        else:
            self.overflow = 0

            # Busy sleep would be better.
            sleep(self.sleep_timer - exec_time)

    def run(self):
        self._running = True
        success, image = self.stream.read()

        while success and self._running:
            start = time()

            self._latest_frame = self.pre_process_frame(image)
            success, image = self.stream.read()

            self.sleep(time() - start)

        self._running = False
        self._latest_frame = None
