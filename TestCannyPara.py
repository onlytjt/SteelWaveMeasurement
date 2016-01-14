#!/usr/bin/python
# -*- coding:utf-8 -*-

import cv2
import numpy as np

oriImg = cv2.imread("./res/oriBad.png", 0)
cv2.imshow("origin", oriImg)

blurImg = cv2.GaussianBlur(oriImg, (3, 3), 0)
cv2.imshow("blurImg", blurImg)

ret, binaryBlurImg = cv2.threshold(blurImg, 125, 255, cv2.THRESH_BINARY)
ret, binaryImg = cv2.threshold(oriImg, 125, 255, cv2.THRESH_BINARY)
cv2.imshow("binaryBlurImg", binaryBlurImg)
cv2.imshow("binaryImg", binaryImg)
cv2.waitKey(0)
