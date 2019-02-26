import glob

import cv2

from model.Canny import Canny

in_folder = './output/'
out_folder = './output2/'

files = glob.glob('./output/*.jpg')


for file in files:
    image = cv2.imread(file)
    canny = Canny(image)

    canny.process_frame()
