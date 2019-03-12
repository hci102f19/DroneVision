import cv2

from libs import show
from model.Canny import Canny
from model.CenterBox import CenterBox
from model.FrameBuffer import FrameBuffer
from model.SFiltering import SFiltering

stream = cv2.VideoCapture('./source/video.v2.mp4')
frame_buffer = FrameBuffer(stream)
frame_buffer.start()

center_box = CenterBox(*frame_buffer.size, w_center=0.1, h_center=0.2, h_offset=0.2)

canny = Canny()
small_filtering = SFiltering(10)

while frame_buffer.running():
    frame = frame_buffer.pop()
    if frame is not None:
        _, center = canny.process_frame(frame)

        if center is not None:
            small_filtering.add(center)

        damped_center = small_filtering.get_point()
        if damped_center is not None:
            if not center_box.intersects(damped_center):
                x, y = center_box.flight(damped_center)

                # frame_buffer.kill()



                print(f'x: {x}, y: {y}')

                # x, y = center_box.flight(damped_center)
                #
                # if x < 0:
                #     print(f"MOVE X DOWN: {x}")
                # if x > 0:
                #     print(f"MOVE X UP: {x}")
                # if y < 0:
                #     print(f"MOVE Y LEFT: {y}")
                # if y > 0:
                #     print(f"MOVE Y RIGHT: {y}")

            damped_center.render(frame)
            center_box.render(frame, damped_center)

        show(frame, fps=True, fps_target=10, wait=1)
# cv2.arrowedLine(image, (0, 0), (int(self.x - 3), int(self.y - 3)), (0, 0, 255), 5)
