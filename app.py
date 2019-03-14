import cv2

from DroneVision import DroneVision
from model.buffers.FrameBuffer import FrameBuffer

stream = cv2.VideoCapture('./source/video.v2.mp4')
frame_buffer = FrameBuffer(stream)

drone_vision = DroneVision(frame_buffer)
drone_vision.start()
