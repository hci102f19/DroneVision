# Thanks:
# http://answers.opencv.org/question/192178/how-to-set-ffmpeg-option-protocol_whitelist-fileudprtp-in-videocapture/
# os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

import cv2
from pyparrot.Bebop import Bebop

from DroneVision import DroneVision
from model.buffers.StreamBuffer import StreamBuffer

bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)

if success:
    bebop.start_video_stream()

    cam = cv2.VideoCapture("./ParrotStream/bebop.sdp")
    stream = StreamBuffer(cam)


    def kill_function():
        bebop.stop_video_stream()
        bebop.disconnect()


    drone_vision = DroneVision(stream, kill_function=kill_function)
    drone_vision.start()
