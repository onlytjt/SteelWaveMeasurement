#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from scipy.fftpack import fft
from scipy.fftpack import ifft
from numpy import NaN, Inf, arange, isscalar, asarray, array
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import matplotlib
from sklearn import linear_model
import ImageProcessing
import datetime
import MyThread


# 将得到的所有波高值，截取某个值一下的噪点
def medianCut(listData):
    listData = np.array(listData)
    median = (np.max(listData)+np.min(listData)) / 2
    mask = listData < median
    listData[mask] = median
    print median
    return listData


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
    FFT_Threshold = 10
    fftData = fft(inputList)
    fftData[FFT_Threshold:] = 0
    result = abs(ifft(fftData))
    return result


# 在波高值中找寻极值，并区分出大波和小波
def findExtremum(inputList):
    extremumList = []
    extremumIndexList = []

    data = np.array(inputList)
    for i in range(3, len(inputList)-3, 1):
        if data[i]>=data[i+1] and data[i] >= data[i-1] \
                and data[i]>data[i-2] and data[i]>data[i+2]\
                and data[i]>data[i-3] and data[i]>data[i+3]:
            extremumList.append(data[i])
            extremumIndexList.append(i)

    extremumMin = np.where(extremumList == np.min(extremumList))
    extremumMax = np.where(extremumList == np.max(extremumList))
    smallWavePosition = extremumIndexList[extremumMin[0][0]]
    bigWavePosition = extremumIndexList[extremumMax[0][0]]
    return smallWavePosition, bigWavePosition


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


# 将输入的2d-array，计算波长平均值并返回
def getAveWaveLength(inputArray):
    if inputArray.ndim != 2:
        return 0
    a = inputArray[:, 0]  # 将2d数组转化为1d
    l = len(a)
    if l < 2:
        return 0
    else:
        result = abs(a[l-1]-a[0]) / (l-1)
        return result


def getSMD(img):  # 灰度差分法
    SMD = 0
    M = img.shape[0]  # 图像行数
    N = img.shape[1]  # 图像列数
    for j in range(N):
        for i in range(1, M, 1):
            SMD += np.abs(int(img[i, j]) - int(img[i-1, j]))
    for i in range(M):
        for j in range(1, N, 1):
            SMD += np.abs(int(img[i, j]) - int(img[i, j-1]))
    return SMD


# 波长处理，将大于波长平均值1.2倍和小于0.7倍的取前后平均值
def waveLengthCut(inputList):
    ave = np.array(inputList).mean()
    for i in range(1, len(inputList)-1):
        if inputList[i] > (1.2 * ave) or inputList[i] < (0.7 * ave):
            inputList[i] = (inputList[i-1] + inputList[i+1]) / 2
    return inputList


'''
# 以下为新的波高波长提取算法
# 处理的流程为：
    1. 将图像进行处理，变为canny边缘图像后，提取出相应的ROI
    2. 将图像使用 imgToList() 转为两个存储曲线的list，存储后应先进行平滑滤波
    3. 在list中使用 peakdet() 函数提取出所有的极值点，可能包含噪点，杂点
    4. 使用 getWavePeak() 将极值点中的噪点去除
    5. 使用 peakPointToWavePara() 将极值点转化为波高，波长的像素值
# 可以直接使用 getWaveParaByPeak() 函数，注意传入参数为已经截取过ROI的canny图像
'''
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


