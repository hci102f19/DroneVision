import cv2

from DroneVision import DroneVision
from model.buffers.FrameBuffer import FrameBuffer
from model.exceptions import Quit

stream = cv2.VideoCapture('./source/video.v2.mp4')
frame_buffer = FrameBuffer(stream, 640, 360)

try:
    drone_vision = DroneVision(frame_buffer)
    drone_vision.start()
except Quit:
    try:
        drone_vision.kill()
    except NameError:
        pass
