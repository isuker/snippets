#!/usr/bin/env python

"""
OpenCV highgui API

"""

import cv
import sys

def show_image():

    image_filename = sys.argv[1]

    # load this image
    image = cv.LoadImage(image_filename)

    # create one window and show it!
    #win = cv.NamedWindow("myWin", flags=cv.CV_WINDOW_AUTOSIZE)
    cv.ShowImage("myWin", image)

    # don't forget this line: show image 2 second
    cv.WaitKey(2000)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "usage: %s image-filename" %sys.argv[0]
        sys.exit(1)

    show_image()
