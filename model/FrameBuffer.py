import threading
from time import time, sleep

import cv2


class FrameBuffer(threading.Thread):
    def __init__(self, stream, x=640, y=360):
        super().__init__()

        if not isinstance(stream, cv2.VideoCapture):
            raise Exception("Not video stream")

        self.stream = stream

        self.fps = self.stream.get(cv2.CAP_PROP_FPS)

        self._current_frame = None
        self._running = False

        self.size = (x, y)
        self.blur = 3

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

            frame = image

            frame = cv2.resize(frame, self.size)
            frame = cv2.GaussianBlur(frame, (self.blur, self.blur), 0)

            self._current_frame = frame
            success, image = self.stream.read()

            self.sleep(time() - start)

        self._running = False
        self._current_frame = None

    def get(self):
        return self._current_frame

    def pop(self):
        frame, self._current_frame = self._current_frame, None
        return frame

    def running(self):
        return self._running

    def kill(self):
        self._running = False
