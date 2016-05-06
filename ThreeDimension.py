#!/usr/bin/python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import DataProcessing as dp
import numpy as np


def buildWaveModel(height, length):
    height = dp.smoothFilter(height)  # 三点平滑滤波后再使用数据
    length = dp.waveLengthCut(length)  # 首先使用阈值对博长治进行剪裁
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
    bigWaveLength = max(bigWaveLengthList)
    smallWaveLength = min(smallWaveLengthList)

    # 波高曲线图
    p1 = plt.subplot(211)
    p1.scatter(range(len(height)), height, s=10)
    p1.plot(height, "r")
    for i in range(peakBigWave.shape[0]):  # 大波蓝色标注
        p1.plot([peakBigWave[i, 0]]*2, [15, 30], "b")
    for i in range(peakSmallWave.shape[0]):  # 小波红色标注
        p1.plot([peakSmallWave[i, 0]] * 2, [15, 30], "r")
     # 波长曲线图
    p2 = plt.subplot(212)
    p2.scatter(range(len(length)), length, s=10)
    p2.plot(length, "r")
    for i in range(peakBigWave.shape[0]):
        p2.plot([peakBigWave[i, 0]]*2, [500, 600], "b")
    for i in range(peakSmallWave.shape[0]):
        p2.plot([peakSmallWave[i, 0]] * 2, [500, 600], "r")
    plt.show()

    return bigWaveHeight, smallWaveHeight, bigWaveLength, smallWaveLength


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
