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
        self.btn_savefile.clicked.connect(lambda :self.onClickedBtnSaveFile())


    def adjustUI(self):
        self.setWindowTitle("Bao Steel")
        self.setWindowIcon(QIcon("./res/bilibili.jpg"))
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 20, QFont.Bold))

    def initCamera(self):
        self.ROIRANGE = 300
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

        # 进行图像处理并显示canny边缘图像
        ip = ImageProcessing.ImageProcessing(oriImg)
        if not ip.doHoughTrans():  # 经过霍夫变换，检测图像没有钢丝情况
            self.label_canny.setPixmap(QPixmap.fromImage(img))
            return
        else:  # 有钢丝情况，首先显示Canny算子的边缘
            # img = q2n.gray2qimage(ip.cannyImg)
            # img = img.scaled(1226, self.ROIRANGE/2, Qt.KeepAspectRatio)  # 此方法显示，会造成边缘断续
            img = cv2.resize(ip.cannyImg, (1226, self.ROIRANGE), cv2.INTER_NEAREST)
            img = q2n.gray2qimage(img)  # 此方法显示会将边缘放大，但实际处理的数据不会改变
            self.label_canny.setPixmap(QPixmap.fromImage(img))

        top, bottom = ip.getP2PByHough()  # 获取波峰波谷像素值
        # 进行精度控制，格式转换
        top = float("%0.1f" % top)
        bottom = float("%0.1f" % bottom)
        pp = 8000.0/2056.0 * (top - bottom)
        pp = float("%0.2f" % pp)
        strDis = "top:" + str(top) + ". bottom:" + str(bottom) + ". P-P:" + str(top-bottom)
        self.edit_big_height.setText(QString(strDis))

        topSin, bottomSin, width = ip.doSinFit()
        topSin = float("%0.1f" % topSin)
        bottomSin = float("%0.1f" % bottomSin)
        strDisSin = "top:" + str(topSin) + ". bottom:" + str(bottomSin) + ". P-P:" + str(topSin-bottomSin)
        self.edit_big_length.setText(QString(strDisSin))

        self.edit_small_height.setText(QString(str(width)))

    def onClickedBtnAutoTest(self):
        # self.btn_auto_test.setText(u"正在测量中。请稍候。。")
        self.timerShowImage.start(50)


    def onClickedBtnStartSystem(self):
        self.initCamera()
        self.timerShowImage.start(50)

    def onClickedBtnCloseSystem(self):
        self.timerShowImage.stop()
        print "Timer timerShowImage has been closed"
        self.ci.closeCamera()
        print "Camera has been closed"
        QCoreApplication.instance().quit()

    def onClickedBtnSaveFile(self):
        self.timerShowImage.stop()
