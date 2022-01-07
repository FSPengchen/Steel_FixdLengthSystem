import cv2
import numpy as np
import math

# 一流底端线的端点
# x1 = int(input('x1'))
# y1 = int(input('y1'))
# x2 = int(input('x2'))
# y2 = int(input('y2'))

x1 = 0
y1 = 300
x2 = 900
y2 = 200
n = 60

# 写入的标定点  如13米点
x_13 = 100  # 402
x_11 = 400  # 408
x_9 = 750  # 416


def scale_line(x1, y1, x2, y2, n):
    # 展示直线
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2, 8)
    k1 = float((y2 - y1)) / float((x2 - x1))
    B = float(((x2 - x1) * y1 - (y2 - y1) * x1)) / float(x2 - x1)
    # print('k1:', k1)
    # print('B:', B)
    cv2.line(img, (x1, y1 - n), (x2, y2 - n), (255, 255, 0), 2, 8)

    y_13 = k1 * x_13 + B
    print('y_13', y_13)
    y_11 = k1 * x_11 + B
    print('y_11', y_11)
    y_9 = k1 * x_9 + B
    print('y_9', y_9)

    cv2.circle(img, (int(x_13), int(y_13)), 2, (0, 0, 255), 2)
    cv2.circle(img, (int(x_11), int(y_11)), 2, (0, 0, 255), 2)
    cv2.circle(img, (int(x_9), int(y_9)), 2, (0, 0, 255), 2)

    # 2000  为2米   5毫米为一个刻度
    # X`刻度坐标(实际5MM为1刻度)
    pianyiliang_11_9 = (x_9 - x_11) / 2000 * 5
    xinx_11_9 = x_11 + pianyiliang_11_9 * 10
    xiny_11_9 = k1 * xinx_11_9 + B

    pianyiliang_11_13 = (x_9 - x_13) / 2000 * 108
    xinx_11_13 = x_11 + pianyiliang_11_13 * 10
    xiny_11_13 = k1 * xinx_11_13 + B

    cv2.circle(img, (int(xinx_11_9), int(xiny_11_9)), 1, (0, 255, 255), 2)
    cv2.circle(img, (int(xinx_11_13), int(xiny_11_13)), 1, (0, 255, 255), 2)

    distance_11_9 = math.sqrt((x_9 - x_11)*(x_9 - x_11) + (y_9 - y_11)*(y_9 - y_11))
    print('11到9之间的距离',distance_11_9)
    num = 50

    # # 刻度线上的点
    # distance_x_11_9_1 = x_11 + ((x_9-x_11)/num)
    # distance_y_11_9_1 = k1 * distance_x_11_9_1 + B
    # print('1',distance_x_11_9_1,distance_y_11_9_1)
    #
    # distance_x_11_9_2 = x_11 + (2*(x_9-x_11) / num)
    # distance_y_11_9_2 = k1 * distance_x_11_9_2 + B
    # print('2', distance_x_11_9_2, distance_y_11_9_2)
    #
    # distance_x_11_9_3 = x_11 + (3*(x_9-x_11) / num)
    # distance_y_11_9_3 = k1 * distance_x_11_9_3 + B
    # print('3', distance_x_11_9_3, distance_y_11_9_3)

    # cv2.circle(img, (int(distance_x_11_9_1), int(distance_y_11_9_1)), 4, (125, 0, 255), 4)
    # cv2.circle(img, (int(distance_x_11_9_2), int(distance_y_11_9_2)), 4, (125, 0, 255), 4)
    # cv2.circle(img, (int(distance_x_11_9_3), int(distance_y_11_9_3)), 4, (125, 0, 255), 4)

    for i in range(num):
        distance_x_11_9 = x_11 + (i * (x_9 - x_11) / num)
        distance_y_11_9 = k1 * distance_x_11_9 + B
        print('3', distance_x_11_9, distance_y_11_9)
        cv2.circle(img, (int(distance_x_11_9), int(distance_y_11_9)), 1, (0, 255, 255), 1)






    D2 = 10
    # 两点间直线长度
    # D2 = (math.sqrt(1 + k1*k1)) * (abs(x1 - x2))
    if y1 != y2:
        cuizhi_k = - 1 / k1
    elif y1 == y2:
        cuizhi_k = 0
    # B1=-K1*X1+Y1
    cuizhi_B = -1 * (cuizhi_k * x_11) + y_11

    keduxian_x11_9_1 = math.sqrt(D2 * D2 / (1 + cuizhi_k * cuizhi_k)) + x_11
    print('x_11', x_11)
    print('y_11', y_11)
    print('keduxian_x11_9_1', keduxian_x11_9_1)

    keduxian_y11_9_1 = cuizhi_k * keduxian_x11_9_1 + cuizhi_B
    print(keduxian_y11_9_1)
    print('keduxian_y11_9_1', keduxian_y11_9_1)
    print('k1:', k1)
    print('cuizhi_k', cuizhi_k)
    print('B', cuizhi_B)

    cv2.line(img, (int(x_11), int(y_11)), (int(keduxian_x11_9_1), int(keduxian_y11_9_1)), (255, 255, 0), 1, 1)

    cuizhi_B = -1 * (cuizhi_k * xinx_11_13) + xiny_11_13
    keduxian_x11_13_1 = math.sqrt(D2 * D2 / (1 + cuizhi_k * cuizhi_k)) + xinx_11_13
    keduxian_y11_13_1 = cuizhi_k * keduxian_x11_13_1 + cuizhi_B
    cv2.line(img, (int(xinx_11_13), int(xiny_11_13)), (int(keduxian_x11_13_1), int(keduxian_y11_13_1)), (255, 255, 0), 1, 1)



img = np.zeros((480, 900, 3), np.uint8)

scale_line(x1, y1, x2, y2, n)

cv2.imshow('a', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
