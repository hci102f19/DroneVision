import glob
import time

import cv2

from libs import clear_folder, make_video, done
from model.Canny import Canny

in_folder = './video/'
out_folder = './output/'

files = glob.glob(f'{in_folder}*.mp4')

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
        print(stop - start)

        canny.render(image)

        filename = f'{out_folder}/frame_{count}.jpg'
        cv2.imwrite(filename, image)
        video_files.append(filename)

        success, image = vidcap.read()
        count += 1

    make_video(video_files, f'./output_{o_count}.mp4')
    print(sum(times) / len(times))
    o_count += 1
done()
