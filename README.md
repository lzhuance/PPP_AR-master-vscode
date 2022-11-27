This is demo for multi-GNSS precise point positioning with ambiguity resolution (PPP-AR), which is based on RTKLIB and RTKLIB_demo5.

FEATURES

1. ppp-ar with different type products
2. others

ENVIRONMENT

WIN10 + CLION2019.3 + TDM(can be foun in ./ide folder)

DATA

Example data can be found in /PPP_AR/GNSS_DATA.7z, please unzip.

CMD

fix solution：  YOUR_PATH/PPP_AR/build/Bin/ppp_ar.exe -C YOUR_PATH/conf/PPP/ppp_mgex_wum.conf -S G -M PPP-KINE(or PPP-STATIC) -A 7 -L 0  

float solution: YOUR_PATH/PPP_AR/build/Bin/ppp_ar.exe -C YOUR_PATH/conf/PPP/ppp_mgex_wum.conf -S G -M PPP-KINE(or PPP-STATIC) -A 0 -L 0 

NOTE

Please set 'pos1-prcdir' in configuration file to your local path

Support by 'Assessment of GPS/Galileo/BDS precise point positioning with ambiguity resolution using products from different analysis centers, Remote Sensing (under review)'

SOMETHING SHOULD BE IMPROVED BY YOURSELF.  
&nbsp;  
&nbsp;
## The following information are updated by liuzan:  
### Histroy:  
2022/11/27: organize source code and analysis tools  

### File structure
```  
|-- .vscode     存放vscode调试配置
|-- bin         存放编译得到的exe
|-- conf        存放示例配置文件
|-- exe         存放示例bat批处理文件
|-- GNSS_DATA   存放示例GNSS原始数据
|-- ide         存放TDM-GCC编译器下载器
|-- include     存放源码头文件rtklib.h
|-- py_analysis 存放python绘图及分析工具（新增）
|-- rtklib_bin  存放rtklib分析工具rtkplot和数据下载工具rtkget（新增）
|-- src         存放源码
```
### Main improvement
1、add CAS BIA file  
2、enable single BDS-3 PPP  
3、enable BDS-3 B1C/B2a IF PPP float solution with both CAS DCB and BIA file
4、expand the PCO struct to enable BDS-3 B1C

### Bug
When BeiDou is not included in PPP fix solution, the bd3opt must not be set as b2/3.