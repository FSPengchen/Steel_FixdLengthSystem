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
    'auto_adjustment_switch_F2': True,  # 2流自动调整模式开关
    'auto_adjustment_switch_F3': True,  # 3流自动调整模式开关
    'auto_adjustment_switch_F4': True,  # 4流自动调整模式开关
    'action_cut_1f': False,  # 1流切割发送至PLC布尔量
    'action_cut_2f': False,  # 2流切割发送至PLC布尔量
    'action_cut_3f': False,  # 3流切割发送至PLC布尔量
    'action_cut_4f': False,  # 4流切割发送至PLC布尔量
    '1f_rset_count_end': False, #1流切割复位计数结束标识 布尔量
    '2f_rset_count_end': False, #2流切割复位计数结束标识 布尔量
    '3f_rset_count_end': False,  # 3流切割复位计数结束标识 布尔量
    '4f_rset_count_end': False,  # 4流切割复位计数结束标识 布尔量
    'selected_status_F1': False,  # 选择1流修改切割线状态
    'selected_status_F2': False,  # 选择2流修改切割线状态
    'selected_status_F3': False,  # 选择3流修改切割线状态
    'selected_status_F4': False,  # 选择4流修改切割线状态
    'Weight_1f_list': [],  # 1流称重期间暂存数组
    'Weight_2f_list': [],  # 2流称重期间暂存数组
    'Weight_3f_list': [],  # 3流称重期间暂存数组
    'Weight_4f_list': [],  # 4流称重期间暂存数组
    'send_cut_1f_stat': False,  # 1流防止再次触发切割信号延时状态
    'send_cut_2f_stat': False,  # 2流防止再次触发切割信号延时状态
    'send_cut_3f_stat': False,  # 3流防止再次触发切割信号延时状态
    'send_cut_4f_stat': False,  # 4流防止再次触发切割信号延时状态
    'Weight_1f_list_stat': False,  # 1流状态称重期间缓冲数组，重量降为0时，清理数组
    'Weight_2f_list_stat': False,  # 2流状态称重期间缓冲数组，重量降为0时，清理数组
    'Weight_3f_list_stat': False,  # 3流状态称重期间缓冲数组，重量降为0时，清理数组
    'Weight_4f_list_stat': False,  # 4流状态称重期间缓冲数组，重量降为0时，清理数组
}

list_SteelData = []
BUTTONDOWNa = []
BUTTONDOWNb = []
