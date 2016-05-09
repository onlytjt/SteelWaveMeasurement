#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import cv2
import Camera  # write by tjt
import time
import matplotlib.pyplot as plt

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MyUI import Ui_MainWindow  # write by tjt
import qimage2ndarray as q2n
import ImageProcessing
import numpy as np
import time
import csv
import DataProcessing as dp
import ThreeDimension as td



class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
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
        self.btn_show.clicked.connect(lambda: self.onClickedBtnShowMode())
        self.btn_cancel.clicked.connect(lambda: self.onClickedBtnCancel())
        self.btn_focus.clicked.connect(lambda: self.onClickedBtnFocus())

    def initVariable(self):
        self.IMG_WIDTH = 2048
        self.IMG_HEIGHT = 1088
        self.isMeasuring = 0
        self.cntImgMeasuring = 0
        self.ROIRANGE = 250
        self.rotatePeriod = 90  # 旋转一周采集的图像数
        self.realWireDiameter = 110.0
        self.waveHeightList = []
        self.waveLengthList = []
        self.wireDiameterList = []
        self.indexRecordToExcel = -1  # 用来记录需要记录到表格内的数据个数
        self.SMDList = []
        self.SHOW_COUNT = False
        self.username = "test"

    def setUsername(self, username):
        self.username = username


    def adjustUI(self):
        self.setWindowTitle("Shanghai Jiao Tong University")
        self.setWindowIcon(QIcon("./res/sjtu.jpg"))  # 设置图标
        pe = QPalette()  # 设置标题的字体，字号，颜色
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 20, QFont.Bold))
        self.label_wave_height.setAlignment(Qt.AlignCenter)
        self.label_wave_height.setPalette(pe)
        self.label_wave_height.setFont(QFont("Roman times", 20, QFont.Bold))
        self.btn_auto_test.setPalette(pe)
        self.btn_auto_test.setFont(QFont("Roman times", 15, QFont.Bold))

        self.initTable()
        self.initProcessBar()

    def initTable(self):
        self.table.setRowCount(1)
        self.table.setColumnCount(10)
        listTableHeader = [u"日期", u"盘号", u"车台号", u"类型",
                           u"大波波高", u"小波波高", u"大波波长", u"小波波长",
                           u"行动", u"备注"]
        self.table.setHorizontalHeaderLabels(listTableHeader)
        self.table.setColumnWidth(0, 150)  # 设置第一列宽度，使其能够放下日期信息


    def initProcessBar(self):
        self.progressBar.setMinimum(0)  # 初始化进度条相关设置，最大最小值，初始值为0
        self.progressBar.setMaximum(self.rotatePeriod)
        self.progressBar.setValue(0)

    def initCamera(self):
        self.ci = Camera.CameraInterface()  # 获取界面中的相机接口
        self.ci.openCamera()
        self.ci.setAttribute()
        firstFrame = self.ci.getFirstFrame()
        ip = ImageProcessing.ImageProcessing(firstFrame)
        if ip.doHoughTrans():
            self.HOUGH_LINE_Y = ip.C
        else:
            self.HOUGH_LINE_Y = self.IMG_HEIGHT/2

        self.ci.setRoi(self.ROIRANGE, ip.C-self.ROIRANGE/2)
        self.ci.startCapture()

    def onTimerShowImage(self):
        self.ci.getOneFrame()  # 采集图像
        img = self.ci.img
        self.displayOriImg(img)  # 显示原始图像
        self.displayEdgeImg(img)  # 显示边缘图像


    def displayOriImg(self, oriImg):  # 原始图像区域的处理
        img = q2n.gray2qimage(oriImg)
        img = img.scaled(self.IMG_WIDTH/2, self.ROIRANGE/2, Qt.KeepAspectRatio)
        self.label_image.setPixmap(QPixmap.fromImage(img))


    def displayEdgeImg(self, oriImg):  # 边缘显示区域的处理
        if self.isMeasuring == 0:  # 打开系统，但是未选择测量时
            # 边缘显示区域也显示原始图像
            img = q2n.gray2qimage(oriImg)
            img = img.scaled(self.IMG_WIDTH/2, self.ROIRANGE/2, Qt.KeepAspectRatio)
            self.label_canny.setPixmap(QPixmap.fromImage(img))  # 在原始图像显示区域写入图像
            return

        elif self.isMeasuring == 2:  # 仅仅用于演示和显示边缘图像，不对图像进行运算处理
            ip = ImageProcessing.ImageProcessing(oriImg)
            img = cv2.resize(ip.cannyImg, (self.IMG_WIDTH / 2, self.ROIRANGE / 2), cv2.INTER_NEAREST)
            img = q2n.gray2qimage(img)  # 此方法显示会将边缘放大，但实际处理的数据不会改变
            self.label_canny.setPixmap(QPixmap.fromImage(img))  # 在边缘显示区域写入图像
            return

        '''单击【自动测量按钮后】 self.isMeasuring==1的情况'''
        ip = ImageProcessing.ImageProcessing(oriImg)
        topCurve, bottomCurve = dp.getEdgeList(ip.cannyImg)
        # waveHeightByPeak, waveLengthByPeak = dp.getWaveParaByPeak(topCurve, bottomCurve)
        waveHeightBySin, waveLengthBySin = dp.getWaveParaBySin(topCurve, bottomCurve)

        # 显示钢丝波高的值
        waveShow = "%0.1f" % (waveHeightBySin * 6.6188 - 7.356)
        waveShow += "um"
        self.label_wave_height.setText(QString(str(waveShow)))
        img = cv2.resize(ip.cannyImg, (self.IMG_WIDTH / 2, self.ROIRANGE / 2), cv2.INTER_NEAREST)
        img = q2n.gray2qimage(img)  # 此方法显示会将边缘放大，但实际处理的数据不会改变
        self.label_canny.setPixmap(QPixmap.fromImage(img))  # 在边缘显示区域写入图像

        self.cntImgMeasuring += 1
        self.progressBar.setValue(self.cntImgMeasuring)  # 更新进度条当前进度
        self.waveHeightList.append(waveHeightBySin)
        self.waveLengthList.append(waveLengthBySin)  # 计数器和数据记录

        if self.cntImgMeasuring > self.rotatePeriod:  # 测量时间大于设定值
            self.completeMeasure()  # 测量完成进行相应得清零和整理工作


    def getCurrentTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def completeMeasure(self):
        self.onClickedBtnCancel()
        self.indexRecordToExcel += 1
        # self.recordWaveHeight()  # 将所有波高、波长值记录，为后面标定和论文
        # self.recordWaveLength()
        waveHeightFFT = dp.fftFilter(self.waveHeightList)
        bigWaveHeight, smallWaveHeight, bigWaveLength, smallWaveLength, peakBigWave, peakSmallWave \
            = td.buildWaveModel(self.waveHeightList, self.waveLengthList)
        self.updateTableWidget(bigWaveHeight, smallWaveHeight, bigWaveLength, smallWaveLength)

        p1 = plt.subplot(211)
        p1.scatter(range(len(self.waveHeightList)), self.waveHeightList, s=1, c="b")
        p1.scatter(peakBigWave[:, 0], peakBigWave[:, 1], s=100, c="r", marker="v")
        p1.scatter(peakSmallWave[:, 0], peakSmallWave[:, 1], s=100, c="g", marker="v")
        p1.plot(self.waveHeightList, "r")
        p2 = plt.subplot(212)
        p2.scatter(range(len(self.waveLengthList)), self.waveLengthList, s=1, c="b")
        p2.plot(self.waveLengthList, "r")
        plt.show()

    def updateTableWidget(self, bigWaveHeight, smallWaveHeight, bigWaveLength, smallWaveLength):
        self.table.insertRow(self.indexRecordToExcel+1)  # 添加新的一行
        self.table.setItem(self.indexRecordToExcel, 0, QTableWidgetItem(self.getCurrentTime()))  # 设置时间
        self.table.setItem(self.indexRecordToExcel, 4, QTableWidgetItem(str(bigWaveHeight)))
        self.table.setItem(self.indexRecordToExcel, 5, QTableWidgetItem(str(smallWaveHeight)))
        self.table.setItem(self.indexRecordToExcel, 6, QTableWidgetItem(str(bigWaveLength)))
        self.table.setItem(self.indexRecordToExcel, 7, QTableWidgetItem(str(smallWaveLength)))
        self.table.setItem(self.indexRecordToExcel, 9, QTableWidgetItem(self.username))

        comboType = QComboBox()
        comboType.addItem(u"调车")
        comboType.addItem(u"放行")
        comboType.addItem(u"满盘")
        comboType.addItem(u"检测")
        self.table.setCellWidget(self.indexRecordToExcel, 3, comboType)

    def recordWaveHeight(self):
        f = open("./img_tmp/height.txt", "a")
        for ele in self.waveHeightList:
            f.write(str(ele) + "\n")
        f.close()

    def recordWaveLength(self):
        f = open("./img_tmp/length.txt", "a")
        for ele in self.waveLengthList:
            f.write(str(ele) + "\n")
        f.close()

    def onClickedBtnAutoTest(self):
        # 为满足多次重复测量情况，在每次测量前，需要对一些record进行清零操作
        self.waveHeightList = []  # 波高record清零
        self.waveLengthList = []  # 波长record清零
        self.wireDiameterList = []  # 钢丝直径清零
        self.btn_auto_test.setText(u"测量中。。")
        self.btn_auto_test.setDisabled(True)  # 设置按钮无法使用，并改变文字提醒
        self.isMeasuring = 1  # 设置工作状态为【正在测量中】

    def onClickedBtnStartSystem(self):
        self.btn_start_system.setDisabled(True)
        self.initCamera()
        # time.sleep(5)
        self.timerShowImage.start(50)
        self.isMeasuring = 0  # 0-未测量，待机状态。1-自动测量中。2-演示模式。

    def onClickedBtnCloseSystem(self):
        # print "valid frame:", self.ci.cntValidFrame
        # print "dropped frame:", self.ci.cntDropFrame
        self.timerShowImage.stop()
        print "Timer timerShowImage has been closed"
        self.ci.closeCamera()
        print "Camera has been closed"
        QCoreApplication.instance().quit()
        print "total time:", self.ci.timeStopCapture - self.ci.timeStartCapture

    def onClickedBtnSaveFile(self):
        self.timerShowImage.stop()
        listToSave = [[] for i in range(self.indexRecordToExcel+1)]
        for i in range(self.indexRecordToExcel+1):
            for j in range(10):
                if j == 3:
                    combContent = self.table.cellWidget(i, j).currentText()
                    listToSave[i].append(unicode(combContent))
                else:
                    if self.table.item(i, j) is None:
                        listToSave[i].append("")
                    else:
                        listToSave[i].append(unicode(self.table.item(i, j).text()))

        f = open("./data/data.csv", "ab")
        wr = csv.writer(f, dialect="excel")
        listTableHeader = [u"日期", u"盘号", u"车台号", u"类型",
                           u"大波波高", u"小波波高", u"大波波长", u"小波波长",
                           u"行动", u"备注"]
        listTableHeader = [s.encode("gbk") for s in listTableHeader]
        wr.writerow(listTableHeader)
        for row in listToSave:
            row = [s.encode("gbk") for s in row]
            wr.writerow(row)
        f.close()
        saved = QMessageBox.information(None, "Saved", u"数据已保存完毕")
        if saved == QMessageBox.Ok:
            self.timerShowImage.start(50)


    def onClickedBtnShowMode(self):
        if not self.SHOW_COUNT:
            self.SHOW_COUNT = True
            self.isMeasuring = 2
        else:
            self.SHOW_COUNT = False
            self.isMeasuring = 0

    def onClickedBtnFocus(self):
        self.ci.setRoiToDefault()
        self.ci.getOneFrame()
        self.ci.endCapture()
        ip = ImageProcessing.ImageProcessing(self.ci.img)
        ip.doHoughTrans()
        self.ci.setRoi(self.ROIRANGE, ip.C - self.ROIRANGE/2)
        self.ci.startCapture()

    def onClickedBtnCancel(self):
        self.btn_auto_test.setText(u"自动测量")
        self.btn_auto_test.setDisabled(False)  # 恢复测量Btn状态
        self.progressBar.setValue(0)  # 清零进度条
        self.cntImgMeasuring = 0  # 清零测量计时计数
        self.isMeasuring = 0  # 设置状态标志位，不在测量中，不进行图像和数据处理



