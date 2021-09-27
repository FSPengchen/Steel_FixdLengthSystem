import cv2
import matplotlib as plt
import numpy as np

frame = cv2.imread("pictrue\\FT-G2F202-Snapshot-20210915103306-27222617882.BMP")

# print(GrayImage)
#
# ret, thresh1 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_BINARY)
#
# ret, thresh2 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_BINARY_INV)
#
# ret, thresh3 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_TRUNC)
#
# ret, thresh4 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_TOZERO)
#
# ret, thresh5 = cv2.threshold(GrayImage, 10, 255, cv2.THRESH_TOZERO_INV)
#
# cv2.imshow('thresh1', thresh1)
#
# input()





gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)  #二值阀图像，更好的边缘检测
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#binary  二值的结果图像
#img = binary
#contours   轮廓信息
# hierarchy 保存结果的层级

print(np.array(contours))    #轮廓的信息

#采用轮廓信息，进行绘制轮廓图像
draw_img = frame.copy() # 注意需要copy,要不原图会变

img = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)#-1 全部轮廓画出来
# 传入绘制图像，轮廓，轮廓索引，颜色模式，线条厚度



cv2.imshow("thresh image",thresh)
cv2.imshow("image",frame)
#cv2.imshow(new_frame)
#cv2.imshow("aa",res)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()





# titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
#
# images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5] 
#
# for i in xrange(6):
#
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#
#     plt.title(titles[i])
#
#     plt.xticks([]),plt.yticks([])
#
# plt.show()