# 对波的极值点进行优化
# 输入为初步使用了matlab函数得到的极值点，二维数组
def getWavePeak(inputArray, line="TopCurve"):
    print "纵坐标方差值: ", np.var(inputArray, axis=0)[1]
    print "最初的极值点: ", inputArray
    if np.var(inputArray, axis=0)[1] > 10:
        meanPeak = inputArray.mean(axis=0)[1]
        if line == "BottomCurve":  # 对于BottomCurve应该选择较小的极值点
            # peakMore：通过纵坐标平均分离后的极值点集合
            peakMore = np.array([row for row in inputArray if row[1] < meanPeak])
        else:  # 对于TopCurve应选择较大的极值点
            peakMore = np.array([row for row in inputArray if row[1] > meanPeak])
    else:  # 当纵坐标方差小于10，直接取平均值
        peakMore = inputArray
    # print "peakMore : ", peakMore

    # peakReal：通过横坐标间隔进行分离后的极值点坐标
    # print "peakMore, 第一阶段处理后: ", peakMore
    # print "peakMore, 第一阶段处理后: ", peakMore.shape
    listGap = []
    peakMoreNum = peakMore.shape[0]
    for i in range(1, peakMoreNum):
        listGap.append(peakMore[i, 0] - peakMore[i-1, 0])
    aveGap = np.array(listGap).mean()
    print "横坐标gap方差: ", np.array(listGap).var()
    print "listGap: ", listGap
    # print "aveGap is : ", aveGap
    peakReal = []
    if np.array(listGap).var() > 2000:
        if peakMore[0, 0] == 0:
            peakReal.append(peakMore[1])
        else:
            peakReal.append(peakMore[0])
        for i in range(1, peakMoreNum):
            if peakMore[i, 0] - peakMore[i - 1, 0] > aveGap:
                peakReal.append(peakMore[i])
    else:
        peakReal = peakMore
    peakReal = np.array(peakReal)
    # print "peakReal: ", peakReal
    # print "peakReal is : ", peakReal
    return peakReal


