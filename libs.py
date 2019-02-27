import glob
import os

import cv2
import pyttsx3


def clear_folder(folder: str):
    for file in glob.glob(f'{folder}/*'):
        os.remove(file)


def make_video(images: list, file: str):
    image_path = images[0]
    frame = cv2.imread(image_path)
    height, width, channels = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(file, fourcc, 20.0, (width, height))

    for image in images:
        image_path = image
        frame = cv2.imread(image_path)

        # for _ in range(3):
        out.write(frame)  # Write out frame to video

    # Release everything if job is finished
    out.release()

    print("The output video is {}".format(file))


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return int(round(x, 0)), int(round(y, 0))


def done():
    engine = pyttsx3.init()
    engine.say('DONE')
    engine.runAndWait()
