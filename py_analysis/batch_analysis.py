# coding=utf-8
# !/usr/bin/env python
"""
Program: batch_analysis.py
Function: batch analysis pos file of PPP_AR
Author:LZ_CUMT
Version:1.0 
Histroy:
2022/01/01 inital py file
2022/11/24 fix some bug
"""

from read_pos import readpos
import os
from gnss_crd import *
import math

# 计算收敛时间所在历元数
def single_cal_time(list_):
    i = 0
    for i in range(len(list_)-20):
        if abs(list_[i]) < 0.1 and abs(list_[i+1]) < 0.1 and abs(list_[i+2]) < 0.1 and abs(list_[i+3]) < 0.1 and \
        abs(list_[i+4]) < 0.1 and abs(list_[i+5]) < 0.1 and abs(list_[i+6]) < 0.1 and abs(list_[i+7]) < 0.1 and \
        abs(list_[i+8]) < 0.1 and abs(list_[i+9]) < 0.1 and abs(list_[i+10]) < 0.1 and abs(list_[i+11]) < 0.1 and \
        abs(list_[i + 12]) < 0.1 and abs(list_[i + 13]) < 0.1 and abs(list_[i + 14]) < 0.1 and abs(list_[i + 15])< 0.1 and \
        abs(list_[i + 16]) < 0.1 and abs(list_[i + 17]) < 0.1 and abs(list_[i + 18]) < 0.1 and abs(list_[i + 19]) < 0.1:
            break
    return i

# 计算ENU收敛时间所在历元数
def cal_time(enu):
    time = []
    for i in range(3):
        list_ = []
        for j in range(len(enu)):
            list_.append(enu[j][i])
        time_ = single_cal_time(list_)
        time.append(time_)
    return time

# 计算RMS
def single_cal_rms(list_):
    sum = 0
    num = 0
    for i in list_:
        sum += i*i
        num += 1
    return math.sqrt(sum/num)

# 计算ENU方向RMS
def cal_rms(enu, time):
    rms = []
    for i in range(3):
        list_ = []
        for j in range(time[i], len(enu)):
            list_.append(enu[j][i])
        rms_ = single_cal_rms(list_)
        rms.append(rms_)
    return rms

# 识别文件信息
def fix_or_float(pos_file):
    pos_file_ = pos_file[:-4]
    pos_file_info = pos_file_.split("_")
    if pos_file_info[4] == "FLOAT":
        return pos_file_info[0], pos_file_info[1], pos_file_info[4], " "
    else:
        return pos_file_info[0], pos_file_info[1], pos_file_info[4], pos_file_info[5]


if __name__ == '__main__':
    filepath = r'E:\PPP_AR-master\GNSS_DATA\2022\274\result_PPP-KINE\obs\com'     # 批处理所在文件路径
    snxfile = r'E:\PPP_AR-master\GNSS_DATA\2022\274\products\igs\igs22P2229.snx'  # snx文件路径

    filelist = []
    file_type = []
    eles = os.listdir(filepath)
    for ele in eles:
        if '.pos' in ele[-4:]:
            filelist.append(ele)
            file_type.append(5)

    writefile = filepath + "\\cal_cc_pppar.csv"
    fw = open(writefile,"w")
    csv_header = "site,system,fix_flag,freq_flag,time_E,time_N,time_U,rms_E,rms_N,rms_U\n"
    fw.write(csv_header)

    # repeat plot with the number of files in filelist
    for i in range(len(filelist)):
        site, sys, fix_flag, freq_flag = fix_or_float(filelist[i])
        pos_file_path = filepath + "\\" + filelist[i]

        # read pos file
        data = readpos(pos_file_path, file_type[i])
        if np.size(data)==0:
            continue
        sow = data[:, 1]
        xyz = data[:, 2:]

        base = getcrd(site, snxfile)
        if base == []:
            continue
        # expand base to base_all and align to data by sow
        base_all = np.zeros(xyz.shape)
        for j in range(xyz.shape[0]):
            base_all[j, :] = base

        # calculate ENU with xyz and base_all
        enu = np.zeros(xyz.shape)
        for j in range(xyz.shape[0]):
            if base_all[j, 0] != 0:
                enu[j, :] = xyz2enu(xyz[j, :], base_all[j, :])
            else:
                enu[j, :] = [0, 0, 0]

        index = cal_time(enu)
        time = [x / 2 for x in index]
        rms = cal_rms(enu, index)
        csv_body = "{},{},{},{},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(site, sys,fix_flag,freq_flag,
                                                                    time[0], time[1], time[2], rms[0],rms[1], rms[2])
        fw.write(csv_body)