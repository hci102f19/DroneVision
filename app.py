from time import time

import cv2

from libs import show
from model.Box import Box
from model.Canny import Canny
from model.FrameBuffer import FrameBuffer

stream = cv2.VideoCapture('./source/video.v2.mp4')
fb = FrameBuffer(stream)
fb.start()

canny = Canny()

fps_real = 10
fps = 1 / fps_real

count = 0

width, height = fb.size

w_center = 0.20
h_center = 0.20
h_offset = 0.20

x1 = int(width * ((1 - w_center) / 2))
y1 = int(height * (((1 - h_center) / 2) - h_offset))
x2 = int(width * (1 - ((1 - w_center) / 2)))
y2 = int(height * ((1 - ((1 - h_center) / 2)) - h_offset))

hitbox = Box(x1, y1, x2, y2)

while fb.running():
    frame = fb.get()
    if frame is not None:
        frame = cv2.resize(frame, (width, height))
        frame = cv2.GaussianBlur(frame, (3, 3), 0)

        if frame is not None:
            start = time()
            points, center = canny.process_frame(frame)

            hitbox.render(frame)

            if points:
                for p in points:
                    p.render(frame)

            if center is not None:
                center.render(frame)

            show(frame, fps=True, fps_target=10, wait=1)

            end = time()
