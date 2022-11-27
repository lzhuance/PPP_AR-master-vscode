# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""

from math import floor

# Change year, day of year to GPS week, day of week
def yrdoy2gpst(year, doy):
    date_1980jan6 = ymd2mjd(1980, 1, 6)
    date = ymd2mjd(year, 1, 1)
    time_delta = date - date_1980jan6
    days_delta = time_delta + doy - 1
    gps_week = int(days_delta/7)
    gps_dow = int(days_delta - gps_week*7)
    return gps_week, gps_dow

# 年月日转换为儒略日
def ymd2mjd(year, mm, dd):
    if mm <= 2:
        mm += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += floor(30.6001 * (mm + 1)) + 2.0 - floor(year / 100.0) + floor(year / 400) + dd
    return mjd

# 年月日转换为GPS周及周内天
def ymd2wkdow(year, mm, dd):
    mjd0 = 44243
    mjd = ymd2mjd(year, mm, dd)
    difmjd = mjd-mjd0-1
    week = floor(difmjd / 7)
    dow = floor(difmjd % 7)
    return week, dow

# 年月日时分秒转换为GPS周及周内秒
def ymdhms2wksow(year, month, day, hour, min, sec):
    week, dow = ymd2wkdow(year, month, day)
    sow = dow * 86400 + hour * 3600 + min * 60 + sec
    return week, sow

def mjd2ymd(mjd):
    jd = mjd+2400000.5
    a = int(jd+0.5)
    b = a+1537
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6)
    D = int(b-d-int(30.6001*e) + (jd+0.5)-floor(jd+0.5))
    M = e -1-12*int(e/14)
    Y = c-4715-int((7+M)/10)
    return Y, M, D

def ydoy2ymd(year, doy):
    mjd = ymd2mjd(year, 1, 1)+doy-1
    year, month, day = mjd2ymd(mjd)
    return year, month, day