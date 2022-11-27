# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/04/09
"""

# rinex_long2short.py
# Author:LZ-CUMT
# Rename RINXE file from long to short by Batch processing
# Change File Name to GAMP File Name Format

# Choose the file path where you want to rename the rinex files
# obs  filename : ABMF00GLP_R_20200010000_01D_30S_MO.cro   ==> abmf0010.20o
# obs  filename : ABMF00GLP_R_20200010000_01D_30S_MO.crx   ==> abmf0010.20o
# nav  filename : BRDC00IGS_R_20200010000_01D_MN.rnx       ==> brdm0010.20p
# sp3  filename : GFZ0MGXRAP_20200010000_01D_05M_ORB.SP3   ==> gfz20863.sp3
# clk  filename : GFZ0MGXRAP_20200010000_01D_30S_CLK.CLK   ==> gfz20863.clk
# bia  filename : GBM0MGXRAP_20200010000_01D_30S_ABS.BIA   ==> gbm20863.bia
# p2c2 filename : P2C22001_RINEX.DCB                       ==> P2C22001.DCB
# erp  filename : igs20P2086.erp                           ==> igs20867.erp
# snx  filename : igs20P2086.snx                           ==>  igs2086.snx
#


import os
from gnss_time import *


def renamefile(path, file, renamef):
    if os.path.isfile(os.path.join(path, renamef)):
        os.remove(os.path.join(path, file))
        print("[INFO] The file", renamef, "has already existed!")
    else:
        os.rename(os.path.join(path, file), os.path.join(path, renamef))

def rename_rinex(path):
    for file in os.listdir(path):
        if file[-4:] == ".cro":
            obsrename = (file[0:4]).lower()+file[16:19]+"0."+file[14:16]+"o"
            renamefile(path, file, obsrename)
        elif file[-4:] == ".rnx":
            if file[0:4] == "BRDC":
                navrename = "brdm"+file[16:19]+"0."+file[14:16]+"p"
            else:
                navrename = (file[0:4]).lower()+file[16:19]+"0."+file[14:16]+"p"
            renamefile(path, file, navrename)
        elif file[-4:] == ".SP3":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            sp3rename = (file[0:3]).lower()+str(week)+str(dow)+".sp3"
            renamefile(path, file, sp3rename)
        elif file[-4:] == ".CLK":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            clkrename = (file[0:3]).lower()+str(week)+str(dow)+".clk"
            renamefile(path, file, clkrename)
        elif file[-4:] == ".BIA":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            biarename = (file[0:3]).lower()+str(week)+str(dow)+".bia"
            renamefile(path, file, biarename)
        elif file[-9:] == "RINEX.DCB":
            p2c2rename = file[0:8]+file[-4:]
            renamefile(path, file, p2c2rename)
        elif file[-4:] == ".erp":
            if file[5] == "P":
                erprename = file[0:3]+file[6:10]+'7'+file[-4:]
                renamefile(path, file, erprename)
        elif file[-4:] == ".snx":
            if file[5] == "P":
                snxrename = file[0:3]+file[-8:]
                renamefile(path, file, snxrename)

    print("[INFO] Rename the files in ", path," complete! ")
