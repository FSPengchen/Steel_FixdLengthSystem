

# -*- coding: UTF-8 -*-
import cv2
import numpy as np


def get_image(path):
    # 获取图片
    img = cv2.imread(r"D:\Picture\IMG_20210410_162657cut.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img, gray


def Gaussian_Blur(gray):
    # 高斯去噪
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    return blurred


def Sobel_gradient(blurred):
    # 索比尔算子来计算x、y方向梯度
    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    return gradX, gradY, gradient


def Thresh_and_blur(gradient):
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)

    return thresh


def image_morphology(thresh):
    # 建立一个椭圆核函数
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    # 执行图像形态学, 细节直接查文档，很简单
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    return closed


def findcnts_and_box_point(closed):
    # 这里opencv3返回的是三个参数
    (_, cnts, _) = cv2.findContours(closed.copy(),
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    return box


def drawcnts_and_cut(original_img, box):
    # 因为这个函数有极强的破坏性，所有需要在img.copy()上画
    # draw a bounding box arounded the detected barcode and display the image
    draw_img = cv2.drawContours(original_img.copy(), [box], -1, (0, 0, 255), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    crop_img = original_img[y1:y1 + hight, x1:x1 + width]

    return draw_img, crop_img


def walk():
    img_path = r'worm.png'
    save_path = r'worm_save.png'
    original_img, gray = get_image(img_path)
    blurred = Gaussian_Blur(gray)
    gradX, gradY, gradient = Sobel_gradient(blurred)
    thresh = Thresh_and_blur(gradient)
    closed = image_morphology(thresh)
    box = findcnts_and_box_point(closed)
    draw_img, crop_img = drawcnts_and_cut(original_img, box)

    # 暴力一点，把它们都显示出来看看

    cv2.imshow('original_img', original_img)
    cv2.imshow('blurred', blurred)
    cv2.imshow('gradX', gradX)
    cv2.imshow('gradY', gradY)
    cv2.imshow('final', gradient)
    cv2.imshow('thresh', thresh)
    cv2.imshow('closed', closed)
    cv2.imshow('draw_img', draw_img)
    cv2.imshow('crop_img', crop_img)
    cv2.waitKey(20171219)
    cv2.imwrite(save_path, crop_img)


walk()
#
# 附录代码：
#
# # 用来转化图像格式的
# img = cv2.cvtColor(src,
#                    COLOR_BGR2HSV  # BGR---->HSV
# COLOR_HSV2BGR  # HSV---->BGR
#     ...)
# # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
#
#
# # 返回一个阈值，和二值化图像，第一个阈值是用来otsu方法时候用的
# # 不过现在不用了，因为可以通过mahotas直接实现
# T = ret = mahotas.threshold(blurred)
# ret, thresh_img = cv2.threshold(src,  # 一般是灰度图像
#                                 num1,  # 图像阈值
#                                 num2,  # 如果大于或者num1, 像素值将会变成 num2
#                                 # 最后一个二值化参数
#                                 cv2.THRESH_BINARY  # 将大于阈值的灰度值设为最大灰度值，小于阈值的值设为0
# cv2.THRESH_BINARY_INV  # 将大于阈值的灰度值设为0，大于阈值的值设为最大灰度值
# cv2.THRESH_TRUNC  # 将大于阈值的灰度值设为阈值，小于阈值的值保持不变
# cv2.THRESH_TOZERO  # 将小于阈值的灰度值设为0，大于阈值的值保持不变
# cv2.THRESH_TOZERO_INV  # 将大于阈值的灰度值设为0，小于阈值的值保持不变
# )
# thresh = cv2.AdaptiveThreshold(src,
#                                dst,
#                                maxValue,
#                                # adaptive_method
#                                ADAPTIVE_THRESH_MEAN_C,
#                                ADAPTIVE_THRESH_GAUSSIAN_C,
#                                # thresholdType
#                                THRESH_BINARY,
#                                THRESH_BINARY_INV,
#                                blockSize=3,
#                                param1=5
#                                )
#
# # 一般是在黑色背景中找白色物体，所以原始图像背景最好是黑色
# # 在执行找边缘的时候，一般是threshold 或者是canny 边缘检测后进行的。
# # warning:此函数会修改原始图像、
# # 返回：坐标位置（x,y）,
# (_, cnts, _) = cv2.findContours(mask.copy(),
#                                 # cv2.RETR_EXTERNAL,             #表示只检测外轮廓
#                                 # cv2.RETR_CCOMP,                #建立两个等级的轮廓,上一层是边界
#                                 cv2.RETR_LIST,  # 检测的轮廓不建立等级关系
#                                 # cv2.RETR_TREE,                   #建立一个等级树结构的轮廓
#                                 # cv2.CHAIN_APPROX_NONE,           #存储所有的轮廓点，相邻的两个点的像素位置差不超过1
#                                 cv2.CHAIN_APPROX_SIMPLE,  # 例如一个矩形轮廓只需4个点来保存轮廓信息
#                                 # cv2.CHAIN_APPROX_TC89_L1,
#                                 # cv2.CHAIN_APPROX_TC89_KCOS
#                                 )
# img = cv2.drawContours(src, cnts, whichToDraw(-1), color, line)
#
# img = cv2.imwrite(filename, dst,  # 文件路径，和目标图像文件矩阵
#
#                   # 对于JPEG，其表示的是图像的质量，用0-100的整数表示，默认为95
#                   # 注意，cv2.IMWRITE_JPEG_QUALITY类型为Long，必须转换成int
#                   [int(cv2.IMWRITE_JPEG_QUALITY), 5]
#                   [int(cv2.IMWRITE_JPEG_QUALITY), 95]
#                       # 从0到9,压缩级别越高，图像尺寸越小。默认级别为3
#                   [int(cv2.IMWRITE_PNG_COMPRESSION), 5])
# [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
#
# # 如果你不知道用哪个flags，毕竟太多了哪能全记住，直接找找。
# 寻找某个函数或者变量
# events = [i for i in dir(cv2) if 'PNG' in i]
# print(events)
#
# 寻找某个变量开头的flags
# flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
# print
# flags
#
# 批量读取文件名字
# import os
#
# filename_rgb = r'C:\Users\aixin\Desktop\all_my_learning\colony\20170629'
# for filename in os.listdir(filename_rgb):  # listdir的参数是文件夹的路径
#     print(filename)