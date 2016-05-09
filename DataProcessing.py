#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from scipy.fftpack import fft
from scipy.fftpack import ifft
from numpy import NaN, Inf, arange, isscalar, asarray, array
import sys
from scipy.optimize import curve_fit

# 3点平滑滤波
def smoothFilter(inputList):
    for i in range(1, len(inputList)-1):
        inputList[i] = (inputList[i-1]+inputList[i]+inputList[i+1]) / 3
    return inputList


# 5点的平滑滤波，输入为原list和滤波窗长度，奇数
def smoothFilter5(ori):
    for i in range(2, len(ori)-2, 1):
        ori[i] = (ori[i-2] + ori[i-1] + ori[i] + ori[i+1] + ori[i+2]) / 5
    return ori


# 对数据进行FFT变换并滤波
def fftFilter(inputList):
    FFT_Threshold = 15
    fftData = fft(inputList)
    fftData[FFT_Threshold:] = 0
    result = abs(ifft(fftData))
    return result


# github上使用python重写了matlab中的findpeaks()方法
def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    Returns two arrays
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    """
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))
    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


# 波长处理，将大于波长平均值1.2倍和小于0.7倍的取前后平均值
def waveLengthCut(inputList):
    ave = np.array(inputList).mean()
    for i in range(1, len(inputList)-1):
        if inputList[i] > (1.2 * ave) or inputList[i] < (0.7 * ave):
            inputList[i] = (inputList[i-1] + inputList[i+1]) / 2
    return inputList


# 将2d array转换为使用list存储的两条边缘
# 方法为用竖直的线从左向右扫一遍，只要纵坐标值最大和最小的
# 输入参数应为经过canny算子提取后的边缘图像
def imgToList(img):
    rowNum = img.shape[0]
    columnNum = img.shape[1]
    listTop = []
    listBottom = []
    for i in range(columnNum):
        listTmp = []
        for j in range(rowNum):
            if img[j, i]:  # 找到边缘点
                listTmp.append(j)
        listTop.append(max(listTmp))
        listBottom.append(min(listTmp))
    return listTop, listBottom


'''
# 公共函数，将img转化为存储着两条边缘曲线的list
'''
def getEdgeList(img):
    topCurve, bottomCurve = imgToList(img)  # 提取上方和下方的两条曲线
    topCurve = smoothFilter(topCurve)  # 3点平滑滤波
    bottomCurve = smoothFilter(bottomCurve)
    return topCurve, bottomCurve

'''
# 尝试使用sin拟合来看一下效果
'''
def getWaveParaBySin(listTopCurve, listBottomCurve):
    xTrainTop = np.array(range(len(listTopCurve)))
    yTrainTop = np.array(listTopCurve)
    xTrainBottom = np.array(range(len(listBottomCurve)))
    yTrainBottom = np.array(listBottomCurve)

    yPredTop, top1, bottom1, lengthTop = doSinFit(xTrainTop, yTrainTop)
    yPredBottom, top2, bottom2, lengthBottom = doSinFit(xTrainBottom, yTrainBottom)

    waveHeight = top1 - bottom2
    waveLength = (lengthTop + lengthBottom) / 2

    return waveHeight, waveLength

    # print "top1:", top1
    # print "bottom1:", bottom1
    # print "top2:", top2
    # print "bottom2:", bottom2
    # print "lengthTop:", lengthTop
    # print "lengthBottom:", lengthBottom

    # plt.scatter(range(len(listTopCurve)), listTopCurve, s=1, c="b")
    # plt.plot(range(len(yPredTop)), yPredTop, "r")
    # plt.scatter(range(len(listBottomCurve)), listBottomCurve, s=1, c="b")
    # plt.plot(range(len(yPredBottom)), yPredBottom, "r")
    # plt.show()


def mySin(x, freq, amp, phase, offset):
    return amp * np.sin(freq * x + phase) + offset


def doSinFit(x, y):
    guessOffset = np.mean(y)
    guessFreq = 2.0 * np.pi / 550
    guessAmp = np.abs(np.max(y - guessOffset))
    guessPhase = 1.0
    p0 = [guessFreq, guessAmp,  # 首先要给出一组较为合理的初始值
          guessPhase, guessOffset]  # 参数的顺序参考数组p0
    # dataFirstGuess = self.mySin(x, *p0)
    fit = curve_fit(mySin, x, y, p0=p0)
    dataFit = mySin(x, *fit[0])
    # print "original guess p0 is: ", p0
    # print " p0 is: ", fit[0]
    top = np.abs(fit[0][1]) + fit[0][3]  # 计算拟合出的sin函数的波峰和波谷的坐标
    bottom = -np.abs(fit[0][1]) + fit[0][3]
    length = 2.0 * np.pi / fit[0][0]
    return dataFit, top, bottom, length
