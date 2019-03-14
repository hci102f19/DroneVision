import cv2

from libs import show
from model.buffers.FrameBuffer import FrameBuffer

stream = cv2.VideoCapture('./source/video.v2.mp4')
frame_buffer = FrameBuffer(stream)
frame_buffer.start()

while frame_buffer.running():
    frame = frame_buffer.pop()
    if frame is not None:

        show(frame, fps=True, fps_target=10, wait=1)
