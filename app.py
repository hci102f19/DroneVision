import glob
import time

import cv2

from libs import clear_folder, done, make_video
from model.Canny import Canny
from model.CoordinateDampner import CoordinateDampner

in_folder = './video/'
out_folder = './output/'

files = glob.glob(f'{in_folder}*.mp4')

coordinate_dampner = CoordinateDampner(2)

o_count = 1
for file in files:
    video_files = []
    clear_folder(out_folder)

    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()

    count = 0
    times = []
    while success:
        start = time.time()

        canny = Canny(image)

        canny.process_frame()
        stop = time.time()

        times.append(stop - start)

        # canny.render(image)

        point = canny.get_center()

        if point is not None and point.is_valid():
            cv2.circle(image, (point.x, point.y), 5, (0, 0, 255), -1)
            coordinate_dampner.enqueue(point)

        d_point = coordinate_dampner.point()
        cv2.circle(image, (d_point.x, d_point.y), 3, (255, 255, 0), -1)

        filename = f'{out_folder}/frame_{count}.jpg'
        cv2.imwrite(filename, image)
        video_files.append(filename)

        success, image = vidcap.read()
        count += 1

    make_video(video_files, f'./output_{o_count}.mp4')
    o_count += 1
done()
