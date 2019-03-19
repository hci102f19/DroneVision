import glob
import random
import cv2

from model.buffers.FrameBuffer import FrameBuffer
from model.exceptions import Quit
from model.vision.DroneVision import DroneVision

modifier = 4
files = glob.glob('./output/*.mp4')

stream = cv2.VideoCapture(random.choice(files))
frame_buffer = FrameBuffer(stream, 960, 720)

try:
    drone_vision = DroneVision(frame_buffer)
    drone_vision.start()
except Quit:
    try:
        drone_vision.kill()
    except NameError:
        pass
