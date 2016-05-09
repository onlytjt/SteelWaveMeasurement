#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PlotRuntimeWaveThread(threading.Thread):
    def __init__(self, topCurve, bottomCurve, xShowTop, yShowTop, xShowBottom, yShowBottom, cnt):
        threading.Thread.__init__(self)
        self.topCurve = topCurve
        self.bottomCurve = bottomCurve
        self.xShowTop = xShowTop
        self.yShowTop = yShowTop
        self.xShowBottom = xShowBottom
        self.yShowBottom = yShowBottom
        self.cnt = cnt

    def run(self):
        matplotlib.use("Agg")
        p1 = plt.subplot(211)
        p1.scatter(range(len(self.topCurve)), self.topCurve, s=10)
        p1.plot(self.xShowTop, self.yShowTop)
        p2 = plt.subplot(212)
        p2.scatter(range(len(self.bottomCurve)), self.bottomCurve, s=10)
        p2.plot(self.xShowBottom, self.yShowBottom)
        savefig("./img_tmp/" + str(self.cnt) + ".png")
        plt.clf()


class PlotResultThread(QThread):
    def __init__(self, height, peakBigWave, peakSmallWave):
        QThread.__init__(self)
        self.height = height
        self.peakBigWave = peakBigWave
        self.peakSmallWave = peakSmallWave

    def run(self):
        plt.clf()
        p1 = plt.subplot(111)
        p1.scatter(range(len(self.height)), self.height, s=10)
        p1.plot(self.height, "r")
        # for i in range(self.peakBigWave.shape[0]):  # 大波蓝色标注
        #     p1.plot([self.peakBigWave[i, 0]] * 2, [15, 30], "b")
        # for i in range(self.peakSmallWave.shape[0]):  # 小波红色标注
        #     p1.plot([self.peakSmallWave[i, 0]] * 2, [15, 30], "r")
        plt.show()


