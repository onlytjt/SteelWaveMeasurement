#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import cv2
import Camera # write by tjt

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MyUI import Ui_MainWindow # write by tjt
import qimage2ndarray as q2n
import ImageProcessing
import numpy as np
import datetime
import matplotlib.pyplot as plt
import threading



class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)
        self.initVariable()
        self.adjustUI()

        self.timerShowImage = QTimer()
        self.timerShowImage.timeout.connect(lambda: self.onTimerShowImage())
        self.btn_auto_test.clicked.connect(lambda: self.onClickedBtnAutoTest())
        self.btn_start_system.clicked.connect(lambda: self.onClickedBtnStartSystem())
        self.btn_close_system.clicked.connect(lambda: self.onClickedBtnCloseSystem())
        self.btn_savefile.clicked.connect(lambda: self.onClickedBtnSaveFile())

    def initVariable(self):
        self.isMeasuring = False
        self.cntImgMeasuring = 0
        self.ROIRANGE = 300
        self.rotatePeriod = 127
        self.waveHeightList = []
        self.wireDiameterList = []

    def adjustUI(self):
        self.setWindowTitle("Bao Steel")
        self.setWindowIcon(QIcon("./res/bilibili.jpg"))  # 设置图标
        pe = QPalette()  # 设置标题的字体，字号，颜色
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 20, QFont.Bold))
        self.progressBar.setMinimum(0)  # 初始化进度条相关设置，最大最小值，初始值为0
        self.progressBar.setMaximum(self.rotatePeriod)
        self.progressBar.setValue(0)

    def initCamera(self):
        self.ci = Camera.CameraInterface()  # 获取界面中的相机接口
        self.ci.initCamera()
        self.ci.initAttribute()
        self.ci.getOneFrame()
        ip = ImageProcessing.ImageProcessing(self.ci.imgData)
        if ip.doHoughTrans():
            self.ci.setROI(roiRange=self.ROIRANGE, offset=ip.C-self.ROIRANGE/2)
        else:
            self.ci.setROI(roiRange=self.ROIRANGE)

    def onTimerShowImage(self):
        # 采集图像
        oriImg = self.ci.getOneFrame()
        # 显示原始图像
        img = q2n.gray2qimage(oriImg)
        img = img.scaled(1226, self.ROIRANGE/2, Qt.KeepAspectRatio)
        self.label_image.setPixmap(QPixmap.fromImage(img))
        # 图像处理初始化
        ip = ImageProcessing.ImageProcessing(oriImg)
        if (not self.isMeasuring) or (not ip.doHoughTrans()):  # 检测图像没有钢丝。或系统刚启动，没在测量时
            self.label_canny.setPixmap(QPixmap.fromImage(img))  # 边缘显示区域也显示原始图像
            return
        else:  # 有钢丝情况，显示Canny算子计算后的边缘
            img = cv2.resize(ip.cannyImg, (1226, self.ROIRANGE), cv2.INTER_NEAREST)
            img = q2n.gray2qimage(img)  # 此方法显示会将边缘放大，但实际处理的数据不会改变
            self.label_canny.setPixmap(QPixmap.fromImage(img))

        waveHeight, wireDiameter = ip.getWaveHeightBySin()
        # 通过配合钢丝直径的值，得出计算结果。首先显示钢丝直径的像素值
        self.lineEdit_5.setText(QString(str(wireDiameter)))
        self.edit_big_height.setText(QString(str(waveHeight)))  # 实时显示波高像素值和直径像素值

        self.cntImgMeasuring += 1
        self.progressBar.setValue(self.cntImgMeasuring)
        self.waveHeightList.append(waveHeight)
        self.wireDiameterList.append(wireDiameter)  # 计数器和数据记录

        if self.cntImgMeasuring > self.rotatePeriod:  # 测量时间大于设定值
            self.completeMeasure()  # 测量完成进行相应得清零和整理工作


    def onClickedBtnAutoTest(self):
        # 为满足多次重复测量情况，在每次测量前，需要对一些record进行清零操作
        self.waveHeightList = []  # 波高record清零
        self.wireDiameterList = []  # 钢丝直径清零
        self.edit_small_height.setText("")  # 清空显示残留值
        self.btn_auto_test.setText(u"正在测量中。请稍候。")
        self.btn_auto_test.setDisabled(True)  # 设置按钮无法使用，并改变文字提醒
        self.isMeasuring = True  # 设置工作状态为【正在测量中】

    def onClickedBtnStartSystem(self):
        self.initCamera()
        self.timerShowImage.start(50)
        self.isMeasuring = False

    def onClickedBtnCloseSystem(self):
        self.timerShowImage.stop()
        print "Timer timerShowImage has been closed"
        self.ci.closeCamera()
        print "Camera has been closed"
        QCoreApplication.instance().quit()

    def onClickedBtnSaveFile(self):
        self.timerShowImage.stop()

    def tmpWriteImg(self):
        oriImg = self.ci.getOneFrame()
        img = q2n.gray2qimage(oriImg)
        img = img.scaled(1226, self.ROIRANGE/2, Qt.KeepAspectRatio)
        self.label_image.setPixmap(QPixmap.fromImage(img))
        self.cntImgMeasuring += 1
        cv2.imwrite("./TmpImg/test%i.png" % self.cntImgMeasuring, oriImg)

    def dealWaveDataFromList(self, data):
        indexOfPeakInData = []  # 用于保存数据中找到的极值的索引值
        # 首先做前后向查分，找到一些极值
        for index, value in enumerate(data):
            right1 = 0 if (index+1)>self.rotatePeriod else index+1  # 保证下标的循环
            right2 = 1 if (index+2)>self.rotatePeriod else index+2
            if value>=data[index-1] and value>=data[index-2] and value>=data[right1] and value>=data[right2]:
                indexOfPeakInData.append(index)
        # 去除极值中索引相邻，值重复的项
        for i, index in enumerate(indexOfPeakInData):
            print index, ": ", data[index]
            if index-1 == indexOfPeakInData[i-1] and data[index] == data[index-1]:
                del indexOfPeakInData[i]  # 保留较小的下标值
        peak1 = []; peak2 = []  # 将大波和小波的波高区分开
        for i, index in enumerate(indexOfPeakInData):
            if not i%2:  # 从第0个开始
                peak1.append(data[index])
            else:
                peak2.append(data[index])
        print "peak1: ", peak1
        print "peak2: ", peak2
        smallWaveHeight = min(np.array(peak1).mean(), np.array(peak2).mean())
        bigWaveHeight = max(np.array(peak1).mean(), np.array(peak2).mean())
        return smallWaveHeight, bigWaveHeight

    def completeMeasure(self):
        self.btn_auto_test.setText(u"自动测量")
        self.btn_auto_test.setDisabled(False)  # 恢复测量Btn状态
        self.cntImgMeasuring = 0  # 清零测量计时计数
        self.isMeasuring = False  # 设置状态标志位，不在测量中，不进行图像和数据处理

        smallWaveHeightPixel, bigWaveHeightPixel = self.dealWaveDataFromList(self.waveHeightList)
        aveWireDiameterPixel = float("%0.2f" % np.array(self.wireDiameterList).mean())

        smallWaveHeight = 112.0/aveWireDiameterPixel * smallWaveHeightPixel
        bigWaveHeight = 112.0/aveWireDiameterPixel * bigWaveHeightPixel
        strEditBigHeight = str(bigWaveHeightPixel) + ",  " + str(bigWaveHeight)
        strEditSmallHeight = str(smallWaveHeightPixel) + ",  " + str(smallWaveHeight)

        self.edit_small_height.setText(QString(str(strEditSmallHeight)))
        self.edit_big_height.setText(QString(str(strEditBigHeight)))  # 显示大波波高像素值
        self.lineEdit_5.setText(QString(str(np.array(self.wireDiameterList).mean())))  # 显示直径平均值
        plt.plot(self.waveHeightList)
        plt.show()

