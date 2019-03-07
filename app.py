from time import time, sleep

import cv2

from libs import show
from model.Canny import Canny
from model.FrameBuffer import FrameBuffer

stream = cv2.VideoCapture('./source/video.v2.mp4')

fb = FrameBuffer(stream)
fb.start()

canny = Canny()

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
# out = cv2.VideoWriter('./test.mp4', fourcc, 30.0, (640, 360))

while fb.running():
    frame = fb.get()
    if frame is not None:
        start = time()
        points = canny.process_frame(frame)

        for point in points:
            point.render(frame)

        # out.write(frame)
        show(frame, fps=True, fps_target=10, wait=1)
        end = time()

        # continue
        fps = 1 / 30

        if end - start < fps:
            sleep(fps - (end - start))
# out.release()
