import glob

import cv2

from libs import clear_folder

files = glob.glob('./video/*')

output = './output/'

for file in files:
    clear_folder(output)
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()
    count = 0

    video_images = []

    while success:
        filename = "{}{:06d}_frame.jpg".format(output, count)

        cv2.imwrite(filename, image)

        success, image = vidcap.read()

        count += 1
    exit(1)
