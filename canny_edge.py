import glob
import json

import cv2
import numpy as np

from libs import clear_folder, make_video, line_intersection
from save_the_frames import KMeans

files = glob.glob('./video/*')

output = './output/'

frames = {}

for file in files:
    clear_folder(output)
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()

    height, width, _ = image.shape

    count = 0

    video_images = []

    kmeans = KMeans()

    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 180)
        lineoutputs = []
        points = []

        if lines is not None:
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
                    lineoutputs.append([[x1, y1], [x2, y2]])

                    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for idx1, line1 in enumerate(lineoutputs):
            for idx2, line2 in enumerate(lineoutputs):
                if idx1 == idx2:
                    continue
                try:
                    x, y = line_intersection(line1, line2)

                    if 0 < x < width and 0 < y < height:
                        points.append([x, y])
                        cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
                except Exception:
                    pass

        if len(points) > 0:
            x, y = kmeans.get_kmeans(points)

            cv2.circle(
                image,
                (
                    x, y
                ), 10, (0, 255, 0), -1
            )

        filename = "{}{:06d}_frame.jpg".format(output, count)
        video_images.append(filename)

        cv2.imwrite(filename, image)

        success, image = vidcap.read()

        count += 1

    make_video(video_images, f'./test.mp4')
    clear_folder(output)

    with open(f'frames.json', 'w') as f:
        json.dump(frames, f, indent=4)

    exit(1)
