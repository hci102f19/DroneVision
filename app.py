import sys
from time import time, sleep

import cv2

from model.Canny import Canny
from model.CoordinateDampner import CoordinateDampner
from model.FrameBuffer import FrameBuffer

# We need to do this for the cluster export
sys.setrecursionlimit(10000)

stream = cv2.VideoCapture('./source/video.v2.mp4')
fb = FrameBuffer(stream)

coordinate_dampner = CoordinateDampner(2)

fb.start()

count = 0
fps = 10

size = (640, 360)
out = cv2.VideoWriter('./test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), float(fps), size)

offset = 0.1

x_center = (size[0] / 2)
x_offset = size[0] * offset
x1 = int(x_center - x_offset)
x2 = int(x_center + x_offset)

y_center = (size[1] / 4)
y_offset = size[1] * offset
y1 = int(y_center - y_offset)
y2 = int(y_center + y_offset)

while fb.running():
    frame = fb.get()
    start = time()

    if frame is not None:
        canny = Canny(frame)
        canny.process_frame()

        point = canny.get_center()

        if point is not None and point.is_valid():
            coordinate_dampner.enqueue(point)

        d_point = coordinate_dampner.point()

        if x1 < d_point.x < x2 and y1 < d_point.y < y2:
            cv2.circle(frame, (d_point.x, d_point.y), 3, (0, 255, 0), -1)
        else:
            cv2.circle(frame, (d_point.x, d_point.y), 3, (0, 0, 255), -1)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

        out.write(frame)

        count += 1

    end = time()

    if end - start > 1 / fps:
        continue

    sleep((1 / fps) - (end - start))
out.release()
