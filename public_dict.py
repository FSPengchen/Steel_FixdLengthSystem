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
    'temp_Lab_1bWeight': 0,  # 1流称重重量
    'temp_Lab_2bWeight': 0,  # 2流称重重量
    'temp_Lab_3bWeight': 0,  # 3流称重重量
    'temp_Lab_4bWeight': 0,  # 4流称重重量
    'temp_Lab_1bTemperature': 0,  # 1流温度
    'temp_Lab_2bTemperature': 0,  # 2流温度
    'temp_Lab_3bTemperature': 0,  # 3流温度
    'temp_Lab_4bTemperature': 0,  # 4流温度
    'temp_Lab_1cCompensate': 0.00,  # 1流补偿值
    'temp_Lab_2cCompensate': 0.00,  # 2流补偿值
    'temp_Lab_3cCompensate': 0.00,  # 3流补偿值
    'temp_Lab_4cCompensate': 0.00,  # 4流补偿值
    # 切割PLC变量
    'plc_cut_IsSuccess': False,  # 切割PLC通讯状态
    'plc_weight_manual_F1': False,  # 1流称重模式
    'plc_weight_manual_F2': False,  # 2流称重模式
    'plc_weight_manual_F3': False,  # 3流称重模式
    'plc_weight_manual_F4': False,  # 4流称重模式
    'plc_weight_auto_F1': False,  # 1流称重模式
    'plc_weight_auto_F2': False,  # 2流称重模式
    'plc_weight_auto_F3': False,  # 3流称重模式
    'plc_weight_auto_F4': False,  # 4流称重模式
    'weiht_flag': True,  # 称重通断启用信号
    # 连铸PLC通讯变量
    'Start_Cut_state_F1': False,  # 1流切割状态标识
    'Start_Cut_state_F2': False,  # 2流切割状态标识
    'Start_Cut_state_F3': False,  # 3流切割状态标识
    'Start_Cut_state_F4': False,  # 4流切割状态标识
    'plc_weighting_F1': False,  # 1流在称重
    'plc_weighting_F2': False,  # 2流在称重
    'plc_weighting_F3': False,  # 3流在称重
    'plc_weighting_F4': False,  # 4流在称重
    'plc_public_IsSuccess': False,  # 连铸公共流PLC通讯状态
    'plc_1f_IsSuccess': False,  # 连铸1流PLC通讯状态
    'plc_2f_IsSuccess': False,  # 连铸2流PLC通讯状态
    'plc_3f_IsSuccess': False,  # 连铸3流PLC通讯状态
    'plc_4f_IsSuccess': False,  # 连铸4流PLC通讯状态
    'plc_1f_pullspeed': 0,  # 连铸1流PLC拉速
    'plc_2f_pullspeed': 0,  # 连铸2流PLC拉速
    'plc_3f_pullspeed': 0,  # 连铸3流PLC拉速
    'plc_4f_pullspeed': 0,  # 连铸4流PLC拉速
    'weighting_F1_state': '否',  # 临时写入状态
    'weighting_F2_state': '否',  # 临时写入状态
    'weighting_F3_state': '否',  # 临时写入状态
    'weighting_F4_state': '否',  # 临时写入状态
    'sql_weighting_F1': 0,  # 写入SQL重量
    'sql_weighting_F2': 0,  # 写入SQL重量
    'sql_weighting_F3': 0,  # 写入SQL重量
    'sql_weighting_F4': 0,  # 写入SQL重量
    'auto_adjustment_switch_F1': True,  # 1流自动调整模式开关




}

list_SteelData = []
BUTTONDOWNa = []
BUTTONDOWNb = []
