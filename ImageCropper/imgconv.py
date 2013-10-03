#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '0.1'

import os, sys
from pgmagick import Image

INPUT_DIR = os.getcwd() + "\\Input\\"
OUTPUT_DIR = os.getcwd() + "\\Output\\"


if __name__ == '__main__':
# check directory exist
    if not os.path.isdir(INPUT_DIR[:-1]):
        print("Error: No Input directory specified.")
        sys.exit(2)
    if not os.path.isdir(OUTPUT_DIR[:-1]):
        os.makedirs(OUTPUT_DIR[:-1])

    # convert
    i = 0
    for filename in os.listdir(INPUT_DIR):
        print filename
        img = Image(os.path.join(INPUT_DIR, filename))

        temp_str = "%03d" % i
        img.write(OUTPUT_DIR + temp_str + ".png",)
        i = i + 1

    print "FINISH!"