import glob

import cv2

from libs import clear_folder, make_video
from rectification import compute_edgelets, ransac_vanishing_point, reestimate_model

files = glob.glob('./video/*')

output = './output/'

sigma = 3

for file in files:
    clear_folder(output)
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()

    height, width, _ = image.shape

    count = 0

    video_images = []

    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edgelets1 = compute_edgelets(gray)
        vp1 = ransac_vanishing_point(edgelets1, num_ransac_iter=2000, threshold_inlier=5)
        vp1 = reestimate_model(vp1, edgelets1, threshold_reestimate=5)

        x, y, _ = vp1

        cv2.circle(image, (int(round(x, 0)), int(round(y, 0))), 10, (255, 0, 0), -1)

        filename = "{}{:06d}_frame.jpg".format(output, count)
        video_images.append(filename)

        cv2.imwrite(filename, image)
        success, image = vidcap.read()
        count += 1

    make_video(video_images, f'./test.mp4')
    exit(1)
