import _thread
import math
import cv2
import numpy as np
from scipy import stats
import logging
import time
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s > %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename='err.log',  # 日志存储文件
                    filemode='a'
                    )

def quantile_exc(data, n):  # 四分位数，其中data为数据组，n为第几个四分位数
    if n < 1 or n > 3:
        return False
    data.sort()
    position = (len(data) + 1) * n / 4
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer - 1]) * pos_decimal
    return quartile

def frameCut(frame_cut, cut_x0, cut_x1, cut_y0, cut_y1, fixlength, temp_Lne_Frame_cut_Y1, temp_Lne_Frame_cut_Y0,
             frame_cut_angle, setcutlimt, threshold, Start_Cut_state, threshold_ratio_switch, threshold_ratio=0.4, pullspeed=2.5, x_9=750, x_11=450, x_13=100, setcutlimt_selected_status=False):
    thickness = 2
    lineType = 4
    colors_Line = (255, 0, 0)
    # 创建字典，第一周期判断为空，只触发一周期的赋值切割
    return_dict = {'Start_Cut_state': Start_Cut_state, 'adjustment': 0}

    def send_cut_timer(name):
        return_dict['Start_Cut_state_F'] = False

    try:
        # 标尺直线框
        ptStart_angle = 450 * float(
            math.tan(math.radians(float(frame_cut_angle))))  # 倾斜距离

        # 根据四个点的坐标绘制两线区间
        scale_line_return = scale_line(frame_cut, x1=int(cut_x0), y1=int(cut_y0), x2=int(cut_x1), y2=int(cut_y1), cut_x=int(setcutlimt), fixlength=int(fixlength), n1=int(frame_cut_angle), x_9=x_9, x_11=x_11, x_13=x_13)
        return_dict['adjustment'] = scale_line_return['adjustment']
        return_dict['setfixlength_x'] = scale_line_return['setfixlength_x']
        return_dict['setfixlength_geshu_x'] = scale_line_return['setfixlength_geshu_x']
        return_dict['num'] = scale_line_return['num']

        # 设置切割线
        # 切割线变化的颜色
        if setcutlimt_selected_status == True:
            setcutlimt_line_color = (255, 255, 0)
        else:
            setcutlimt_line_color = (0, 255, 0)

        set_line(frame_cut, x1=int(cut_x0), y1=int(cut_y0), x2=int(cut_x1), y2=int(cut_y1), cut_x=int(setcutlimt), n1=int(frame_cut_angle), line_color=setcutlimt_line_color)
        # 切割区域

        # 判断 Y轴值的大小,修改切割图像方式
        if cut_y0 <= cut_y1:
            frame_cut_f1_temp = frame_cut[int(cut_y0 - int(frame_cut_angle)):int(cut_y1), int(cut_x0):int(cut_x1)]
        else:
            frame_cut_f1_temp = frame_cut[int(cut_y1 - int(frame_cut_angle)):int(cut_y0), int(cut_x0):int(cut_x1)]

        # 深度复制，不动原图
        frame_cut_f1_temp_gray = frame_cut_f1_temp.copy()
        # 图像处理
        gray = cv2.cvtColor(frame_cut_f1_temp_gray, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)  # 高斯

        # 判断阈值 = 设定阈值 *  拉速 * 阈值比例
        if float(pullspeed) >= 1.6 and float(threshold_ratio) <= 0.8 and float(
                threshold_ratio) >= 0.2 and threshold_ratio_switch == True:
            ret, thresh = cv2.threshold(blurred, int(threshold) * float(pullspeed) * float(threshold_ratio), 255,
                                        cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        else:
            ret, thresh = cv2.threshold(blurred, int(threshold), 255,
                                        cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓
        frame_cut_f1_temp_gray = cv2.drawContours(frame_cut_f1_temp_gray, contours, -1, (0, 0, 255), 3)  # -1 全部轮廓画出来

        # 腐蚀
        kernel = np.ones((3, 3), np.uint8)
        frame_cut_f1_temp_gray = cv2.erode(frame_cut_f1_temp_gray, kernel, iterations=1)
        # cv2.imshow(str(cut_y0),frame_cut_f1_temp_gray)    # 切割钢坯图像

        # 图像判断
        contoursX_list = []  # 空的图形X轴数据
        contoursY_list = []  # 空的图形Y轴数据

        # print("一共有多少个" + str(len(contours)))  # 图形数量

        steelMasterFlow = None
        for i in range(0, len(contours)):
            cnt = contours[i]
            # print('图形面积', cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 5000.0:  # 判断出大面积
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
            # if len(contoursX_list) > 10:
            #     for i in range(0, 7):
            #         minX_list.append(np.min(contoursX_list))
            #         contoursX_list.remove(np.min(contoursX_list))
            #
            # # 四分位数
            # if len(minX_list) >= 7:
            #     # print('minX_list', minX_list)
            #     quantile_minX_list2 = quantile_exc(minX_list, 2)
            #
            # else:
            quantile_minX_list2 = np.min(contoursX_list)
            # print("第1四分位数", quantile_minX_list2)

            # 钢坯头部位置提示线
            set_line(frame_cut, x1=int(cut_x0), y1=int(cut_y0), x2=int(cut_x1), y2=int(cut_y1), cut_x=int(quantile_minX_list2),
                       n1=int(frame_cut_angle))


            # print('X轴图形众值', stats.mode(contoursX_list)[0][0])
            # print('切割设定值', setcutlimt)
            # cv2.imshow(str(cut_y0), frame_cut_f_temp) # 这个开启
            # print('跟踪最小值',cut_y0,quantile_minX_list2)
            # print('切割设定值',cut_y0,setcutlimt)
            # 限制切割线及切割线-10位置范围内触发切割

            if int(quantile_minX_list2) <= int(setcutlimt) and int(quantile_minX_list2) >= int(int(setcutlimt) - 20):
                if return_dict['Start_Cut_state'] == False:
                    # 触发一个周期的赋值
                    return_dict['Start_Cut_state'] = True
                    # print(cut_y0, "钢坯切割")
                    return_dict['Start_Cut_state_F'] = True
                    logging.info('第{}流坐标,钢坯切割时间{},跟踪值{}'.format(cut_y0, int(time.time()), quantile_minX_list2))

                else:
                    return_dict['Lab_fcState'] = '钢坯切割'
                    return_dict['Start_Cut_state_F'] = False
                    # print(cut_y0, "已触发切割")
                    logging.info('第{}流坐标,已触发切割时间{},跟踪值{}'.format(cut_y0, int(time.time()), quantile_minX_list2))
                return return_dict

            else:
                return_dict['Lab_fcState'] = '钢坯跟踪'
                return_dict['Start_Cut_state_F'] = False
                logging.info('第{}流坐标,钢坯跟踪时间{},跟踪值{}'.format(cut_y0, int(time.time()), quantile_minX_list2))
                return return_dict
    except Exception as e:
        print(e)

# 刻度线
def scale_line(img, fixlength, x1=0, y1=400, x2=900, y2=420, x_9=750, x_11=450, x_13=100, cut_x = 200, n1=60):
    # 展示直线
    font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
    return_dict ={}



    if y1 != y2:
        # 获取线属性
        k1 = float((y2 - y1)) / float((x2 - x1))
        B = float(((x2 - x1) * y1 - (y2 - y1) * x1)) / float(x2 - x1)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2, 8)
        cv2.line(img, (x1, y1 - n1), (x2, y2 - n1), (255, 0, 0), 2, 8)

        y_13 = k1 * x_13 + B
        y_11 = k1 * x_11 + B
        y_9 = k1 * x_9 + B

        cut_y = k1 * cut_x + B
        # 绘制X_13的点
        cv2.circle(img, (int(x_13), int(y_13)), 2, (0, 0, 255), 2)
        cv2.putText(img, '13', (x_13 -15, int(y_13) +20), font, 0.5, (0, 255, 0), 2)# 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
        # 绘制X_11的点
        cv2.circle(img, (int(x_11), int(y_11)), 2, (0, 0, 255), 2)
        cv2.putText(img, '12', (x_11 - 15, int(y_11) + 20), font, 0.5, (0, 255, 0), 2)
        # 绘制X_9的点
        cv2.circle(img, (int(x_9), int(y_9)), 2, (0, 0, 255), 2)
        cv2.putText(img, '11', (x_9 - 15, int(y_9) + 20), font, 0.5, (0, 255, 0), 2)

        distance_11_9 = math.sqrt((x_9 - x_11) * (x_9 - x_11) + (y_9 - y_11) * (y_9 - y_11))
        # print('11到9之间的距离', distance_11_9)

        num = 50  # 刻度段数
        for i in range(num):
            # 绘制刻度线上的间隔
            distance_x_11_9 = x_11 + (i * (x_9 - x_11) / num)
            distance_y_11_9 = k1 * distance_x_11_9 + B
            # print('3', distance_x_11_9, distance_y_11_9)
            cv2.circle(img, (int(distance_x_11_9), int(distance_y_11_9)), 1, (0, 255, 255), 1)

            distance_x_13_11 = x_13 + (i * (x_11 - x_13) / num)
            distance_y_13_11 = k1 * distance_x_13_11 + B
            # print('3', distance_x_11_9, distance_y_11_9)
            cv2.circle(img, (int(distance_x_13_11), int(distance_y_13_11)), 1, (0, 255, 255), 1)

        D2 = n1
        # 判断Y轴的值
        if y1 != y2:
            cuizhi_k = - 1 / k1
        elif y1 == y2:
            cuizhi_k =0
        # B1=-K1*X1+Y1
        cuizhi_B = -1 * (cuizhi_k * cut_x) + cut_y

        keduxian_x11_9_1 = math.sqrt(D2 * D2 / (1 + cuizhi_k*cuizhi_k)) + cut_x
        keduxian_y11_9_1 = (-1 / k1) * keduxian_x11_9_1 + cuizhi_B

        # cv2.line(img, (int(cut_x), int(cut_y)), (int(keduxian_x11_9_1), int(keduxian_y11_9_1)), (255, 255, 0), 2, 8)
        # 设置输入X轴画出两线间的线段

        # 获取定尺长度，判断格数
        if 12000 > int(fixlength) >= 11000:

            setfixlength_x = (((x_9 - x_11) * (12000 - fixlength) + 1000 * x_11) / 1000)
            # print(str(y1), 'setfixlength_x ', setfixlength_x)
            setfixlength_y = k1 * setfixlength_x + B

            cv2.circle(img, (int(setfixlength_x), int(setfixlength_y)), 3, (0, 255, 255), 3)

        elif 13000 > int(fixlength) >= 12000:
            setfixlength_x = ((x_11 - x_13) * (13000 - fixlength) + 1000 * x_13) / 1000
            # print(str(y1),'setfixlength_x ',setfixlength_x)
            setfixlength_y = k1 * setfixlength_x + B

            cv2.circle(img, (int(setfixlength_x), int(setfixlength_y)), 3, (0, 255, 255), 3)
        else:
            # print('输入数值不对')
            pass

        # 定尺值坐标转换格数
        if setfixlength_x < x_11:
            setfixlength_geshu_x = (num * (setfixlength_x - x_13)) / (x_11 - x_13)
        elif setfixlength_x >= x_11:
            setfixlength_geshu_x = (num * (setfixlength_x - x_11)) / (x_9 - x_11) + num

        # print(str(y1), setfixlength_geshu_x, '定尺值坐标转换格数')


        # 切割设定值坐标转换格数
        if cut_x < x_11:
            geshu_x = (num * (cut_x - x_13)) / (x_11 - x_13)
        elif cut_x >= x_11:
            geshu_x = (num * (cut_x - x_11)) / (x_9 - x_11) + num

        # print(str(y1), '切割设定值坐标转换格数', geshu_x)

        # 定尺值格数 - 切割设定值格数 = 微调值格数
        return_dict['adjustment'] = float(setfixlength_geshu_x) - float(geshu_x)
        # print(return_dict['adjustment'])


        # 须测试是否正确
        # 格数转坐标

        # geshu_x = 1  返回的计算值不同
        if geshu_x < 50:
            zuobiao_x = ((geshu_x * x_11) - (geshu_x * x_13) + (num * x_11)) / num - (x_11 - x_13)
        elif geshu_x >= 50:
            zuobiao_x = ((geshu_x * x_9) - (geshu_x * x_11) + (num * x_9)) / num - (x_9 - x_13)
        # print(str(y1), '转换后x坐标', zuobiao_x, cut_x)

        # 返回1格度 = 多少X坐标
        #  主程序  直接 减去 N*格数坐标

        # 将跟踪坐标转换为重量以及长度

        return_dict['setfixlength_x'] = setfixlength_x
        return_dict['setfixlength_geshu_x'] = setfixlength_geshu_x
        return_dict['num'] = num
        return return_dict


    else:
        # 画直线
        cv2.line(img, (x1, y1), (x2, y1), (255, 0, 0), 2, 8)
        cv2.line(img, (x1, y1 - n1), (x2, y1 - n1), (255, 0, 0), 2, 8)

        # 校对点
        cv2.circle(img, (int(x_13), int(y1)), 2, (0, 0, 255), 2)
        cv2.putText(img, '13', (x_13 - 15, y1 + 15), font, 0.5, (0, 255, 0), 2)  # 图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
        cv2.circle(img, (int(x_11), int(y1)), 2, (0, 0, 255), 2)
        cv2.putText(img, '12', (x_11 - 15, y1 + 15), font, 0.5, (0, 255, 0), 2)
        cv2.circle(img, (int(x_9), int(y1)), 2, (0, 0, 255), 2)
        cv2.putText(img, '11', (x_9 - 15, y1 + 15), font, 0.5, (0, 255, 0), 2)

        num = 50
        for i in range(num):
            distance_x_11_9 = x_11 + (i * (x_9 - x_11) / num)
            # print('3', distance_x_11_9, distance_y_11_9)
            cv2.circle(img, (int(distance_x_11_9), int(y1)), 1, (0, 255, 255), 1)

            distance_x_13_11 = x_13 + (i * (x_11 - x_13) / num)
            # print('3', distance_x_11_9, distance_y_11_9)
            cv2.circle(img, (int(distance_x_13_11), int(y1)), 1, (0, 255, 255), 1)


        # 获取定尺长度，判断格数
        if 12000 > int(fixlength) >= 11000:

            setfixlength_x = (((x_9 - x_11) * (12000 - fixlength) + 1000 * x_11) / 1000)
            # print(str(y1), 'setfixlength_x ', setfixlength_x)
            setfixlength_y = y1

            cv2.circle(img, (int(setfixlength_x), int(setfixlength_y)), 3, (0, 255, 255), 3)

        elif 13000 > int(fixlength) >= 12000:
            setfixlength_x = ((x_11 - x_13) * (13000 - fixlength) + 1000 * x_13) / 1000
            # print(str(y1),'setfixlength_x ',setfixlength_x)
            setfixlength_y = y1

            cv2.circle(img, (int(setfixlength_x), int(setfixlength_y)), 3, (0, 255, 255), 3)
        else:
            print('输入数值不对')

        # 定尺值坐标转换格数
        if setfixlength_x < x_11:
            setfixlength_geshu_x = (num * (setfixlength_x - x_13)) / (x_11 - x_13)
        elif setfixlength_x >= x_11:
            setfixlength_geshu_x = (num * (setfixlength_x - x_11)) / (x_9 - x_11) + num

        # print(str(y1), setfixlength_geshu_x, '定尺值坐标转换格数')

        # 切割设定值坐标转换格数
        if cut_x < x_11:
            geshu_x = (num * (cut_x - x_13)) / (x_11 - x_13)
        elif cut_x >= x_11:
            geshu_x = (num * (cut_x - x_11)) / (x_9 - x_11) + num
        # print(str(y1), '坐标转换格数', geshu_x)

        # 定尺值格数 - 切割设定值格数 = 微调值格数
        return_dict['adjustment'] = float(setfixlength_geshu_x) - float(geshu_x)
        # print(return_dict['adjustment'])

        # 格数转坐标
        if geshu_x < 50:
            zuobiao_x = ((geshu_x * x_11) - (geshu_x * x_13) + (num * x_11)) / num - (x_11 -x_13)
        elif geshu_x >= 50:
            zuobiao_x = ((geshu_x * x_9) - (geshu_x * x_11) + (num * x_9)) / num - (x_9 - x_13)
        # print(str(y1), '转换后x坐标', zuobiao_x,cut_x)

        # 返回1格度 = 多少X坐标
        #  主程序  直  接 减去 N*格数坐标
        return_dict['setfixlength_x'] = setfixlength_x
        return_dict['setfixlength_geshu_x'] = setfixlength_geshu_x
        return_dict['num'] = num
        return return_dict

    # 设置输入X轴画出两线间的线段
def set_line(img, x1=0, y1=400, x2=900, y2=420, cut_x = 200, n1=60,line_color=(255, 0, 0)):
    if y1 != y2:
        if y1 < y2:
            # 展示直线
            k1 = float((y2 - y1)) / float((x2 - x1))    # 斜率
            B = float(((x2 - x1) * y1 - (y2 - y1) * x1)) / float(x2 - x1)
            # print(str(y1),'k1', k1, 'B', B)
            cut_y = k1 * cut_x + B  # 输入X轴值,获得Y轴值

            D2 = n1
            # 垂直斜率
            cuizhi_k = - 1 / k1
            # B1=-K1*X1+Y1
            cuizhi_B = -1 * (cuizhi_k * cut_x) + cut_y

            # 两线间的直线
            keduxian_x11_9_1 = math.sqrt(D2 * D2 / (1 + cuizhi_k*cuizhi_k)) + cut_x
            keduxian_y11_9_1 = (-1 / k1) * keduxian_x11_9_1 + cuizhi_B
            cv2.line(img, (int(cut_x), int(cut_y)), (int(keduxian_x11_9_1), int(keduxian_y11_9_1)),line_color, 2, 8)


        elif y1 > y2:
            # 展示直线
            k1 = float((y2 - y1)) / float((x2 - x1))  # 斜率
            # B = float(((x1 - x2) * y2 - (y1 - y2) * x1)) / float((x1 - x2))
            B = float(((x2 - x1) * y1 - (y2 - y1) * x1)) / float(x2 - x1)
            # B =y1 - k1 *x1
            # print(str(y1),'k1',k1,'B',B)
            cut_y = k1 * cut_x + B   # 输入X轴值,获得Y轴值

            D2 = n1
            # 垂直斜率
            cuizhi_k = - 1 / k1

            # 上端线交点的坐标
            keduxian_x11_9_1 = cut_x - math.sqrt(D2 * D2 / (1 + cuizhi_k*cuizhi_k))
            keduxian_y11_9_1 = k1 * keduxian_x11_9_1 + B - n1
            # keduxian_y11_9_1 = (-1 / k1) * keduxian_x11_9_1 + cuizhi_B
            # print(str(y1),'keduxian_x11_9_1',keduxian_x11_9_1)
            # print(str(y1),'keduxian_y11_9_1',keduxian_y11_9_1)
            # keduxian_y11_9_1 = (-1*cut_x / k1) + cut_y + (cut_x / k1)

            cv2.line(img, (int(cut_x), int(cut_y)), (int(keduxian_x11_9_1), int(keduxian_y11_9_1)), line_color, 2, 8)

    else:
        cut_y = y1 - n1
        cv2.line(img, (int(cut_x), int(y1)), (int(cut_x), int(cut_y)), line_color, 2, 8)
