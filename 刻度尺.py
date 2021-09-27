import cv2
import numpy as np
import math


def scale_line(img, pt1, pt2, before, after, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_8,scale_h=3):
    # 展示直线
    cv2.line(img=img, pt1=pt1, pt2=pt2, color=color, thickness=thickness, lineType=lineType)
    if pt1[0] < pt2[0] and pt1[1] < pt2[1]:
        # 计算绝对值距离,即直角三角形的两个非直角边的边长
        a = abs(pt2[0] - pt1[0])
        b = abs(pt2[1] - pt1[1])

        print('底边长度a:', a, '底边长度b:', b)
        # 获取底边对应的角度
        tana = a / b
        print('底边a对应的tan角度', tana)
        jiao_tan = math.atan(tana)
        print('底边a对应的角度', jiao_tan)
        c = a / math.sin(jiao_tan)
        print('直角三角形斜边长', c)

        # 前段开始距离点
        y_b1 = before * math.cos(jiao_tan)
        x_a1 = before * math.sin(jiao_tan)
        print(x_a1 + pt1[0], y_b1 + pt1[1])
        cv2.circle(img, (int(x_a1 + pt1[0]), int(y_b1 + pt1[1])), 1, (0, 0, 255), 1)

        # 后段开始距离点
        c2 = c - after
        y_b2 = c2 * math.cos(jiao_tan)
        x_a2 = c2 * math.sin(jiao_tan)
        print(x_a2 + pt1[0], y_b2 + pt1[1])
        cv2.circle(img, (int(x_a2 + pt1[0]), int(y_b2 + pt1[1])), 1, (0, 0, 255), 1)

        # 去除前后段线缆的中心点坐标
        x_center = (((c - float(after) - float(before)) / 2) + float(before)) * math.sin(jiao_tan)
        y_center = (((c - float(after) - float(before)) / 2) + float(before)) * math.cos(jiao_tan)
        print(x_center, y_center)
        cv2.circle(img, (int(x_center + pt1[0]), int(y_center + pt1[1])), 1, (0, 0, 255), 1)

        # jiao_scale_h = math.asin(scale_h / ((c - float(after) - float(before)) / 2) + float(before))

    else:
        print('未编写')


img = np.zeros((600, 900, 3), np.uint8)

scale_line(img, pt1=(40, 50), pt2=(500, 100), before=20, after=10)

cv2.imshow('a', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
