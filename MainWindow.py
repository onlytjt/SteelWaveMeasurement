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



class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)
        self.adjustUI()

        self.timerShowImage = QTimer()
        self.timerShowImage.timeout.connect(lambda: self.onTimerShowImage())
        self.btn_auto_test.clicked.connect(lambda: self.onClickedBtnAutoTest())
        self.btn_start_system.clicked.connect(lambda: self.onClickedBtnStartSystem())
        self.btn_close_system.clicked.connect(lambda: self.onClickedBtnCloseSystem())


    def adjustUI(self):
        self.setWindowTitle("Bao Steel")
        self.setWindowIcon(QIcon("./res/bilibili.jpg"))
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 20, QFont.Bold))

    def initCamera(self):
        ROIRANGE = 200
        self.ci = Camera.CameraInterface()  # 获取界面中的相机接口
        self.ci.initCamera()
        self.ci.initAttribute()
        self.ci.getOneFrame()
        ip = ImageProcessing.ImageProcessing(self.ci.imgData)
        ip.doHoughTrans()
        self.ci.setROI(roiRange=ROIRANGE, offset=ip.C-ROIRANGE/2)


    def onTimerShowImage(self):
        # 采集图像
        self.ci.getOneFrame()
        # 显示原始图像
        img = q2n.gray2qimage(self.ci.imgData)
        img = img.scaled(1226, 100, Qt.KeepAspectRatio)
        self.label_image.setPixmap(QPixmap.fromImage(img))
        # 进行图像处理并显示canny边缘图像
        ip = ImageProcessing.ImageProcessing(self.ci.imgData)
        img = cv2.resize(ip.cannyImg, (1226, 100), cv2.INTER_AREA)
        img = q2n.gray2qimage(img)
        self.label_canny.setPixmap(QPixmap.fromImage(img))
        (top, bottom) = ip.getP2PByHough()

        # 进行精度控制，格式转换
        top = float("%0.1f" % top)
        bottom = float("%0.1f" % bottom)
        pp = 4000/2056 * (top - bottom)
        pp = float("%0.2f" % pp)
        strDis = "top:" + str(top) + ". bottom:" + str(bottom) + ". And P-P:" + str(top-bottom)
        strDis = strDis + ". And result is:" + str(pp)
        self.edit_big_height.setText(QString(strDis))

    def onClickedBtnAutoTest(self):
        self.btn_auto_test.setText(u"正在测量中。。。")
        inputImg = cv2.imread("./res/21.bmp", 0)
        img = q2n.gray2qimage(inputImg)
        img = img.scaled(400, 300, Qt.KeepAspectRatio)
        self.label_image.setPixmap(QPixmap.fromImage(img))

        ip = ImageProcessing.ImageProcessing(inputImg)
        img = cv2.resize(ip.cannyImg, (800, 600), cv2.INTER_NEAREST)
        img = q2n.gray2qimage(img)
        self.label_canny.setPixmap(QPixmap.fromImage(img))


    def onClickedBtnStartSystem(self):
        self.initCamera()
        self.timerShowImage.start(50)

    def onClickedBtnCloseSystem(self):
        self.timerShowImage.stop()
        print "Timer timerShowImage has been closed"
        self.ci.closeCamera()
        print "Camera has been closed"
        QCoreApplication.instance().quit()
