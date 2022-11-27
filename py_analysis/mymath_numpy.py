# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.1
 Date:2022/04/12
 '''
import math
import numpy as np

# 计算enu矩阵的RMS值
def math_rms(enu):
    sump = [0, 0, 0]
    rms = []
    for i in range(len(enu[0])):
        for j in range(len(enu)):
            sump[i] += enu[j][i] * enu[j][i]
        rms.append(round(math.sqrt(sump[i] / len(enu)), 4))
    return rms

def get_abs_max_in_list(list_, percent):
    abs_max = []
    for n in range(len(list_[0])):
        list_abs = np.zeros(len(list_))
        for i in range(len(list_)):
            list_abs[i] = abs(list_[i][n])
            abs_max.append(np.percentile(list_abs, percent))
    return abs_max

# 计算enu矩阵的RMS值
def math_rms_percent(enu,percent):
    enumax = np.zeros(3)
    for k in range(3):
        enu_abs = np.maximum(enu[:, k], -enu[:, k])
        enumax[k] = np.percentile(enu_abs, percent)
    sump = [0, 0, 0]
    rms = []
    for i in range(enu.shape[1]):
        for j in range(enu.shape[0]):
            if abs(enu[j, i])<enumax[i]:
                sump[i] += enu[j, i] * enu[j, i]
        rms.append(round(math.sqrt(sump[i] / enu.shape[0]), 4))
    return rms
