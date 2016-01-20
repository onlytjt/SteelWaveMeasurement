#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("./HeightRecord.txt", dtype=float, delimiter=",")
data = data[:, 2]

indexOfPeakInData = []  # 用于保存数据中找到的极值的索引值
# 首先做前后向查分，找到一些极值
for index, value in enumerate(data):
    if value>=data[index-1] and value>=data[index+1] and value>=data[index-2] and value>=data[index+2]:
        indexOfPeakInData.append(index)
# 去除极值中索引相邻，值重复的项
for i, index in enumerate(indexOfPeakInData):
    if index-1 == indexOfPeakInData[i-1] and data[index] == data[index-1]:
        del indexOfPeakInData[i]  # 保留较小的下标值

peak1 = []; peak2 = []
for i, index in enumerate(indexOfPeakInData):
    if not i%2:  # 从第0开始
        peak1.append(data[index])
    else:
        peak2.append(data[index])
peak1 = np.array(peak1)
peak2 = np.array(peak2)

print peak1
print peak2

print peak1.mean()
print peak2.mean()


