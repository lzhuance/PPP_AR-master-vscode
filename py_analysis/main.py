# coding=utf-8
# !/usr/bin/env python
"""
Program:plot_pos_error
Function: plot pos error in ENU
Author:LZ_CUMT
Version:1.0
Date:2022/04/12
"""
import shutil
from plot_config_dynamic import *
from gnss_crd import *
from read_pos import readpos
import matplotlib.pyplot as plt
import numpy as np
from mymath_numpy import math_rms_percent

# convert sow to strtime (86400 --> 00:00:00)
def sow2hourtime(sow):
    sod = sow%86400
    hour = sod/3600
    return hour

# get the base coordinate
def get_base(base_type):
    if base_type == 1:
        # get base with the input coordinate
        if base_crd_type == 'LLH':
            return llh2xyz(np.array(base_crd))
        elif base_crd_type == 'XYZ':
            return np.array(base_crd)
        else:
            print('[Error] Wrong base_crd_type')
            exit(0)
    elif base_type == 2:
        # find site coordinate from snx file with site name
        return getcrd(site, snxfile)
    elif base_type == 3:
        # get base coordinate from dynamic pos file
        return readpos(base_file, base_file_type)
    else:
        print('[Error] Wrong base_type')
        exit(0)


if __name__ == '__main__':
    # set the config file dir
    cfg_file = 'plot_config_dynamic.py'   # change the config file here!
    shutil.copyfile(cfg_file, 'plot_config.py')
    from plot_config import *
    #from matplotlib import rcParams
    #config = {
    #    "font.family": 'serif',  # 衬线字体
    #    "font.size": 12,  # 相当于小四大小
    #    "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    #    "font.serif": ['STSong'],  # 宋体
    #    'axes.unicode_minus': False  # 处理负号，即-号
    #}
    #rcParams.update(config)

    # get the base coordinate
    base = get_base(base_type)

    # set the number of subplot
    fig, ax = plt.subplots(3, 1, sharex='col')

    # repeat plot with the number of files in filelist
    for i in range(len(filelist)):
        # read pos file
        data = readpos(filelist[i], file_type[i])
        sow = data[:, 1]
        xyz = data[:, 2:]

        # expand base to base_all and align to data by sow
        base_all = np.zeros(xyz.shape)
        if base_type == 1 or base_type == 2:
            for j in range(xyz.shape[0]):
                base_all[j, :] = base
        elif base_type == 3:
            index = 0
            for j in range(xyz.shape[0]):
                for k in range(index, base.shape[0]):
                    if base[k, 1] == sow[j]:
                        base_all[j, :] = base[k, 2:]
                        index = k  # record the search index and use it in the next epoch (shorten the search time)
                        break

        # calculate ENU with xyz and base_all
        enu = np.zeros(xyz.shape)
        for j in range(xyz.shape[0]):
            if base_all[j, 0] != 0:
                enu[j, :] = xyz2enu(xyz[j, :], base_all[j, :])
            else:
                enu[j, :] = [0, 0, 0]

        print(math_rms_percent(enu, 100))
        print(math_rms_percent(enu, 95))

        # convert sow to hourtime
        strtime = []
        for j in range(xyz.shape[0]):
            strtime.append(sow2hourtime(sow[j]))
        # Start single pos file plot
        for j in range(3):
            ax[j].plot(strtime, enu[:, j])
            if not xlimit == []:
                ax[j].set_xlim((xlimit[0], xlimit[1]))
            if not ylimit == []:
                ax[j].set_ylim((ylimit[0], ylimit[1]))
            ax[j].grid(linestyle='--')
            if j == 2 and xlabel != '':
                ax[j].set_xlabel(xlabel)
            if j == 1 and ylabel != '':
                ax[j].set_ylabel(ylabel)
            # change xticks from sow to strtime (86400 --> 00:00:00)
            # step = int(xyz.shape[0]/4)
            # ax[j].set_xticks(sow.tolist()[::step])
            # ax[j].set_xticklabels(strtime[::step])

    # set the overall information about plot
    if len(title_str) > 0:
        ax[0].set_title(title_str)
    ax[0].legend(legend_list, ncol=len(legend_list))
    plt.savefig(savefig_dir, dpi=400)
    plt.show()
