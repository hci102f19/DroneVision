from time import time

import cv2

from libs import show
from model.Canny import Canny
from model.CenterBox import CenterBox
from model.FrameBuffer import FrameBuffer
from model.SFiltering import SFiltering

stream = cv2.VideoCapture('./source/video.v2.mp4')
fb = FrameBuffer(stream)
fb.start()

canny = Canny()
sf = SFiltering(10)

while fb.running():
    frame = fb.pop()
    if frame is not None:

        # data = json.load(open('test.json', 'r'))

        cb = CenterBox(*fb.size, w_center=0.1, h_center=0.2, h_offset=0.2)
        # cb = CenterBox(*fb.size, **data)

        points, center = canny.process_frame(frame)

        cb.render(frame)

        if points and False:
            for p in points:
                p.render(frame)

        if center is not None:
            sf.add(center)
            center2 = sf.get_point()

            if center2 is not None:
                center2.render(frame)
            # center.render(frame)

        show(frame, fps=True, fps_target=10, wait=1)

        end = time()
