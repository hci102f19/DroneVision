from time import time

import cv2
from pyparrot.Bebop import Bebop

from libs import show
from model.Canny import Canny
from model.CenterBox import CenterBox
from model.StreamBuffer import StreamBuffer

# Thanks:
# http://answers.opencv.org/question/192178/how-to-set-ffmpeg-option-protocol_whitelist-fileudprtp-in-videocapture/
# os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)

if success:
    bebop.start_video_stream()
    cam = cv2.VideoCapture("./ParrotStream/bebop.sdp")

    stream = StreamBuffer(cam)
    stream.start()

    cb = CenterBox(*stream.size, 0.2, 0.2, 0.2)
    canny = Canny()

    try:
        while stream.running():
            frame = stream.pop()

            if frame is not None:
                start = time()
                points, center = canny.process_frame(frame)

                cb.render(frame)

                if points:
                    for p in points:
                        p.render(frame)

                if center is not None:
                    center.render(frame)

                k = show(frame, fps=True, fps_target=10, wait=1)
                if k == 27:
                    stream.kill()
                    bebop.stop_video_stream()
                    bebop.disconnect()
    except Exception:
        print("FAK!")
        # stream.kill()
        # bebop.stop_video_stream()
        # bebop.disconnect()
