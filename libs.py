import glob
import os
from time import time

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


def done(txt="DONE"):
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()


fps_timer = time()


def write_text(image, text, top, left, **kwargs):
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = kwargs.get('font', 1.5)
    color = kwargs.get('color', (255, 255, 255))
    bg_color = kwargs.get('bg_color', (255, 255, 255))

    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]

    text_offset_x = top
    text_offset_y = text_height + left

    box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width - 2, text_offset_y - text_height - 2))
    cv2.rectangle(image, box_coords[0], box_coords[1], bg_color, cv2.FILLED)

    cv2.putText(image, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=color, thickness=1)


def show(image, **kwargs):
    if len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    if kwargs.get('fps', False):

        global fps_timer
        now = time()
        diff = round(now - fps_timer, 2)
        fps_timer = now

        if diff > 0:
            fps_nbr = round(1 / diff, 1)
        else:
            fps_nbr = 'inf.'
        fps_ = str(fps_nbr)

        if kwargs.get('fps_target', None) is not None:
            if fps_nbr == 'inf' or kwargs.get('fps_target', 0) < fps_nbr:
                write_text(image, fps_, 1, 2, color=(0, 255, 0))
            else:
                write_text(image, fps_, 1, 2, color=(0, 0, 255))
        else:
            write_text(image, fps_, 1, 2, color=(0, 0, 0))

    cv2.imshow('frame', image)
    return cv2.waitKey(kwargs.get('wait', 1))
