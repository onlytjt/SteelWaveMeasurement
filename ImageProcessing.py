#!/usr/bin/python
# -*- coding:utf-8 -*-
# 功能:实现了输入ndarray图像，输出输出该幅图像的峰峰值的数据
# 包括直接计算和通过霍夫变换计算两种方式
# 注：输入给构造函数的图像必须是灰度图

import cv2
import numpy as np
import datetime

class ImageProcessing:
    # 构造函数，读入图像
    # 私有变量存储：高斯模糊，模糊后二值图(反转颜色)，canny算子边缘图
    def __init__(self, image):
        self.originImg = image
        self.blurImg = cv2.GaussianBlur(self.originImg, (3, 3), 0)
        ret, self.binaryBlurImg = cv2.threshold(self.blurImg, 78, 255, cv2.THRESH_BINARY_INV)
        self.cannyImg = cv2.Canny(self.blurImg, 50, 150) # 图像正放

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
        lines = cv2.HoughLines(img, 1, np.pi/180, 120)
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



    # 计算输入点到已得出霍夫变换直线的距离，利用点到直线距离公式
    # 注意这里的pt坐标需要自己转换清楚
    def calDisPointToLine(self, pt):
        x = pt[0]
        y = pt[1]
        return (self.A*x + self.B*y + self.C)/np.sqrt(self.A*self.A + self.B*self.B)

    # 使用霍夫变换方法求出峰峰值(P2P)
    def getP2PByHough(self):
        time1 = datetime.datetime.now()
        self.doHoughTrans() # 求出A, B, C
        cannyImgT = np.transpose(self.cannyImg) # 将图像旋转90度放置以计算峰峰值(P2P)
        cnt = 0
        disTop = 0
        disBottom = 0
        # time1 = datetime.datetime.now()
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
        # print "PP pixels is:", disTop - disBottom
        # print "PP value is:", 4000/964 * (disTop - disBottom)
        # time2 = datetime.datetime.now()
        # print "Hough image processing time: ", time2-time1
        return disTop, disBottom


def main():
    # 类使用方法举例
    img = cv2.imread("./res/111.bmp", 0)
    ins = ImageProcessing(img)
    # ins.getRoughOfEdge(img)
    # ins.getP2PByHough()
    # ins.directGetP2P()
    pass
if __name__ == "__main__":
    main()
