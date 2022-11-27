# coding=utf-8
# !/usr/bin/env python

# pos文件设置
#filelist = [r".\test_static\abpo0010.rtklib.pos",
#            r".\test_static\abpo0010.gamp.pos",
#            r".\test_static\abpo0010.demo5.pos",
#           r".\test_static\abpo0010.pppar.pos",
#            r".\test_static\abpo0010.net_diff.pos"]      # 文件路径
filelist = [r".\test_static\abpo0010.rtklib.pos",
            r".\test_static\abpo0010.ppp_G.pos",]
file_type = [1, 1]        # 文件类型[1:RTKLIB 2:GAMP 3:Net_Diff 4:IE 5:PPPAR_CC]

# 基准设置
# [1:静态基准坐标 2:snx文件+搜索静态站点 3:动态基准pos文件]
base_type = 2
# --------------------------------------------------------------
base_crd = []             # 静态基准站坐标
base_crd_type = 'LLH'     # 静态基准站坐标类型[LLH XYZ]
# --------------------------------------------------------------
snxfile = r'.\test_static\igs22P2199.snx'   # snx文件路径
site = 'ABPO'                                          # 搜索静态站点名
# --------------------------------------------------------------
base_file = r''       # 动态基准POS文件路径
base_file_type = 3    # 动态基准POS文件类型[1:RTKLIB 2:GAMP 3:Net_Diff 4:IE 5:PPPAR_CC]

# 绘图设置(若不进行设置请默认为空)
xlimit = []                          # x轴上下限
ylimit = [-0.2,0.2]                          # y轴上下限
xlabel = 'GPST--second of week[s]'
ylabel = 'Error[m]'
legend_list = ['rtklib']  # 图例
title_str = 'POS File Compare'       # 标题
savefig_dir = r'.\test_static\ABPO.pos.svg'   #图片保存路径