# 通过找寻极值点的方法计算出波高和波长值
# 输入参数为TopCurve与BottomCurve两条曲线的极值点，2d array
def peakPointToWavePara(peakTopCurve, peakBottomCurve, topCurve, bottomCurve, cnt):
    # 首先应去除极值点中，横坐标为0的点，减少误差出现的可能性
    peakTopCurve = np.array([row for row in peakTopCurve if row[0] != 0])
    peakBottomCurve = np.array([row for row in peakBottomCurve if row[0] != 0])

    '''=========处理波高值==========='''
    '''处理上方曲线的波高信息'''
    # matplotlib.use("Agg")
    # p1 = plt.subplot(121)
    # print "Top Curve 纵坐标方差: ", np.var(peakTopCurve, axis=0)[1]
    if peakTopCurve.shape[0] == 0:  # 没有极值点的情况，直接赋值在曲线中的最大值
        boundTopCurve = max(topCurve)
    else:  # 输入找到了有效的极值点
        if np.var(peakTopCurve, axis=0)[1] < 5:
            boundTopCurve = peakTopCurve.mean(axis=0)[1]
            xShowTop = [0, len(topCurve)-1]
            yShowTop = [boundTopCurve] * 2
        else:  # 当纵坐标方差较大时，需要进行斜线的拟合
            clfTop = linear_model.LinearRegression()
            X = peakTopCurve[:, 0][:, np.newaxis]
            y = peakTopCurve[:, 1]
            clfTop.fit(X, y)
            boundTopCurve = clfTop.predict(len(topCurve)/2)[0]
            xShowTop = np.array(range(len(topCurve)))[:, np.newaxis]
            yShowTop = clfTop.predict(xShowTop)
        # p1.plot(xShowTop, yShowTop)
    # print "boundTopCurve: ", boundTopCurve
    '''处理下方曲线的波高信息'''
    # print "Bottom Curve 纵坐标方差: ", np.var(peakBottomCurve, axis=0)[1]
    if peakBottomCurve.shape[0] == 0:  # 当曲线中找不到极值点，直接赋值曲线中的最小值
        boundBottomCurve = min(bottomCurve)
    else:
        if np.var(peakBottomCurve, axis=0)[1] < 5:
            boundBottomCurve = peakBottomCurve.mean(axis=0)[1]
            xShowBottom = [0, len(bottomCurve) - 1]
            yShowBottom = [boundBottomCurve] * 2
        else:  # 当纵坐标方差较大时，需要进行斜线的拟合
            clfBottom = linear_model.LinearRegression()
            X = peakBottomCurve[:, 0][:, np.newaxis]
            y = peakBottomCurve[:, 1]
            clfBottom.fit(X, y)
            boundBottomCurve = clfBottom.predict(len(bottomCurve)/2)[0]
            xShowBottom = np.array(range(len(bottomCurve)))[:, np.newaxis]
            yShowBottom = clfBottom.predict(xShowBottom)
        # p1.plot(xShowBottom, yShowBottom)
    # print "boundBottomCurve: ", boundBottomCurve
    waveHeight = boundTopCurve - boundBottomCurve
    # print "waveHeight: ", waveHeight

    '''=========处理波长值==========='''
    waveLengthList = []  # 首先将两个曲线中有用的波长值存储起来
    peakTopNum = peakTopCurve.shape[0]
    peakBottomNum = peakBottomCurve.shape[0]
    if peakTopNum >= 2:
        for i in range(1, peakTopNum):
            waveLengthList.append(peakTopCurve[i, 0] - peakTopCurve[i-1, 0])
    if peakBottomNum >= 2:
        for i in range(1, peakBottomNum):
            waveLengthList.append(peakBottomCurve[i, 0] - peakBottomCurve[i-1, 0])
    # 对waveLengthList中的波长数值进行处理，分类
    if len(waveLengthList) == 0:
        waveLength = 0
    elif len(waveLengthList) == 1:
        waveLength = waveLengthList[0]
    else:
        waveLengthList = sorted(waveLengthList, reverse=True)  # 波长像素值由高到低排序
        for i in range(len(waveLengthList)-1):
            if float(waveLengthList[i]) / waveLengthList[i+1] >= 1.5 and waveLengthList[i] > 800:
                waveLengthList = waveLengthList[i+1:]
                break
        waveLength = np.array(waveLengthList).mean()
    # print "waveLengthList: ", waveLengthList
    # print "waveLength: ", waveLength

    # 测试代码，用于绘制单幅处理后的图像
    '''
    p1.scatter(range(len(topCurve)), topCurve, c="r", s=1)
    for i in range(peakTopCurve.shape[0]):
        x = [peakTopCurve[i, 0]] * 2
        y = [peakTopCurve.mean(axis=0)[1] + 5, peakTopCurve.mean(axis=0)[1] - 5]
        p1.plot(x, y)

    p1.scatter(range(len(bottomCurve)), bottomCurve, c="g", s=1)
    for i in range(peakBottomCurve.shape[0]):
        x = [peakBottomCurve[i, 0]] * 2
        y = [peakBottomCurve.mean(axis=0)[1] + 5, peakBottomCurve.mean(axis=0)[1] - 5]
        p1.plot(x, y)
    # plt.show()
    savefig("./img_tmp/" + str(cnt) + ".png")
    plt.clf()
    '''
    plotRuntimeWave = MyThread.PlotRuntimeWaveThread(
        topCurve, bottomCurve, xShowTop, yShowTop, xShowBottom, yShowBottom, cnt)
    plotRuntimeWave.start()
    return waveHeight, waveLength


# 通过波峰极值点方式来计算波形的各种参数
# 输入参数为截取了ROI的canny和hough的纵坐标值
def getWaveParaByPeak(cutImg, cnt):
    topCurve, bottomCurve = imgToList(cutImg)  # 提取上方和下方的两条曲线
    topCurve = smoothFilter5(topCurve)  # 5点平滑滤波
    bottomCurve = smoothFilter5(bottomCurve)

    maxTabTopCurve, minTabTopCurve = peakdet(topCurve, 0.5)  # 通过函数直接找到极值点，包含了一些噪点。
    maxTabBottomCurve, minTabBottomCurve = peakdet(bottomCurve, 0.5)

    # peakTopCurve = getWavePeak(maxTabTopCurve, line="TopCurve")
    # peakBottomCurve = getWavePeak(minTabBottomCurve, line="BottomCurve")
    peakTopCurve = maxTabTopCurve
    peakBottomCurve = minTabBottomCurve
    waveHeight, waveLength = peakPointToWavePara(peakTopCurve, peakBottomCurve, topCurve, bottomCurve, cnt)

    return waveHeight, waveLength
