# coding=utf-8
# !/usr/bin/env python
'''
 Program:read_pos
 Author:LZ_CUMT
 Version:1.0
 Date:2022/04/12
 '''

from gnss_time import ymdhms2wksow
import numpy as np
from gnss_crd import llh2xyz

def strtime2gpstime(ymd, hms):
    year = int(ymd[0:4])
    month = int(ymd[5:7])
    day = int(ymd[8:10])
    hour = int(hms[0:2])
    minite = int(hms[3:5])
    second = float(hms[6:])
    week, sow = ymdhms2wksow(year, month, day, hour, minite, second)
    return [week, sow]

def read_RTKLIB_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[0] == '%':
            if "latitude(deg)" in ln:
                type = 'LLH'
                break
            elif "x-ecef(m)" in ln:
                type = 'XYZ'
                break
    ln = f.readline()
    while ln:
        if ln[0] != '%' and ln[0] != '\n':
            ele = ln.split()
            ymd = ele[0]
            hms = ele[1]
            time = strtime2gpstime(ymd, hms)
            if type == 'XYZ':
                xyz = [float(x) for x in ele[2:5]]
            elif type == 'LLH':
                llh = [float(x) for x in ele[2:5]]
                xyz = llh2xyz(np.array(llh)).tolist()
            else:
                return 0
            xyzlist.append(time+xyz)
        ln = f.readline()
    print("[INFO] Finish Reading the RTKLIB pos file")
    return xyzlist

def read_GAMP_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if not ln:
            break
        if len(ln) > 10:
            xyzlist.append([float(x) for x in ln.split()[6:11]])
        ln = f.readline()
    print("[INFO] Finish Reading the GAMP pos file")
    return xyzlist

def read_NetDiff_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if ln[0] != '%':
            ele = ln.split()
            ymd = ele[0]
            hms = ele[1]
            time = strtime2gpstime(ymd, hms)
            xyz = [float(x) for x in ele[7:10]]
            xyzlist.append(time+xyz)
        ln = f.readline()
    print("[INFO] Finish Reading the Net_Diff pos file")
    return xyzlist

def read_IE_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[3:10] == "(weeks)":
            break
    while ln:
        ln = f.readline()
        if not ln:
            break
        if ln[18:21] == "000":
            x = float(ln[22:36])
            y = float(ln[37:51])
            z = float(ln[52:66])
            t = int(ln[11:17])
            xyzlist.append([x, y, z, t])
    print("[INFO] Finish Reading the IE pos file")
    return xyzlist

def read_PPPAR_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[0] == '%':
            if "latitude(deg)" in ln:
                type = 'LLH'
                break
            elif "x-ecef(m)" in ln:
                type = 'XYZ'
                break
    ln = f.readline()
    while ln:
        if ln[0] != '%' and ln[0] != '\n':
            ele = [float(x) for x in ln.split(",")]
            time = ele[0:2]
            if type == 'XYZ':
                xyz = ele[2:5]
            elif type == 'LLH':
                llh = np.array(ele[2:5])
                xyz = llh2xyz(llh).tolist()
            else:
                return 0
            xyzlist.append(time+xyz)
        ln = f.readline()
    print("[INFO] Finish Reading the PPPAR pos file")
    return xyzlist

# 读取POS文件 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE 5:PPP_AR]
def readpos(file, pos_type):
    if pos_type == 1:
        xyzlist = read_RTKLIB_pos(file)
    elif pos_type == 2:
        xyzlist = read_GAMP_pos(file)
    elif pos_type == 3:
        xyzlist = read_NetDiff_pos(file)
    elif pos_type == 4:
        xyzlist = read_IE_pos(file)
    elif pos_type == 5:
        xyzlist = read_PPPAR_pos(file)
    else:
        print("[Error] Please cheak the input type!")
        return 0
    # data = xyzlist                                                         # Save as list
    data = np.array(xyzlist)                                                 # Save as numpy.array
    # data = pd.DataFrame(xyzlist, columns=['week', 'sow', 'x', 'y', 'z'])   # Save as pandas.DateFrame
    return data

