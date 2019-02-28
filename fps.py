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

from libs import done


class FrameBuffer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stream = cv2.VideoCapture('./source/destination_all.mp4')

        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.frames = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)

        self._current_frame = None

        self.size = (640, 360)

        self.overflow = 0
        self.sleep_timer = 1 / self.fps

    def sleep(self, exec_time):
        exec_time = exec_time + self.overflow + 0.002  # Magic 0.002 overflow number, for dat magic match

        if exec_time >= self.sleep_timer:
            self.overflow = exec_time - self.sleep_timer
        else:
            self.overflow = 0

            sleep(self.sleep_timer - exec_time)

    def run(self):
        success, image = self.stream.read()

        while success:
            start = time()

            self._current_frame = cv2.resize(image, self.size)
            success, image = self.stream.read()

            self.sleep(time() - start)

        self._current_frame = None

        done()


fb = FrameBuffer()

fb.start()
