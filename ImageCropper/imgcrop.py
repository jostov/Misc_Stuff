#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '0.1'

import os, sys
from PIL import Image

INPUT_DIR = os.getcwd() + "\\Input\\"
OUTPUT_DIR = os.getcwd() + "\\Output\\"


def resizeFromHeight(image, baseheight=800):
    hpercent = (baseheight / float(image.size[1]))
    wsize = int((float(image.size[0]) * float(hpercent)))
    img = image.resize((wsize, baseheight), Image.ANTIALIAS)
    return img


def cropIntoHalf(image):
    box1 = (0, 0, image.size[0] / 2, image.size[1])
    box2 = (image.size[0] / 2, 0, image.size[0], image.size[1])
    img1 = image.crop(box1)
    img2 = image.crop(box2)
    return [img1, img2]


if __name__ == '__main__':
# check directory exist
    if not os.path.isdir(INPUT_DIR[:-1]):
        print("Error: No Input directory specified.")
        sys.exit(2)
    if not os.path.isdir(OUTPUT_DIR[:-1]):
        os.makedirs(OUTPUT_DIR[:-1])

    # scan, resize & crop
    i = 0
    for filename in os.listdir(INPUT_DIR):
        print filename
        img = Image.open(os.path.join(INPUT_DIR, filename))
        img = resizeFromHeight(img)
        imglist = cropIntoHalf(img)
        for index, img_split in enumerate(imglist):
            temp_str = "%03d" % i
            imglist[index].save(OUTPUT_DIR + temp_str + ".jpg", "JPEG")
            # img.save("resized_image.jpg", "JPEG", quality=50)
            i = i + 1

    print "FINISH!"