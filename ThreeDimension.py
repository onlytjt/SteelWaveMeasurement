#!/usr/bin/python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import DataProcessing as dp
import numpy as np



def buildWaveModel(height, length, heightFFT):
    height = dp.smoothFilter(height)  # 三点平滑滤波后再使用数据
    length = dp.waveLengthCut(length)  # 首先使用阈值对波长治进行剪裁
    length = dp.smoothFilter(length)  # 三点平滑滤波后再使用数据

    '''=========处理波高值==========='''
    maxTab, minTab = dp.peakdet(heightFFT, 0.1)  # 提取图像中所有的极值点，并去除第一个点
    peakInHeight = [row for row in maxTab if row[0] != 0]
    avePeakHeight = np.array(peakInHeight).mean(axis=0)[1]

    # peakBigWave = np.array([row for row in peakInHeight if row[1] > avePeakHeight])  # 大小波极值点分离
    # peakSmallWave = np.array([row for row in peakInHeight if row[1] < avePeakHeight])

    # 将FFT波形得到的极值点转化为原波高值曲线中的极值点
    peakBigWaveFFT = np.array([row for row in peakInHeight if row[1] > avePeakHeight])  # 大小波极值点分离
    peakSmallWaveFFT = np.array([row for row in peakInHeight if row[1] < avePeakHeight])
    peakBigWave = np.array([[int(i), height[int(i)]] for i in peakBigWaveFFT[:, 0]])
    peakSmallWave = np.array([[int(i), height[int(i)]] for i in peakSmallWaveFFT[:, 0]])

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

    print u"大波波高像素值:", "%0.1f" % bigWaveHeight
    print u"小波波高像素值:", "%0.1f" % smallWaveHeight
    print u"大波波长像素值:", "%0.1f" % bigWaveLength
    print u"小波波长像素值:", "%0.1f" % smallWaveLength
    print "-----------------------------"

    # 像素物理分辨率直线，与大小波分别标定直线
    bigWaveHeight = (bigWaveHeight*6.6188 - 7.356)*0.5 + (bigWaveHeight*3.236 + 91.611)*0.5
    bigWaveHeight = "%0.1f" % bigWaveHeight
    smallWaveHeight = (smallWaveHeight*6.6188 - 7.356)*0.3 + (smallWaveHeight*2.474 + 95.93)*0.7
    smallWaveHeight = "%0.1f" % smallWaveHeight

    bigWaveLength = "%0.1f" % (bigWaveLength*1.816 + 2046.33)
    smallWaveLength = "%0.1f" % (smallWaveLength*0.942 + 2366.73)

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
