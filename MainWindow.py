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
        self.realWireDiameter = 110.0
        self.waveHeightList = []
        self.waveLengthList = []
        self.wireDiameterList = []

    def adjustUI(self):
        self.setWindowTitle("Bao Steel")
        self.setWindowIcon(QIcon("./res/bilibili.jpg"))  # 设置图标
        pe = QPalette()  # 设置标题的字体，字号，颜色
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 20, QFont.Bold))

        self.initTable()
        self.initProcessBar()

    def initTable(self):
        self.tableModel = QStandardItemModel()
        self.tableModel.setColumnCount(10)
        listTableHeader = [u"日期", u"盘号", u"车台号", u"类型",
                           u"大波波高", u"小波波高", u"大波波长", u"小波波长",
                           u"行动", u"备注"]
        for i in range(10):
            self.tableModel.setHeaderData(i, Qt.Horizontal, QString(listTableHeader[i]))
        self.table.setModel(self.tableModel)
        for i in range(5):
            for j in range(10):
                self.tableModel.setItem(i, j, QStandardItem(""))

    def initProcessBar(self):
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
        oriImg = self.ci.getOneFrame()  # 采集图像
        self.displayOriImg(oriImg)  # 显示原始图像
        self.displayEdgeImg(oriImg)  # 显示边缘图像

    def displayOriImg(self, oriImg):  # 原始图像区域的处理
        img = q2n.gray2qimage(oriImg)
        img = img.scaled(981, 120, Qt.KeepAspectRatio)  # 从1226*150以0.8倍变换得来
        self.label_image.setPixmap(QPixmap.fromImage(img))

    def displayEdgeImg(self, oriImg):  # 边缘显示区域的处理
        ip = ImageProcessing.ImageProcessing(oriImg)
        if (not self.isMeasuring) or (not ip.doHoughTrans()):  # 检测图像没有钢丝。或系统刚启动，没在测量时
            # 边缘显示区域也显示原始图像
            img = q2n.gray2qimage(oriImg)
            img = img.scaled(981, 120, Qt.KeepAspectRatio)
        else:  # 有钢丝情况，显示Canny算子计算后的边缘
            img = cv2.resize(ip.cannyImg, (981, 120), cv2.INTER_NEAREST)
            img = q2n.gray2qimage(img)  # 此方法显示会将边缘放大，但实际处理的数据不会改变
        self.label_canny.setPixmap(QPixmap.fromImage(img))  # 在边缘显示区域写入图像

        waveHeight, waveLength, wireDiameter = ip.getWaveHeightBySin()
        # 通过配合钢丝直径的值，得出计算结果。首先显示钢丝直径的像素值
        self.lineEdit_5.setText(QString(str(wireDiameter)))
        self.edit_big_height.setText(QString(str(waveHeight)))  # 实时显示波高像素值和直径像素值
        self.edit_big_length.setText(QString(str(waveLength)))

        self.cntImgMeasuring += 1
        self.progressBar.setValue(self.cntImgMeasuring)  # 更新进度条当前进度
        self.waveHeightList.append(waveHeight)
        self.waveLengthList.append(waveLength)
        self.wireDiameterList.append(wireDiameter)  # 计数器和数据记录

        if self.cntImgMeasuring > self.rotatePeriod:  # 测量时间大于设定值
            self.completeMeasure()  # 测量完成进行相应得清零和整理工作

    def onClickedBtnAutoTest(self):
        # 为满足多次重复测量情况，在每次测量前，需要对一些record进行清零操作
        self.waveHeightList = []  # 波高record清零
        self.waveLengthList = []  # 波长record清零
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

    def dealWaveDataFromList(self, data):
        indexOfPeakInData = []  # 用于保存数据中找到的极值的索引值
        # 首先做前后向查分，找到一些极值
        for index, value in enumerate(data):
            right1 = 0 if (index+1)>self.rotatePeriod else index+1  # 保证下标的循环
            right2 = 1 if (index+2)>self.rotatePeriod else index+2
            if value>=data[index-1] and value>=data[index-2] and value>=data[right1] and value>=data[right2]:
                if index != 0 and index != self.rotatePeriod:
                    indexOfPeakInData.append(index)
        # 去除极值中索引相邻，值重复的项
        for i, index in enumerate(indexOfPeakInData):
            print index, ": ", data[index]
            if index-1 == indexOfPeakInData[i-1] and data[index] == data[index-1]:
                del indexOfPeakInData[i]  # 保留较小的下标值

        # 暂时测试使用两个大波之间的坐标直接得到小波波高，20160126
        # 找寻和小波所在位置的下标，以计算波长
        if self.waveHeightList[indexOfPeakInData[0]] < self.waveHeightList[indexOfPeakInData[1]]:
            smallWaveLengthIndex = indexOfPeakInData[0]
            bigWaveLengthIndex = indexOfPeakInData[1]
            print "中点小波测量法：", self.waveHeightList[(indexOfPeakInData[1]+indexOfPeakInData[3])/2], ", ", \
                self.waveHeightList[(indexOfPeakInData[1]+indexOfPeakInData[3])/2]*110.0/np.array(self.wireDiameterList).mean()
        else:
            smallWaveLengthIndex = indexOfPeakInData[1]
            bigWaveLengthIndex = indexOfPeakInData[0]
            print "中点小波测量法：", self.waveHeightList[(indexOfPeakInData[0]+indexOfPeakInData[2])/2], ", ", \
                self.waveHeightList[(indexOfPeakInData[0]+indexOfPeakInData[2])/2]*110.0/np.array(self.wireDiameterList).mean()

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
        return smallWaveHeight, bigWaveHeight, smallWaveLengthIndex, bigWaveLengthIndex

    def completeMeasure(self):
        self.btn_auto_test.setText(u"自动测量")
        self.btn_auto_test.setDisabled(False)  # 恢复测量Btn状态
        self.cntImgMeasuring = 0  # 清零测量计时计数
        self.isMeasuring = False  # 设置状态标志位，不在测量中，不进行图像和数据处理

        self.waveHeightList = ImageProcessing.ImageProcessing.smoothFilter(self.waveHeightList)  # 三点平滑滤波
        smallWaveHeightPixel, bigWaveHeightPixel, \
        smallWaveLengthIndex, bigWaveLengthIndex = self.dealWaveDataFromList(self.waveHeightList)

        aveWireDiameterPixel = float("%0.2f" % np.array(self.wireDiameterList).mean())
        smallWaveHeight = self.realWireDiameter/aveWireDiameterPixel * smallWaveHeightPixel
        bigWaveHeight = self.realWireDiameter/aveWireDiameterPixel * bigWaveHeightPixel
        smallWaveLength = self.realWireDiameter/aveWireDiameterPixel * self.waveLengthList[smallWaveLengthIndex]
        bigWaveLength = self.realWireDiameter/aveWireDiameterPixel * self.waveLengthList[bigWaveLengthIndex]

        strEditBigHeight = str(bigWaveHeightPixel) + ",  " + str(float("%0.1f" % bigWaveHeight))
        strEditSmallHeight = str(smallWaveHeightPixel) + ",  " + str(float("%0.1f" % smallWaveHeight))

        self.edit_small_height.setText(QString(str(strEditSmallHeight)))
        self.edit_big_height.setText(QString(str(strEditBigHeight)))
        self.edit_small_length.setText(QString(str(float("%0.1f" % smallWaveLength))))
        self.edit_big_length.setText(QString(str(float("%0.1f" % bigWaveLength))))
        self.lineEdit_5.setText(QString(str(np.array(self.wireDiameterList).mean())))  # 显示直径平均值
        plt.plot(self.waveHeightList)
        plt.show()

