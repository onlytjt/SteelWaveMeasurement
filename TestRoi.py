#!/usr/bin/python
# -*- coding:utf-8 -*-

import Camera
from pymba import *
import cv2
import ImageProcessing

def main():
    ci = Camera.CameraInterface()
    ci.openCamera()
    ci.setAttribute(mode="Continuous")
    img = ci.getFirstFrame()
    ip = ImageProcessing.ImageProcessing(img)
    ip.doHoughTrans()
    print "ip.C:", ip.C

    ci.setRoi(250, ip.C-125)
    ci.startCapture()
    while True:
        ci.getOneFrame()
        cv2.imshow("test", ci.img)
        k = cv2.waitKey(1)
        if k == 0x1b:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()