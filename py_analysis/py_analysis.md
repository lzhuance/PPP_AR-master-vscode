py_analysis file structure
```  
|-- \test_dynamic  测试动态数据pos文件
|-- \test_static   测试静态数据pos文件
    |-- __ init __.py
    |-- batch_analysis.py 批量分析PPP_AR pos文件并将定位误差收敛时间结果生成csv
    |-- copy_gnss_files_to_gamp_dir.py  将ppp所需文件复制至一个文件夹下
    |-- gnss_crd.py             gnss坐标系库函数  
    |-- gnss_time.py            gnss时间库函数
    |-- main.py                 pos绘图主函数
    |-- mymath.py               自定计算函数
    |-- plot_config.py          绘图默认配置文件
    |-- plot_config_dynamic.py  动态数据绘图示例配置文件
    |-- plot_config_static.py   静态数据绘图示例配置文件
    |-- read_pos.py             pos文件读取函数
    |-- rinex_long2short.py     rinex长文件命名批量转短文件命名


Need to be expanded!
