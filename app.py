import cv2

from model.buffers.FrameBuffer import FrameBuffer
from model.exceptions import Quit
from model.vision.DroneVision import DroneVision

modifier = 4

stream = cv2.VideoCapture('./source/video.v2.mp4')
frame_buffer = FrameBuffer(stream, 960, 720)

try:
    drone_vision = DroneVision(frame_buffer)
    drone_vision.start()
except Quit:
    try:
        drone_vision.kill()
    except NameError:
        pass
