from time import time, sleep

import cv2

from model.Canny import Canny
from model.CoordinateDampner import CoordinateDampner
from model.FrameBuffer import FrameBuffer

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
