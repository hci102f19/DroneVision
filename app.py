from time import time

import cv2

from libs import show
from model.Canny import Canny
from model.CenterBox import CenterBox
from model.FrameBuffer import FrameBuffer

stream = cv2.VideoCapture('./source/video.v2.mp4')
fb = FrameBuffer(stream)
fb.start()

canny = Canny()

cb = CenterBox(*fb.size, 0.2, 0.2, 0.2)

while fb.running():
    frame = fb.get()
    if frame is not None:
        points, center = canny.process_frame(frame)

        cb.render(frame)

        if points:
            for p in points:
                p.render(frame)

        if center is not None:
            center.render(frame)

        show(frame, fps=True, fps_target=10, wait=1)

        end = time()
