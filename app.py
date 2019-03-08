from time import time

import cv2

from libs import show
from model.Box import Box
from model.Canny import Canny

stream = cv2.VideoCapture('./source/video.v2.mp4')
success, image = stream.read()

canny = Canny()

fps_real = 10
fps = 1 / fps_real

count = 0

width, height = 640, 360

w_center = 0.20
h_center = 0.20
h_offset = 0.20

x1 = int(width * ((1 - w_center) / 2))
y1 = int(height * (((1 - h_center) / 2) - h_offset))
x2 = int(width * (1 - ((1 - w_center) / 2)))
y2 = int(height * ((1 - ((1 - h_center) / 2)) - h_offset))

hitbox = Box(x1, y1, x2, y2)

while success:
    frame = image
    frame = cv2.resize(frame, (width, height))
    frame = cv2.GaussianBlur(frame, (3, 3), 0)

    if frame is not None:
        start = time()
        points, center = canny.process_frame(frame)

        if points:
            for p in points:
                p.render(frame)

        if center is not None:
            if hitbox.intersects(center):
                center.render(frame)

        # out.write(frame)
        hitbox.render(frame)
        show(frame, fps=True, fps_target=10, wait=1)

        # cv2.imwrite(f'./output/{count}.png', frame)

        end = time()

        # if end - start < fps:
        #     sleep(fps - (end - start))
    count += 1
    success, image = stream.read()
