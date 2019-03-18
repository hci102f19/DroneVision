import cv2
from pyparrot.Bebop import Bebop

from model.buffers.StreamBuffer import StreamBuffer
from model.vision.BebopVision import BebopVision

bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)

if success:
    cam = cv2.VideoCapture("./ParrotStream/bebop.sdp")
    stream = StreamBuffer(cam, 640, 480)

    drone_vision = BebopVision(bebop, stream)
    drone_vision.start()
