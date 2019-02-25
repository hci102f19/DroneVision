import glob
from os.path import basename

import cv2
import numpy as np

from libs import line_intersection, clear_folder

files = glob.glob('./output/*.jpg')

output = './output2/'

sigma = 0.33
minLineLength = 5
maxLineGap = 10
line_deviation = 0.15

clear_folder(output)


def abs_list(lst):
    return [abs(e) for e in lst]


for file in files:
    image = cv2.imread(file)

    # vidcap = cv2.VideoCapture(file)
    # success, image = vidcap.read()

    height, width, _ = image.shape
    blank_image = np.zeros((height, width, 3), np.uint8)

    count = 0

    video_images = []

    # while success:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    v = np.median(image)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edges = cv2.Canny(gray, lower, upper, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)

    points = []
    k = []

    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)

            direction = [[x1, y1], [x2, y2]]

            x_deviation = min(abs_list([x1, x2])) / max(abs_list([x1, x2]))
            y_deviation = min(abs_list([y1, y2])) / max(abs_list([y1, y2]))

            if 1 - line_deviation < x_deviation or 1 - line_deviation < y_deviation:
                continue

            for k_ in k:
                try:
                    x, y = line_intersection(k_, direction)
                    if 0 < x < width and 0 < y < height:
                        points.append([x, y])
                        cv2.circle(blank_image, (x, y), 5, (255, 0, 0), -1)
                except Exception as f:
                    pass

            k.append(direction)

            cv2.line(blank_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imwrite(f'./{output}/{basename(file)}', blank_image)

    # success, image = vidcap.read()
    # count += 1

    # make_video(video_images, f'./test.mp4')
