#!/usr/bin/python
# -*- coding:utf-8 -*-

import cv2
import numpy as np
import time
from pymba import *
from ImageProcessing import *

# CameraInterface类使用说明:
# 首先调用initCamera()函数打开vimba，并获取相机句柄
# initAttribute()对相机参数进行设置，包括：采集模式，ROI
# getOneFrame()采集一副图像，以ndarray形式return，并存在self.imgData

class CameraInterface:
    def __init__(self):
        self.WIDTH = 2452
        self.HEIGHT = 2056

    def initCamera(self):
        self.vimba = Vimba()
        self.vimba.startup()  # 启用vimba驱动程序,获取vimba的句柄
        print "Vimba run successfully! Version: ", self.vimba.getVersion()  # 打印当前使用vimba版本信息
        system = self.vimba.getSystem()
        system.runFeatureCommand("GeVDiscoveryAllOnce")  # enabling discovery for GigE cameras
        time.sleep(0.2)
        cameraIds = self.vimba.getCameraIds()
        print "Available cameras: ", cameraIds  # 列出所有可用相机的ID
        self.camera = self.vimba.getCamera(cameraIds[0])  # 得到相机的相机句柄，用于后续各种操作
        self.camera.openCamera()
        print "Camera: ", cameraIds, "has opened successfully!"

    def initAttribute(self):
        print "CameraFeature: ", self.camera.AcquisitionMode  # 列出相机当前设置
        # print self.camera._handle._dist_
        self.camera.AcquisitionMode = 'SingleFrame'  # 设置相机的帧采集模式
        # self.camera.AcquisitionMode = 'Continuous'  # 设置相机的帧采集模式

        # 使用G223时，由于帧率足够，不对相机设置ROI，获取整幅图像后剪裁
        # offsetY = VimbaFeature("OffsetY", self.camera._handle)
        # offsetY._setIntFeature(0)
        # height = VimbaFeature("Height", self.camera._handle)
        # height._setIntFeature(1088)  # 每次重启相机都将设置回复为默认值

        self.frame0 = self.camera.getFrame()
        self.frame1 = self.camera.getFrame()
        self.frame0.announceFrame()  # 为frame声明内存

    def setROI(self, roiRange=1088, offset=0):
        offsetY = VimbaFeature("OffsetY", self.camera._handle)
        offsetY._setIntFeature(offset)
        height = VimbaFeature("Height", self.camera._handle)
        height._setIntFeature(roiRange)
        self.frame0 = self.camera.getFrame()
        self.frame0.announceFrame()  # 为frame声明内存

    def getOneFrame(self):
        self.camera.startCapture()
        self.frame0.queueFrameCapture()
        self.camera.runFeatureCommand('AcquisitionStart')
        self.camera.runFeatureCommand('AcquisitionStop')
        self.frame0.waitFrameCapture()
        # imgData = self.frame0.getBufferByteData()
        moreUsefulImgData = np.ndarray(buffer=self.frame0.getBufferByteData(),
                                   dtype=np.uint8,
                                   shape=(self.frame0.height, self.frame0.width))  # numpy的ndarray进行方便进行处理
        # print "moreUsefulImgData shape:", moreUsefulImgData.shape
        self.camera.endCapture()
        self.camera.revokeAllFrames()  # 获取图像完毕后，清理内存
        self.imgData = moreUsefulImgData
        return moreUsefulImgData

    def closeCamera(self):
        self.vimba.shutdown()

def main():
    ROIRANGE = 300
    ci = CameraInterface()
    ci.initCamera()
    ci.initAttribute()
    testImg = ci.getOneFrame()
    ip = ImageProcessing(testImg)
    ip.doHoughTrans()
    ci.setROI(roiRange=ROIRANGE, offset=ip.C-ROIRANGE/2)
    while True:
        img = ci.getOneFrame()
        ip1 = ImageProcessing(img)
        cv2.imshow("ori", img)
        cv2.imshow("canny", ip1.cannyImg)
        cv2.imshow("binary", ip1.binaryBlurImg)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

# while True:
#         ins.captureFrame()
#         ins.showImage()
#         if cv2.waitKey(1) == 27: # press esc to quit
#             break
#     ins.endShow()