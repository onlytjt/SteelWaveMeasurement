#!/usr/bin/python
# -*- coding:utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np
import DataProcessing as dp
import ImageProcessing



def main():
    img = cv2.imread("./img/noise2.bmp", 0)
    ip = ImageProcessing.ImageProcessing(img)
    ip.doHoughTrans()
    img = ip.cannyImg[ip.C-125:ip.C+125, :]
    topCurve, bottomCurve = dp.imgToList(img)

    maxTabTopCurve, minTabTopCurve = dp.peakdet(topCurve, 0.5)  # 通过函数直接找到极值点，包含了一些噪点。
    maxTabBottomCurve, minTabBottomCurve = dp.peakdet(bottomCurve, 0.5)

    peakTopCurve = dp.getWavePeak(maxTabTopCurve, line="TopCurve")
    peakBottomCurve = dp.getWavePeak(minTabBottomCurve, line="BottomCurve")

    waveHeight, waveLength = dp.peakPointToWavePara(peakTopCurve, peakBottomCurve)

    plt.scatter(range(len(topCurve)), topCurve, c="r", s=1)
    plt.scatter(range(len(bottomCurve)), bottomCurve, c="g", s=2)
    plt.plot(range(2048), [peakTopCurve.mean(axis=0)[1]]*2048)
    plt.plot(range(2048), [peakBottomCurve.mean(axis=0)[1]] * 2048)
    for i in range(peakTopCurve.shape[0]):
        x = [peakTopCurve[i, 0]] * 2
        y = [peakTopCurve.mean(axis=0)[1]+5, peakTopCurve.mean(axis=0)[1]-5]
        plt.plot(x, y)
    for i in range(peakBottomCurve.shape[0]):
        x = [peakBottomCurve[i, 0]] * 2
        y = [peakBottomCurve.mean(axis=0)[1]+5, peakBottomCurve.mean(axis=0)[1]-5]
        plt.plot(x, y)
    plt.show()

def test():
    img = cv2.imread("./img/153g.bmp", 0)
    ip = ImageProcessing.ImageProcessing(img)
    ip.doHoughTrans()
    img = ip.cannyImg[ip.C - 125:ip.C + 125, :]

    waveHeight, waveLenght = dp.getWaveParaByPeak(img)

if __name__ == '__main__':
    test()
