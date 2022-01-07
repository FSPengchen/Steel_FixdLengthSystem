import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from pandas.plotting import scatter_matrix
from sqlalchemy import create_engine
import os, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    print('读取数据')
    df = pd.read_excel(r'E:\PycharmProjects\FixedLengthSystem\数据0927-1015.xlsx')

    x = df[['定尺', '微调值', '设定重量']]
    x = np.array(x)
    y = df.实际重量
    y = np.array(y)
    print(y, type(y))

    # 2 分割训练数据和测试数据
    # 随机采样25%作为测试 75%作为训练

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    # 3 训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    print('变化前', x_train)
    x_train = ss_x.fit_transform(np.array(x_train))
    # x_train = ss_x.fit_transform(x_train.reshape(-1,1))
    print('变化后', x_train)
    print('x_test:', x_test)
    x_test = ss_x.transform(x_test)

    # ss_y = StandardScaler()
    # y_train = ss_y.fit_transform(y_train.reshape(-1,1))
    # y_test = ss_y.transform(y_test.reshape(-1, 1))

    from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor

    # 极端随机森林回归
    etr = ExtraTreesRegressor()
    # 训练
    etr.fit(x_train, y_train)
    # 预测 保存预测结果
    print('x_test:', x_test)
    etr_y_predict = etr.predict(x_test)
    print('预测值', etr_y_predict)

    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    # 极端随机森林回归模型评估
    # print("极端随机森林回归的默认评估值为：", etr.score(x_test, y_test))
    # print("极端随机森林回归的R_squared值为：", r2_score(y_test, etr_y_predict))
    # print("极端随机森林回归的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),
    #                                             ss_y.inverse_transform(etr_y_predict)))
    # print("极端随机森林回归的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),
    #                                                ss_y.inverse_transform(etr_y_predict)))

    # 极端随机森林回归模型评估(y值未归一化)
    print("极端随机森林回归的默认评估值为：", etr.score(x_test, y_test))
    print("极端随机森林回归的R_squared值为：", r2_score(y_test, etr_y_predict))
    print("极端随机森林回归的均方误差为:", mean_squared_error(y_test,
                                                etr_y_predict))
    print("极端随机森林回归的平均绝对误差为:", mean_absolute_error(y_test,
                                                   etr_y_predict))

    # import pickle  # 保存模型 pickle模块
    #
    # # 保存Model(注:save文件夹要预先建立，否则会报错)
    # with open('motel/etr.pickle', 'wb') as f:
    #     pickle.dump(etr, f)
    #
    # # 读取Model
    # with open('motel/etr.pickle', 'rb') as f:
    #     etr2 = pickle.load(f)

    etr2_y_predict = etr.predict(x_test)
    print('预测值', etr2_y_predict)
