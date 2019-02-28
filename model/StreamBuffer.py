import threading

import cv2


class StreamBuffer(threading.Thread):
    def __init__(self, stream, x=640, y=360):
        super().__init__()

        self.stream = stream

        self.size = (x, y)

        self._latest_frame = None
        self._running = False

    def run(self):
        self._running = True

        while not self.stream.isOpened():
            print("Waiting for stream to open")

        success, image = self.stream.read()
        while success:
            try:
                self._latest_frame = cv2.resize(image, self.size)
            except Exception:
                pass

            success, image = self.stream.read()

        self._running = False
        self._latest_frame = None

    def get(self):
        return self._latest_frame

    def running(self):
        return self._running
