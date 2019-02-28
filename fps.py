# import cv2
#
# stream = cv2.VideoCapture('./source/destination_all.mp4')
# fps = stream.get(cv2.CAP_PROP_FPS)
#
# fps_target = 10
#
# size = (640, 360)
#
# print(fps)
# # resized_image = cv2.resize(image, (100, 50))
import threading
from time import time, sleep

import cv2

from model.Canny import Canny
from model.CoordinateDampner import CoordinateDampner


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


fb = FrameBuffer()
coordinate_dampner = CoordinateDampner(2)

fb.start()

count = 0
fps = 10

size = (640, 360)
out = cv2.VideoWriter('./test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), float(25), size)

while fb.running():
    frame = fb.get()
    start = time()

    if frame is not None:
        canny = Canny(frame)
        canny.process_frame()

        point = canny.get_center()

        if point is not None and point.is_valid():
            cv2.circle(frame, (point.x, point.y), 5, (0, 0, 255), -1)
            coordinate_dampner.enqueue(point)

        d_point = coordinate_dampner.point()
        cv2.circle(frame, (d_point.x, d_point.y), 3, (255, 255, 0), -1)

        out.write(frame)

        count += 1

    end = time()

    if end - start > 1 / fps:
        continue

    sleep((1 / fps) - (end - start))
out.release()
