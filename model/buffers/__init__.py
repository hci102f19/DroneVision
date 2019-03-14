import threading

import cv2


class Buffer(threading.Thread):
    def __init__(self, stream, x=640, y=360):
        super().__init__()

        self.stream = stream

        self.size = (x, y)
        self.blur = 3

        self._latest_frame = None
        self._running = False

    def get(self):
        return self._latest_frame

    def pop(self):
        frame, self._latest_frame = self._latest_frame, None
        return frame

    def running(self):
        return self._running

    def kill(self):
        self._running = False

    def pre_process_frame(self, frame):
        frame = cv2.resize(frame, self.size)
        frame = cv2.GaussianBlur(frame, (self.blur, self.blur), 0)

        return frame
