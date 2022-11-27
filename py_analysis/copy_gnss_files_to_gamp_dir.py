# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/04/09
"""

import os
import shutil
from gnss_time import *
from rinex_long2short import rename_rinex


def find_file(path, identifier, file_list):
    file_path = ""
    for file in os.listdir(path):
        if identifier in file:
            file_path = os.path.join(path, file)
            break
    if file_path != "":
        file_list.append(file_path)
    return file_list

def copy_from_rtkget_download(input, save_dir):
    rtkget_download_dir = r"D:\IGS_DATA"

    str_year = input[0]
    str_doy = input[1]
    products = input[2]
    site = input[3].upper()

    year = int(str_year)
    doy = int(str_doy)
    week, dow = yrdoy2gpst(year, doy)
    year, month, day = ydoy2ymd(year, doy)

    main_dir = os.path.join(rtkget_download_dir, input[0], input[1])
    file_list = []

    obs_dir = os.path.join(main_dir, "obs")
    nav_dir = os.path.join(main_dir, "products", "nav")
    products_dir = os.path.join(main_dir, "products", products)
    erp_dir = os.path.join(rtkget_download_dir, input[0], "igs_erp")
    snx_dir = os.path.join(rtkget_download_dir, input[0], "igs_snx")
    code_dcb_dir = os.path.join(rtkget_download_dir, input[0], "dcb")
    cas_dcb_dir = os.path.join(main_dir, "products", "cas")

    find_file(obs_dir, site, file_list)
    find_file(nav_dir, "BRDC", file_list)
    find_file(products_dir, "SP3", file_list)
    find_file(products_dir, "CLK", file_list)
    find_file(products_dir, "sp3", file_list)
    find_file(products_dir, "clk", file_list)
    find_file(erp_dir, str(week), file_list)
    find_file(snx_dir, str(week), file_list)
    find_file(cas_dcb_dir, "BSX", file_list)

    dcb_types = ["P1C1", "P2C2", "P1P2"]
    for dcb_type in dcb_types:
        dcb_ind = "{}{}{:02d}".format(dcb_type, str_year[-2:], month)
        find_file(code_dcb_dir, dcb_ind, file_list)

    for file in file_list:
        print("[INFO] Copy the file:",file,"to the save_dir")
        shutil.copy(file, save_dir)

def copy_from_gnss_input(save_dir):
    gnss_input_dir = r"C:\Users\LZ\Desktop\gnss_input"
    if os.path.exists(gnss_input_dir):
        atx_file = os.path.join(gnss_input_dir, "igs14.atx")
        ocean_file = os.path.join(gnss_input_dir, "ocnload.blq")
        shutil.copy(atx_file, save_dir)
        shutil.copy(ocean_file, save_dir)


if __name__ == "__main__":
    input = ["2022", "060", "wum", "YEL2"]

    save_dir = r"C:\Users\LZ\Desktop\gamp4"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    copy_from_rtkget_download(input, save_dir)
    copy_from_gnss_input(save_dir)
    rename_rinex(save_dir)
