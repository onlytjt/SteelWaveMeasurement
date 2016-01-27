#!/usr/bin/python
# -*- coding:utf-8 -*-
# 功能:实现了输入ndarray图像，输出输出该幅图像的峰峰值的数据
# 包括直接计算和通过霍夫变换计算两种方式
# 注：输入给构造函数的图像必须是灰度图

import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import leastsq

class ImageProcessing:
    # 构造函数，读入图像
    # 私有变量存储：高斯模糊，模糊后二值图(反转颜色)，canny算子边缘图
    def __init__(self, image):
        self.originImg = image
        self.blurImg = cv2.GaussianBlur(self.originImg, (3, 3), 0)
        ret, self.binaryBlurImg = cv2.threshold(self.blurImg, 125, 255, cv2.THRESH_BINARY_INV)
        self.cannyImg = cv2.Canny(self.binaryBlurImg, 50, 150) # 图像正放

    # 直接遍历canny边缘图，计算整幅图像的最高和最低
    def directGetP2P(self):
        cannyImgT = np.transpose(self.cannyImg) # 将图像旋转90度放置以计算峰峰值(P2P)
        cnt = 0
        indexTopMin = 963
        indexBottomMax = 0
        time1 = datetime.datetime.now()
        for column in cannyImgT:
            for index, ele in enumerate(column):
                if ele:
                    cnt += 1
                    if cnt%2 == 1: # 对应第一次找到直线，上方直线
                        indexTopMin = min(index, indexTopMin)
                    else: # 对应第二次找到直线，下方直线
                        indexBottomMax = max(index, indexBottomMax)
        print indexTopMin
        print indexBottomMax
        time2 = datetime.datetime.now()
        print "Processing time:", time2 - time1
        return indexTopMin, indexBottomMax

    # 对已经模糊并二值化的图像进行霍夫变换
    # 提取图像中的直线，并保存直线A, B, C参数
    def doHoughTrans(self):
        img = self.binaryBlurImg
        lines = cv2.HoughLines(img, 1, np.pi/180, 300)
        if lines == None:  # 如果经过霍夫变换，发现图像中没有钢丝，直接返回False
            return False
        result = self.cannyImg.copy()
        for line in lines[0]:
            rho = line[0]
            theta = line[1]
            if (theta < (np.pi/4.0)) or (theta > (3.*np.pi/4.0)):
                pt1 = (int(rho/np.cos(theta)), 0)
                pt2 = (int((rho-result.shape[0]*np.sin(theta))/np.cos(theta)),result.shape[0])
                cv2.line(result, pt1, pt2, (0, 0, 0), 1)
            else:
                pt1 = (0, int(rho/np.sin(theta)))
                pt2 = (result.shape[1], int((rho-result.shape[1]*np.cos(theta))/np.sin(theta)))
                cv2.line(result, pt1, pt2, (0, 0, 0), 1)

        k = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
        b = -k*pt1[0] + pt1[1]
        # y=kx+b  kx-y+b=0
        self.A = k
        self.B = -1
        self.C = b
        # print "A=", self.A
        # print "B=", self.B
        # print "C=", self.C
        return True  # 如果图像中有钢丝，计算钢丝中心线方程，并返回True

    # 计算输入点到已得出霍夫变换直线的距离，利用点到直线距离公式
    # 注意这里的pt坐标需要自己转换清楚
    def calDisPointToLine(self, pt):
        x = pt[0]
        y = pt[1]
        return (self.A*x + self.B*y + self.C)/np.sqrt(self.A*self.A + self.B*self.B)

    # 使用霍夫变换方法求出峰峰值(P2P)
    def getP2PByHough(self):
        # time1 = datetime.datetime.now()
        # self.doHoughTrans()  # 求出A, B, C
        cannyImgT = np.transpose(self.cannyImg)  # 将图像旋转90度放置以计算峰峰值(P2P)
        disTop = 0
        disBottom = 0
        for x, column in enumerate(cannyImgT):
            for y, ele in enumerate(column):
                if ele:
                    tmp = self.calDisPointToLine((x, y))
                    if tmp > disTop:
                        disTop = tmp
                    elif tmp < disBottom:
                        disBottom = tmp
        # print "disTop=", disTop
        # print "disBottom", disBottom
        # time2 = datetime.datetime.now()
        # print "Processing time:", time2 - time1
        # time2 = datetime.datetime.now()
        # print "Hough image processing time: ", time2-time1
        return disTop, disBottom

    # 遍历已经提取完边缘的图像，提取出边缘上所有的点
    def getWaveHeightBySin(self):
        cannyImgT = np.transpose(self.cannyImg)  # 将图像旋转90度，以沿纵向遍历
        xTrain1 = []; yTrain1 = []
        xTrain2 = []; yTrain2 = []
        for x, column in enumerate(cannyImgT):
            cnt = False
            for y, ele in enumerate(column):
                if ele:
                    cnt = not cnt
                    if cnt:  # 使用-y，图像坐标系和数学坐标系不同，防止波形翻转
                        xTrain1.append(x); yTrain1.append(-y)
                    else:
                        xTrain2.append(x); yTrain2.append(-y)

        xTrain1 = np.array(xTrain1); yTrain1 = np.array(yTrain1)
        xTrain2 = np.array(xTrain2); yTrain2 = np.array(yTrain2)
        yPred1, top1, bottom1, waveLength1 = self.doSinFit(xTrain1, yTrain1)
        yPred2, top2, bottom2, waveLength2 = self.doSinFit(xTrain2, yTrain2)
        wireDiameter = (top1+bottom1)/2 - (top2+bottom2)/2
        waveHeight = top1 - bottom2
        wireDiameter = float("%0.2f" % wireDiameter)
        waveHeight = float("%0.2f" % waveHeight)  # 小数格式控制
        # 通过一个独立窗口显示sin函数拟合结果，使用matplotlib
        # plt.clf()
        # plt.scatter(xTrain1, yTrain1, c="r", s=1)
        # plt.scatter(xTrain2, yTrain2, c="r", s=1)
        # plt.plot(xTrain1, yPred1, "b")
        # plt.plot(xTrain2, yPred2, "r")
        # plt.show(block=False)
        # plt.pause(0.0001)
        # print "top1: ", top1
        # print "bottom2: ", bottom2
        waveLengthAve = (waveLength1 + waveLength2) / 2
        return waveHeight, waveLengthAve, wireDiameter

    def mySin(self, x, freq, amp, phase, offset):
        return amp * np.sin(freq*x + phase) + offset

    def doSinFit(self, x, y):
        guessOffset = np.mean(x)
        guessFreq = 2.0*np.pi / 650
        guessAmp = np.abs(np.max(x-guessOffset))
        guessPhase = 1.0
        p0 = [guessFreq, guessAmp,   # 首先要给出一组较为合理的初始值
              guessPhase, guessOffset]  # 参数的顺序参考数组p0
        # dataFirstGuess = self.mySin(x, *p0)
        fit = curve_fit(self.mySin, x, y, p0=p0)
        dataFit = self.mySin(x, *fit[0])
        # print "original guess p0 is: ", p0
        # print "predict p0 is: ", fit[0]
        top = np.abs(fit[0][1]) + fit[0][3]  # 计算拟合出的sin函数的波峰和波谷的坐标
        bottom = -np.abs(fit[0][1]) + fit[0][3]
        waveLength = 2*np.pi / fit[0][0]
        return dataFit, top, bottom, waveLength

    @staticmethod
    def smoothFilter(inputList):  # 3点平滑滤波
        for i in (1, len(inputList)-2):
            inputList[i] = (inputList[i-1]+inputList[i]+inputList[i+1]) / 3
        return inputList


def main():
    # 类使用方法举例
    img = cv2.imread("./res/oriBad.png", 0)
    ip = ImageProcessing(img)


if __name__ == "__main__":
    main()


# while True:
#         ins.captureFrame()
#         ins.showImage()
#         if cv2.waitKey(1) == 27: # press esc to quit
#             break
#     ins.endShow()