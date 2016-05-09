#!/usr/bin/python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import DataProcessing as dp
import numpy as np
import MyThread as mt


def buildWaveModel(height, length):
    height = dp.smoothFilter(height)  # 三点平滑滤波后再使用数据
    length = dp.waveLengthCut(length)  # 首先使用阈值对波长治进行剪裁
    length = dp.smoothFilter(length)  # 三点平滑滤波后再使用数据

    '''=========处理波高值==========='''
    maxTab, minTab = dp.peakdet(height, 0.5)  # 提取图像中所有的极值点，并去除第一个点
    peakInHeight = [row for row in maxTab if row[0] != 0]
    avePeakHeight = np.array(peakInHeight).mean(axis=0)[1]

    peakBigWave = np.array([row for row in peakInHeight if row[1] > avePeakHeight])  # 大小波极值点分离
    peakSmallWave = np.array([row for row in peakInHeight if row[1] < avePeakHeight])

    bigWaveHeight = peakBigWave.mean(axis=0)[1]  # 计算大小波的波高像素值
    smallWaveHeight = peakSmallWave.mean(axis=0)[1]

    '''=========处理波长值==========='''
    bigWaveLengthList = []
    smallWaveLengthList = []
    for i in peakBigWave[:, 0]:
        if 1 <= i <= len(length)-2:
            i = int(i)
            bigWaveLengthList.append((length[i-1]+length[i]+length[i+1]) / 3)
        else:
            bigWaveLengthList.append(length[i])
    for i in peakSmallWave[:, 0]:
        if 1 <= i <= len(length)-2:
            i = int(i)
            smallWaveLengthList.append((length[i-1]+length[i]+length[i+1]) / 3)
        else:
            smallWaveLengthList.append(length[i])

    length1 = np.mean(bigWaveLengthList)
    length2 = np.mean(smallWaveLengthList)
    bigWaveLength = max(length1, length2)
    smallWaveLength = min(length1, length2)

    # plotResultThread = mt.PlotResultThread(height, peakBigWave, peakSmallWave)
    # plotResultThread.start()

    print "大波波高像素值:", bigWaveHeight
    print "小波波高像素值:", smallWaveHeight
    print "大波波长像素值:", bigWaveLength
    print "小波波长像素值:", smallWaveLength
    print "-----------------------------"

    bigWaveHeight = "%0.1f" % (bigWaveHeight*6.6188 - 7.356)
    smallWaveHeight = (smallWaveHeight*6.6188 - 7.356)*0.3 + (smallWaveHeight*2.474+95.93)*0.7
    # bigWaveLength = "%0.1f" % (bigWaveLength*0.9857 + 2510.35)
    # smallWaveLength = "%0.1f" % (smallWaveLength*(-1.6723) + 3657.65)

    return bigWaveHeight, smallWaveHeight, bigWaveLength, smallWaveLength, peakBigWave, peakSmallWave


def main():
    height = []
    f1 = open("./img_tmp/height.txt", "r")
    for line in f1.readlines():
        line = line.strip("\n")
        height.append(float(line))
    f1.close()
    length = []
    f2 = open("./img_tmp/length.txt", "r")
    for line in f2.readlines():
        line = line.strip("\n")
        length.append(float(line))
    buildWaveModel(height, length)


if __name__ == '__main__':
    main()
