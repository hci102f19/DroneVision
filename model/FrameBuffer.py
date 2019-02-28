import threading
from time import time

import cv2


class FrameBuffer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stream = cv2.VideoCapture('./source/destination_all.mp4')

        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.frames = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)

        self._current_frame = None
        self._running = False

        self.size = (640, 360)

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

        while success:
            start = time()

            self._current_frame = cv2.resize(image, self.size)
            success, image = self.stream.read()

            self.sleep(time() - start)

        self._running = False
        self._current_frame = None

    def get(self):
        return self._current_frame

    def running(self):
        return self._running
