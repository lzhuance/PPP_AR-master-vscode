# coding=utf-8
# !/usr/bin/env python

# pos文件设置
filelist = [r".\test_dynamic\KVH0_GC_DF_IF_FLOAT_B1IB3I.pos",
            r".\test_dynamic\KVH0_GC_DF_IF_FIX_OSB_B1IB3I.pos"]      # 文件路径
file_type = [5, 5]        # 文件类型[1:RTKLIB 2:GAMP 3:Net_Diff 4:IE 5:PPPAR_CC]

# 基准设置
# [1:静态基准坐标 2:snx文件+搜索静态站点 3:动态基准pos文件]
base_type = 3
# --------------------------------------------------------------
base_crd = []             # 静态基准站坐标
base_crd_type = 'LLH'     # 静态基准站坐标类型[LLH XYZ]
# --------------------------------------------------------------
snxfile = r''   # snx文件路径
site = 'ABPO'   # 搜索静态站点名
# --------------------------------------------------------------
base_file = r'.\test_dynamic\Coor_2021196_base-KVH0.pos'       # 动态基准POS文件路径
base_file_type = 3    # 动态基准POS文件类型[1:RTKLIB 2:GAMP 3:Net_Diff 4:IE 5:PPPAR_CC]

# 绘图设置(若不进行设置请默认为空)
xlimit = []                          # x轴上下限
ylimit = [-0.5, 0.5]                          # y轴上下限
xlabel = 'GPST--second of week[s]'
ylabel = 'Error[m]'
legend_list = ['PPP-float', 'PPP-fix']  # 图例
title_str = 'POS File Compare'          # 标题
savefig_dir = r'.\test_dynamic\KVH.pos.png'   #图片保存路径
