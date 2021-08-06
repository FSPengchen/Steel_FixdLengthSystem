# 配置文件
import Config

config_ini = Config.Config(path=r"E:\PycharmProjects\FixedLengthSystem", pathconfig='config.ini')
config_fur = Config.Config(path=r"E:\PycharmProjects\FixedLengthSystem", pathconfig='FurNum.ini')

public_dict = {
    'temp_changesteelDensityname': 0,  # 修改密度下的临时变量
    'temp_changesteelFixleng': 0,  # 修改定尺下的定尺
    'temp_Lne_Frame_cut_Y0_F1': 0,  # 1流切割Y轴位置点
    'temp_Lne_Frame_cut_Y0_F2': 0,  # 2流切割Y轴位置点
    'temp_Lne_Frame_cut_Y0_F3': 0,  # 3流切割Y轴位置点
    'temp_Lne_Frame_cut_Y0_F4': 0,  # 4流切割Y轴位置点
    'temp_Lne_Frame_cut_Y1_F1': 0,  # 1流切割Y轴位置点
    'temp_Lne_Frame_cut_Y1_F2': 0,  # 2流切割Y轴位置点
    'temp_Lne_Frame_cut_Y1_F3': 0,  # 3流切割Y轴位置点
    'temp_Lne_Frame_cut_Y1_F4': 0,  # 4流切割Y轴位置点
}

list_SteelData = []
BUTTONDOWNa = []
BUTTONDOWNb = []
