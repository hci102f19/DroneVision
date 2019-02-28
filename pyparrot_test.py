# Thanks:
# http://answers.opencv.org/question/192178/how-to-set-ffmpeg-option-protocol_whitelist-fileudprtp-in-videocapture/
# os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

import cv2
from pyparrot.Bebop import Bebop

from model.Canny import Canny
from model.CoordinateDampner import CoordinateDampner
from model.StreamBuffer import StreamBuffer

bebop = Bebop()
coordinate_dampner = CoordinateDampner(2)

# connect to the bebop
success = bebop.connect(5)

if success:
    bebop.start_video_stream()

    cam = cv2.VideoCapture("./ParrotStream/bebop.sdp")

    stream = StreamBuffer(cam)
    stream.start()

    while stream.running():
        img = stream.get()

        if img is not None:
            canny = Canny(img)
            canny.process_frame()

            point = canny.get_center()
            if point is not None and point.x is not None and point.y is not None:
                cv2.circle(img, (point.x, point.y), 3, (0, 255, 0), -1)
            else:
                print("STOP IT TAF!!!")

            cv2.imshow("frame", img)
            cv2.waitKey(1)

        # bebop.smart_sleep(0.01)
