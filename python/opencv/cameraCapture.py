#!/usr/bin/env python

"""
OpenCV highgui API

"""

import cv
import sys

def camera_capture():

    # /dev/video0
    c = cv.CaptureFromCAM(0)
    #assert type(c) ==  "cv.Capture"

    # or use QueryFrame. It's the same
    cv.GrabFrame(c)
    image = cv.RetrieveFrame(c)
    #image = cv.QueryFrame(c)
    assert image != None

    dst = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_16S, 3)
    #im = cv.CloneImage(image)
    laplace = cv.Laplace(image, dst)
    cv.SaveImage("my-camera.png", dst)

    print cv.GetCaptureProperty(c, cv.CV_CAP_PROP_FRAME_HEIGHT)

if __name__ == "__main__":


    camera_capture()

