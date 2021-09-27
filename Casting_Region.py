import math
import cv2
import numpy
from scipy import stats

'''
计算偏转角度以及画区域直线
'''


class casting_region():
    def __init__(self, frame_cut, cut_angle, cut_x0, cut_x1, cut_y0, cut_y1, colors_Line=(255, 0, 0), thickness=2, lineType=4,temp_Lne_Frame_cut_Y1, temp_Lne_Frame_cut_Y0, frame_cut_angle,setcutlimt, Limt_color=(0, 255, 255)):
        self.frame_cut_angle = cut_angle  # 读取旋转角度
        self.frame_cut_y0 = cut_y0  # 顶部坐标
        self.frame_cut_y1 = cut_y1  # 底部坐标
        self.frame_cut_x0 = cut_x0  # 顶部坐标
        self.frame_cut_x1 = cut_x1  # 底部坐标
        self.colors_Line = colors_Line  # 选择颜色
        self.thickness = thickness  # 线粗度
        self.lineType = lineType  # 线类型
        self.frame_cut = frame_cut  # 载入图像
        self.temp_Lne_Frame_cut_Y1 = temp_Lne_Frame_cut_Y1
        self.temp_Lne_Frame_cut_Y0 = temp_Lne_Frame_cut_Y0
        self.frame_cut_angle

        self.Lab_NumcState = '钢坯等待'
        self.Start_Cut_state = False

    def frame_line(self, frame_cut):
        # 标尺直线框
        ptStart_angle = 450 * float(math.tan(math.radians(self.frame_cut_angle)))  # 角度偏转高度

        ptStart_up = (0, int(float(self.frame_cut_y0) - float(ptStart_angle)))  # 直线开始点坐标

        pt1End_up = (900, int(float(self.frame_cut_y0) + float(ptStart_angle)))  # 直线结束点坐标

        cv2.line(self.frame_cut, ptStart_up, pt1End_up, self.colors_Line, self.thickness, self.lineType)  # 画直线

        ptStart_down = (0, int(float(self.frame_cut_y1) - float(ptStart_angle)))  # 直线开始点

        pt1End_down = (900, int(float(self.frame_cut_y1) + float(ptStart_angle)))  # 直线结束点

        cv2.line(self.frame_cut, ptStart_down, pt1End_down, self.colors_Line, self.thickness, self.lineType)  # 画直线

        # 设置切割线位置
        # ptLimt_angle_X = int(temp_Lne_Frame_cut_Y1 - int(temp_Lne_Frame_cut_Y0) * float(
        #     math.tan(math.radians(float(frame_cut_angle)))))
        ptLimt_angle_X = int(self.temp_Lne_Frame_cut_Y1) * float(
            math.tan(math.radians(float(self.frame_cut_angle))))

        ptLimt_angle_Y = int(self.setcutlimt) * float(math.tan(math.radians(float(self.frame_cut_angle))))

        Limt_Start = (int(self.setcutlimt) + int(ptLimt_angle_X),
                      int(self.temp_Lne_Frame_cut_Y0) - int(ptLimt_angle_Y))  # 画线直线起点

        Limt_End = (int(self.setcutlimt) + int(ptLimt_angle_X),
                    int(self.temp_Lne_Frame_cut_Y1) - int(ptLimt_angle_Y))

        print('起始点', Limt_Start, '结束点', Limt_End)

        cv2.line(frame_cut, Limt_Start, Limt_End, (255, 0, 0), self.thickness, self.lineType)

    # 切割区域,图像旋转仿射
    def frame_Rotation(self, frame_cut):
        '''
        :param frame_cut: 载入图像
        :return:
        '''
        frame_cut_temp = frame_cut[int(self.frame_cut_y0):int(self.frame_cut_y1),
                         int(self.frame_cut_x0):int(self.frame_cut_x1)]
        # 计算高度
        frame_cut_temp_height = int(self.frame_cut_y1) - int(self.frame_cut_y0)

        # 计算宽度
        frame_cut_temp_width = int(self.frame_cut_x1) - int(self.frame_cut_x1)

        # 旋转 (中心,旋转角度，缩放)
        M = cv2.getRotationMatrix2D((frame_cut_temp_width / 2, frame_cut_temp_height / 2),
                                    float(self.frame_cut_angle) / 2, 1)

        # 仿射（原始图片，不同变换矩阵实现不同仿射，尺寸大小）
        frame_cut_temp = cv2.warpAffine(frame_cut_temp, M,
                                        (
                                            frame_cut_temp_width,
                                            frame_cut_temp_height))

        # cv2.rectangle(frame_cut, (0, int(config_ini.readvalue('setcamre', 'frame_cut_y0'))), (
        # int(config_ini.readvalue('setcamre', 'frame_cut_x1')), int(config_ini.readvalue('setcamre', 'frame_cut_y1'))),
        #               colors, 2)  # 画矩形

        # cv2.imshow('frame_cut_temp',frame_cut_temp)
        # print(frame_cut_temp, type(frame_cut_temp))

        return frame_cut_temp

    # 图像处理
    def frame_cv2(self, frame_cut, threshold):
        '''
        :param frame_cut: load image
        :param threshold: threshold value
        :return:
        '''
        gray = cv2.cvtColor(frame_cut, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯
        ret, thresh = cv2.threshold(blurred, int(threshold), 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓
        frame_cut = cv2.drawContours(frame_cut, contours, -1, (0, 0, 255), 3)  # -1 全部轮廓画出来
        kernel = numpy.ones((3, 3), numpy.uint8)
        frame_cut_temp = cv2.erode(frame_cut, kernel, iterations=1)
        cv2.imshow('frame_cv2', frame_cut_temp)
        # print("一共有多少个" + str(len(contours)))    # 图形数量

        return contours  # 返回目标图像数量

    def frame_target_image(self, contours,setcutlimt):
        List_contoursX = []  # 空的图形X轴数据
        List_contoursY = []  # 空的图形Y轴数据
        steelMasterFlow = None  # 第几个图形为主图像，状态标签

        # print("一共有多少个图形数量" + str(len(contours)))
        for i in range(0, len(contours)):
            cnt = contours[i]  # 图形的数组数据
            # print('图形的面积:', cv2.contourArea(cnt))

            # 有符合面积要求的图像
            if cv2.contourArea(cnt) > 5000.0:  # 判断出大面积
                # print("第" + str(i + 1) + "个是大于要求")  # 第几个大于要求
                steelMasterFlow = i  # 第几个图形
                # print("得出图形", contours[i])
                # print("图形边框数量:", len(contours[i]))  # 图形边框数量
                # 将X轴与Y轴放到list

                for j in range(0, len(contours[i])):
                    List_contoursX.append(contours[i][j][0][0])  # 增加图形中X轴的数据
                    List_contoursY.append(contours[i][j][0][1])  # 增加图形中Y轴的数据

                    dict_return = {'Num_image': steelMasterFlow,  'Lab_NumcState': "钢坯跟踪"}
                if len(List_contoursX) > 0 and len(List_contoursY) > 0 and dict_input[
                    'Lab_NumcState'] == "钢坯跟踪" and self.Start_Cut_state == False:
                    # print('setcutlimt',setcutlimt)
                    # print('stats.mode',stats.mode(dict_input['List_contoursX'])[0][0])
                    if stats.mode(List_contoursX)[0][0] <= int(setcutlimt):
                        if self.Start_Cut_state == False:
                            self.Start_Cut_state = True
                            print("启动切割信号")
                            dict_return['Lab_NumcState'] = "钢坯切割"
                elif self.Start_Cut_state == True and stats.mode(List_contoursX)[0][0] > int(setcutlimt):
                    self.Start_Cut_state = False

                dict_return = {'Num_image': steelMasterFlow, 'Lab_NumcState': "钢坯跟踪"}
                return dict_return

            # 如果这个图形为空，则没有适合图形
            elif steelMasterFlow is None or len(List_contoursX) == 0 or len(
                    List_contoursY) == 0:
                # print("没有符合面积的图形")
                dict_return = {'Num_image': steelMasterFlow, 'List_contoursX': List_contoursX,
                               'List_contoursY': List_contoursY, 'Lab_NumcState': "等待钢坯"}
        return dict_return

        '''
        dict_return:
        Num_image: 第几个图像符合要求
        List_contoursX:X轴的数组
        List_contoursY:Y轴的数组
        Lab_NumcState:显示信息状态
        
        '''

    def frame_target_Line(self, frame_cut, dict_input, temp_Lne_Frame_cut_Y1, temp_Lne_Frame_cut_Y0, frame_cut_angle):
        if len(dict_input['List_contoursX']) > 0 and len(dict_input['List_contoursY']) > 0 and dict_input[
            'Lab_NumcState'] == "钢坯跟踪" and self.Start_Cut_state == False:
            # print("List_contoursX X轴数值", dict_input['List_contoursX'])
            # print("List_contoursY Y轴数值", dict_input['List_contoursY'])
            # print("最小值", min(dict_input['List_contoursX']))
            # print("X众数值", stats.mode(dict_input['List_contoursX'])[0][0])  # X众数值
            # print("Y众数值", stats.mode(dict_input['List_contoursY'])[0][0])  # Y众数值

            # 钢坯头部位置提示线
            ptStart_angle_X = int(
                int(temp_Lne_Frame_cut_Y1) - int(temp_Lne_Frame_cut_Y0)) * float(
                math.tan(math.radians(float(frame_cut_angle))))
            ptStart_angle_Y = int(
                int(temp_Lne_Frame_cut_Y1) - int(temp_Lne_Frame_cut_Y0)) * float(
                math.tan(math.radians(float(frame_cut_angle))))

            Line_Start_f4 = (
                min(dict_input['List_contoursX']) + int(ptStart_angle_X), temp_Lne_Frame_cut_Y0)  # 画线直线起点
            Line_End_f4 = (
                min(dict_input['List_contoursX']) - int(ptStart_angle_X), temp_Lne_Frame_cut_Y1)  # 画线直线终点
            # int((int(temp_Lne_Frame_cut_Y0) + int(temp_Lne_Frame_cut_Y1)) / 2) #中间值
            # 跟踪钢坯头部线
            cv2.line(frame_cut, Line_Start_f4, Line_End_f4, (255, 255, 0), self.thickness, self.lineType)




                    # # 增加4流计数量
                    # config_ini.writeValue('init', 'Lab_4cCount',
                    #                       str(int(config_ini.readvalue('init', 'Lab_4cCount')) + 1))
                    # self.Lab_4cCount.setText(str(config_ini.readvalue('init', 'Lab_4cCount')))  # 4流记数
                    #
                    # config_ini.writeValue('init', 'Lab_talRoot',
                    #                       str(int(config_ini.readvalue('init', 'Lab_talRoot')) + 1))
                    # self.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数

    #                 self.slot_CutToSQL(
    #                     FurNum=str((config_fur.readvalue('FurListData1', 'lne_setfurno'))),
    #                     FlowNum="4",  # 流号
    #                     FixLength=str(self.Lab_4cSetLength.text()),  # 定尺长度
    #                     Team=str(self.Btn_Class.text()),  # 班组
    #                     SteelType=str(self.Lab_4cSteels.text()),  # 钢种
    #                     RealWeight=str(self.Lab_4cWeight.text()),  # 真实重量
    #                     Weighing="否",  # 是否称重
    #                     SetWeight=str(self.Btn_1aSetWeight.text()),  # 设定重量
    #                     IDtime=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),  # 时间
    #                     adjustment=str(self.Lab_4cCompensate.text()),  # 补偿值
    #                     density="7.8",  # 密度
    #                     theoryWeight=str(self.Lab_4bWeight.text())  # 理论重量
    #                 )
    #                 # 传给PLC  给M区变量1个值来判断切割
