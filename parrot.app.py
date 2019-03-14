import cv2
from pyparrot.Bebop import Bebop

from libs import show
from model.Canny import Canny
from model.CenterBox import CenterBox
from model.SFiltering import SFiltering
from model.buffers.StreamBuffer import StreamBuffer

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

    center_box = CenterBox(*stream.size, w_center=0.1, h_center=0.2, h_offset=0.2)

    canny = Canny()
    small_filtering = SFiltering(10)

    try:
        while stream.running():
            frame = stream.pop()

            if frame is not None:
                _, center = canny.process_frame(frame)

                if center is not None:
                    small_filtering.add(center)

                damped_center = small_filtering.get_point()
                if damped_center is not None:
                    if not center_box.intersects(damped_center):
                        x, y = center_box.flight(damped_center)
                        print(f'x: {x}, y: {y}')

                    damped_center.render(frame)
                    center_box.render(frame, damped_center)

                k = show(frame, fps=True, fps_target=10, wait=1)
                if k == 27:
                    stream.kill()
                    bebop.stop_video_stream()
                    bebop.disconnect()
    except Exception as e:
        print(str(e))
        print("FAK!")
        # stream.kill()
        # bebop.stop_video_stream()
        # bebop.disconnect()
