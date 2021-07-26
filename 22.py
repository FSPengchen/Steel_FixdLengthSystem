import numpy as np
import matplotlib.pylab as mp

mp.figure(facecolor="lightgray")  # 创建窗口

# 存储定位器名称
locators=[
    'mp.NullLocator()',
    'mp.MaxNLocator(nbins=5, steps=[1,3,5,7,9])',
    'mp.FixedLocator(locs=[0, 2.5, 5, 7.5, 10])',
    'mp.AutoLocator()',
    'mp.IndexLocator(offset=0.5, base=1.5)',
    'mp.MultipleLocator()',
    'mp.LinearLocator(numticks=21)',
    'mp.LogLocator(base=2, subs=[1.0])',
]

n_locators = len(locators)  # 获取定位器长度

# 遍历每一个定位器来创建子图
for i, locator in enumerate(locators):
    mp.subplot(n_locators, 1, i+1)  # 创建行数为定位器长度，列数为1，图号为i+1的子图
    mp.xlim(0, 10)  # 水平方向是从0到10
    mp.ylim(-1, 1)  # 垂直方向是-1到1
    mp.yticks(())  # 隐藏y坐标轴
    ax = mp.gca()  # 获取坐标轴
    ax.spines['left'].set_color("none")  # 将左坐标轴透明
    ax.spines['top'].set_color("none")  # 将上坐标轴透明
    ax.spines['right'].set_color("none")  # 将右坐标轴透明
    ax.spines['bottom'].set_position(('data', 0))  # 将底坐标轴设置数据坐标为0的位置

    # 设置主刻度
    ax.xaxis.set_major_locator(eval(locator))  # 以遍历到的定位器为朱刻度
    # 设置次刻度
    ax.xaxis.set_minor_locator(mp.MultipleLocator(0.1))  # 以0.1为最小间隔距离
    print(ax)

    # 随便画个图
    mp.plot(np.arange(11), np.zeros(11), c='none')  # 0到10位横坐标，10个0位纵坐标，颜色为空

    # 用文字标识一下定位器
    mp.text(5, 0.3, locator[3:], ha='center', size=12)

mp.tight_layout()  # 紧凑显示
mp.show()  # 显示图表