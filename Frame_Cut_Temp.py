import math
import cv2
import numpy as np
from scipy import stats

def quantile_exc(data, n):  # 四分位数，其中data为数据组，n为第几个四分位数
    if n < 1 or n > 3:
        return False
    data.sort()
    position = (len(data) + 1) * n / 4
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer - 1]) * pos_decimal
    return quartile

def frameCut(frame_cut, cut_x0, cut_x1, cut_y0, cut_y1, temp_Lne_Frame_cut_Y1, temp_Lne_Frame_cut_Y0,
             frame_cut_angle, setcutlimt, threshold, Start_Cut_state, threshold_ratio=0.4, pullspeed=2.5):
    thickness = 2
    lineType = 4
    colors_Line = (255, 0, 0)
    # 创建字典，第一周期判断为空，只触发一周期的赋值切割
    # print('Start_Cut_state',Start_Cut_state)
    return_dict = {'Start_Cut_state': Start_Cut_state}
    # print('字典长度', len(return_dict))

    try:
        # 标尺直线框
        ptStart_angle = 450 * float(
            math.tan(math.radians(float(frame_cut_angle))))  # 倾斜距离
        ptStart_up = (
            0, int(float(cut_y0) - float(ptStart_angle)))  # 直线开始点
        pt1End_up = (
            900, int(float(cut_y0) + float(ptStart_angle)))  # 直线结束点
        cv2.line(frame_cut, ptStart_up, pt1End_up, colors_Line, thickness, lineType)

        ptStart_down = (
            0, int(float(cut_y1) - float(ptStart_angle)))  # 直线开始点
        pt1End_down = (
            900, int(float(cut_y1) + float(ptStart_angle)))  # 直线结束点
        cv2.line(frame_cut, ptStart_down, pt1End_down, colors_Line, thickness, lineType)

        # 切割区域,图像旋转仿射

        frame_cut_f1_temp = frame_cut[int(cut_y0):int(cut_y1), int(cut_x0):int(cut_x1)]
        frame_cut_f1_temp_height = int(cut_y1) - int(cut_y0)
        frame_cut_f1_temp_width = int(cut_x0) - int(cut_x1)
        M = cv2.getRotationMatrix2D((frame_cut_f1_temp_width / 2, frame_cut_f1_temp_height / 2),
                                    float(frame_cut_angle) / 2,
                                    1)  # 旋转 (中心,旋转角度，缩放)
        # 切割后的流图像
        frame_cut_f_temp = cv2.warpAffine(frame_cut_f1_temp, M,
                                          (frame_cut_f1_temp_width,
                                           frame_cut_f1_temp_height))  # 仿射（原始图片，不同变换矩阵实现不同仿射，尺寸大小）
        # print(frame_cut_f1_temp_width, frame_cut_f1_temp_width)
        # cv2.imshow(str(cut_y0), frame_cut_f_temp)

        # 图像处理
        gray = cv2.cvtColor(frame_cut_f_temp, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)  # 高斯
        # 判断阈值 = 设定阈值 * 拉速 * 阈值比例
        if float(pullspeed) >= 1.6 or float(threshold_ratio) <= 0.8 or float(threshold_ratio) >= 0.2 :
            ret, thresh = cv2.threshold(blurred, int(threshold) * float(pullspeed) * float(threshold_ratio), 255,
                                        cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        else:
            ret, thresh = cv2.threshold(blurred, int(threshold), 255,
                                        cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓
        frame_cut_f_temp = cv2.drawContours(frame_cut_f_temp, contours, -1, (0, 0, 255), 3)  # -1 全部轮廓画出来
        kernel = np.ones((3, 3), np.uint8)
        frame_cut_f_temp = cv2.erode(frame_cut_f_temp, kernel, iterations=1)

        # 设置切割线位置
        ptLimt_angle_X = int(int(temp_Lne_Frame_cut_Y1) - int(temp_Lne_Frame_cut_Y0)) * float(
            math.tan(math.radians(float(frame_cut_angle))))
        # ptLimt_angle_X = int(temp_Lne_Frame_cut_Y1) * float(
        #     math.tan(math.radians(float(frame_cut_angle))))

        ptLimt_angle_Y = int(setcutlimt) * float(math.tan(math.radians(float(frame_cut_angle))))

        Limt_Start = (int(setcutlimt) + int(ptLimt_angle_X),
                      int(temp_Lne_Frame_cut_Y0) - int(ptLimt_angle_Y))  # 画线直线起点

        Limt_End = (int(setcutlimt) + int(ptLimt_angle_X),
                    int(temp_Lne_Frame_cut_Y1) - int(ptLimt_angle_Y))

        # print('起始点', Limt_Start, '结束点', Limt_End)

        cv2.line(frame_cut, Limt_Start, Limt_End, (255, 255, 0), thickness, lineType)

        # 图像判断
        contoursX_list = []  # 空的图形X轴数据
        contoursY_list = []  # 空的图形Y轴数据

        # print("一共有多少个" + str(len(contours)))  # 图形数量

        steelMasterFlow = None
        for i in range(0, len(contours)):
            cnt = contours[i]
            # print('图形面积', cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 9000.0:  # 判断出大面积
                # print("第" + str(i + 1) + "个是符合要求")  # 第几个大于要求
                steelMasterFlow = i  # 第几个图形
                # print("得出图形", contours[i])
                # print("图形边的数据:", len(contours[i]))  # 图形边框数量

                for j in range(0, len(contours[i])):
                    contoursX_list.append(contours[i][j][0][0])  # 增加图形中X轴的数据
                    contoursY_list.append(contours[i][j][0][1])  # 增加图形中Y轴的数据

        if steelMasterFlow is None and len(contoursX_list) == 0 and len(contoursY_list) == 0:  # 为空，则没有适合图形
            # print("没有符合钢坯要求面积的图形")
            return_dict['Start_Cut_state'] = False
            return_dict['Lab_fcState'] = '钢坯等待'
            return_dict['Start_Cut_state_F'] = False
            return return_dict

        else:
            if return_dict['Start_Cut_state'] == False:
                return_dict['Lab_fcState'] = '钢坯跟踪'
            # print("contoursXList X轴数值", contoursX_list)
            # print("contoursYList Y轴数值", contoursY_list)
            # print("最小值", min(contoursX_list))
            # print("X众数值", stats.mode(contoursX_list)[0][0])  # X众数值
            # print("Y众数值", stats.mode(contoursY_list)[0][0])  # Y众数值

            # 判断大于10个数的数组，取最小的7个数
            minX_list = []
            if len(contoursX_list) > 10:
                for i in range(0, 7):
                    minX_list.append(np.min(contoursX_list))
                    contoursX_list.remove(np.min(contoursX_list))

            # 第2四分位数
            quantile_minX_list2 = quantile_exc(minX_list, 2)
            print("第2四分位数", quantile_minX_list2)

            # 钢坯头部位置提示线
            ptStart_angle_X = int(
                int(temp_Lne_Frame_cut_Y1) - int(temp_Lne_Frame_cut_Y0)) * float(
                math.tan(math.radians(float(frame_cut_angle))))
            ptStart_angle_Y = int(
                int(temp_Lne_Frame_cut_Y1) - int(temp_Lne_Frame_cut_Y0)) * float(
                math.tan(math.radians(float(frame_cut_angle))))

            Line_Start = (
                int(quantile_minX_list2) + int(ptStart_angle_X), temp_Lne_Frame_cut_Y0)  # 画线直线起点
            Line_End = (
                int(quantile_minX_list2) - int(ptStart_angle_X), temp_Lne_Frame_cut_Y1)  # 画线直线终点
            print('quantile_minX_list2',quantile_minX_list2)
            print('min(contoursX_list)',min(contoursX_list))

            # int((int(temp_Lne_Frame_cut_Y0) + int(temp_Lne_Frame_cut_Y1)) / 2) #中间值
            # 跟踪钢坯头部线
            cv2.line(frame_cut, Line_Start, Line_End, (255, 15, 0), thickness, lineType)
            # print(Line_Start, Line_End)

            # print('X轴图形众值', stats.mode(contoursX_list)[0][0])
            # print('切割设定值', setcutlimt)
            # cv2.imshow(str(cut_y0), frame_cut_f_temp) # 这个开启
            if int(quantile_minX_list2) <= int(setcutlimt):
                if return_dict['Start_Cut_state'] == False:
                    # 触发一个周期的赋值
                    return_dict['Start_Cut_state'] = True
                    # print(cut_y0, "钢坯切割")
                    return_dict['Start_Cut_state_F'] = True

                else:
                    return_dict['Lab_fcState'] = '钢坯切割'
                    return_dict['Start_Cut_state_F'] = False
                    # print(cut_y0, "已触发切割")
                return return_dict
            else:
                return_dict['Lab_fcState'] = '钢坯跟踪'
                return_dict['Start_Cut_state_F'] = False
                return return_dict
    except Exception as e:
        print(e)
