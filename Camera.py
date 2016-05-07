#!/usr/bin/python
# -*- coding:utf-8 -*-

import cv2
import numpy as np
import time
from pymba import *
from ImageProcessing import *
import datetime

# CameraInterface类使用说明:
# 首先调用initCamera()函数打开vimba，并获取相机句柄
# initAttribute()对相机参数进行设置，包括：采集模式，ROI
# getOneFrame()采集一副图像，以ndarray形式return，并存在self.imgData

class CameraInterface:
    def __init__(self):
        self.WIDTH = 2048
        self.HEIGHT = 1088
        self.cntValidFrame = 0
        self.cntDropFrame = []

    def openCamera(self):
        vimba = Vimba()
        vimba.startup()  # 启用vimba驱动程序,获取vimba的句柄
        print "Vimba run successfully! Version: ", vimba.getVersion()  # 打印当前使用vimba版本信息
        system = vimba.getSystem()
        system.runFeatureCommand("GeVDiscoveryAllOnce")  # enabling discovery for GigE cameras
        time.sleep(0.2)
        cameraIds = vimba.getCameraIds()
        print "Available cameras: ", cameraIds  # 列出所有可用相机的ID
        self.camera = vimba.getCamera(cameraIds[0])  # 得到相机的相机句柄，用于后续各种操作
        self.camera.openCamera()
        print "Camera: ", cameraIds, "has opened successfully!"

    def setAttribute(self, mode="SingleFrame"):
        try:  # 设置千兆网的传输速率
            print "GevSCPSPacketSize:", self.camera.GevSCPSPacketSize
            print "StreamBytesPerSecond:", self.camera.StreamBytesPerSecond
            self.camera.StreamBytesPerSecond = 100000000
        except:
            print "当前相机不是千兆网"

        print "CameraFeature: ", self.camera.AcquisitionMode  # 列出相机当前设置
        self.camera.AcquisitionMode = mode  # 设置相机的帧采集模式
        # self.camera.AcquisitionMode = 'SingleFrame'  # 设置相机的帧采集模式
        # self.camera.AcquisitionMode = 'Continuous'  # 设置相机的帧采集模式

    def startCapture(self):
        self.camera.startCapture()
        self.timeStartCapture = datetime.datetime.now()


    def setRoiToDefault(self):  # 从区域较小图像设置到较大图像
        offsetY = VimbaFeature("OffsetY", self.camera._handle)
        print "offsetY:", offsetY._getIntFeature()
        offsetY._setIntFeature(0)
        height = VimbaFeature("Height", self.camera._handle)
        print "Height:", height._getIntFeature()
        height._setIntFeature(1088)
        self.frame = self.camera.getFrame()
        self.frame.announceFrame()

    def setRoi(self, roirange, offset):  # 从区域较大图像设置到较小图像
        height = VimbaFeature("Height", self.camera._handle)
        print "Height:", height._getIntFeature()
        height._setIntFeature(roirange)
        offsetY = VimbaFeature("OffsetY", self.camera._handle)
        print "offsetY:", offsetY._getIntFeature()
        offsetY._setIntFeature(offset)
        self.frame = self.camera.getFrame()
        self.frame.announceFrame()

    def getFirstFrame(self):
        self.setRoiToDefault()
        self.camera.startCapture()
        self.getOneFrame()
        self.camera.endCapture()
        self.camera.revokeAllFrames()
        return self.img

    def getOneFrame(self):
        try:
            self.frame.queueFrameCapture()
            isCaptured = True
        except:
            # self.cntDropFrame.append(self.cntValidFrame)
            isCaptured = False

        self.camera.runFeatureCommand('AcquisitionStart')
        self.camera.runFeatureCommand('AcquisitionStop')
        self.frame.waitFrameCapture(1000)
        imgData = self.frame.getBufferByteData()
        if isCaptured:
            # self.cntValidFrame += 1
            moreUsefulImgData = np.ndarray(buffer=imgData,
                                       dtype=np.uint8,
                                       shape=(self.frame.height, self.frame.width))  # numpy的ndarray进行方便进行处理
            self.img = moreUsefulImgData


    def closeCamera(self):
        self.camera.endCapture()
        self.camera.revokeAllFrames()
        self.camera.closeCamera()
        self.timeStopCapture = datetime.datetime.now()
