#!/usr/bin/python
# coding=utf-8

"""
gnss坐标转换库
Version：1.1
Author:LZ_CUMT
 Date:2022/04/12
"""
import numpy as np
from math import sin, cos, atan, pi, sqrt, atan2

# xyz转换为llh（经纬度）
def xyz2llh(ecef):
    aell = 6378137.0
    fell = 1.0 / 298.257223563
    deg = pi / 180
    u = ecef[0]
    v = ecef[1]
    w = ecef[2]
    esq = 2*fell-fell*fell
    lat = 0
    N = 0
    if w == 0:
        lat = 0
    else:
        lat0 = atan(w/(1-esq)*sqrt(u*u+v*v))
        j = 0
        delta = 10 ^ 6
        limit = 0.000001/3600*deg
        while delta > limit:
            N = aell / sqrt(1 - esq * sin(lat0)*sin(lat0))
            lat = atan((w / sqrt(u*u + v*v)) * (1 + (esq * N * sin(lat0) / w)))
            delta = abs(lat0 - lat)
            lat0 = lat
            j = j + 1
            if j > 10:
                break
    long = atan2(v, u)
    h = (sqrt(u*u+v*v)/cos(lat))-N
    llh = [lat * 180 / pi, long * 180 / pi, h]
    return np.array(llh)

# 经纬度转化为xyz(参考RTKLIB)
def llh2xyz(llh):
    RE_WGS84 = 6378137.0
    FE_WGS84 = 1.0/298.257223563
    lat = llh[0] * pi / 180
    lon = llh[1] * pi / 180
    h = llh[2]
    sinp = sin(lat)
    cosp = cos(lat)
    sinl = sin(lon)
    cosl = cos(lon)
    e2 = FE_WGS84*(2.0-FE_WGS84)
    v = RE_WGS84 / sqrt(1.0 - e2 * sinp * sinp)
    x = (v+h)*cosp*cosl
    y = (v+h)*cosp*sinl
    z = (v*(1.0-e2)+h)*sinp
    return np.array([x, y, z])


# xyz转换至以测站精确坐标为基准的enu坐标
def xyz2enu(xyz, basecrd):
    llhcrd = xyz2llh(basecrd)
    phi = llhcrd[0] * pi / 180
    lam = llhcrd[1] * pi / 180
    sinphi = sin(phi)
    cosphi = cos(phi)
    sinlam = sin(lam)
    coslam = cos(lam)
    R = np.array([[       -sinlam,         coslam,      0],
                  [-sinphi*coslam, -sinphi*coslam, cosphi],
                  [ cosphi*coslam,  cosphi*sinlam, sinphi]])
    return R@(xyz-basecrd)

# 根据测站id在snx文件中查找测站精确坐标
def getcrd(siteid, sscfile):
    snxcrd = []
    if sscfile != '':
        f = open(sscfile, encoding='gb18030', errors='ignore')
        ln = f.readline()
        while ln:
            ln = f.readline()
            if not ln:
                print('[ERROR] Not find the siteid', siteid)
                break
            if ln[14:18] == siteid:
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                break
        if snxcrd:
            print('[INFO] The', siteid, 'sitecrd is', snxcrd)
        f.close()
    return snxcrd


def getsite(file, type):
    path = file.split('\\')
    if type != 3:
        return path[-1][0:4].upper()
    else:
        return path[-1][-8:-4].upper()

