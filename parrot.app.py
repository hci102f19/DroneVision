from time import time

import cv2
from pyparrot.Bebop import Bebop

from libs import show
from model.Box import Box
from model.Canny import Canny
from model.StreamBuffer import StreamBuffer

# Thanks:
# http://answers.opencv.org/question/192178/how-to-set-ffmpeg-option-protocol_whitelist-fileudprtp-in-videocapture/
# os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

canny = Canny()

fps_real = 10
fps = 1 / fps_real

count = 0
# region Hitbox caclulations
width, height = 640, 360

w_center = 0.20
h_center = 0.20
h_offset = 0.20

x1 = int(width * ((1 - w_center) / 2))
y1 = int(height * (((1 - h_center) / 2) - h_offset))
x2 = int(width * (1 - ((1 - w_center) / 2)))
y2 = int(height * ((1 - ((1 - h_center) / 2)) - h_offset))

hitbox = Box(x1, y1, x2, y2)
# endregion

bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)

if success:
    bebop.start_video_stream()
    cam = cv2.VideoCapture("./ParrotStream/bebop.sdp")

    stream = StreamBuffer(cam)
    stream.start()
    try:
        while stream.running():
            frame = stream.pop()

            if frame is not None:
                start = time()
                points, center = canny.process_frame(frame)

                hitbox.render(frame)

                if points:
                    for p in points:
                        p.render(frame)

                if center is not None:
                    center.render(frame)
                    if not hitbox.intersects(center):
                        cv2.imwrite(f'./output/{count}.png', frame)

                show(frame, fps=True, fps_target=10, wait=1)
    except Exception:
        print("FAK!")
        stream.kill()
        bebop.stop_video_stream()
        bebop.disconnect()
