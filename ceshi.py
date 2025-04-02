# import numpy as np
# # 生成误差数据
# # 原始数据
# original_data = np.array([
#     0, 10.50555, 17.6456, 33.51883, 334.77315, 606.60097, 777.32802,
#     1003.30892, 1040.68247, 1036.41581, 1037.77646, 1038.83293, 1038.67269,
#     1038.05617, 1045.19622, 1088.929, 1094.15272, 1093.68829, 1097.93864,
#     1095.49706, 1098.07442, 1097.71822, 1096.8414, 1098.9625, 1099.61546,
#     1097.72947, 1098.02549, 1100.28084, 1101.35515, 1100.0891, 1098.75332,
#     1104.39341, 1106.64566, 1105.69312, 1100.39369, 1101.60225, 1103.6369,
#     1103.909, 1102.03405, 1100.04873, 1102.6261, 1109.76615, 1151.9248,
#     1160.54772, 1214.27101, 1324.75798, 1447.13404, 1471.91357, 1456.40984,
#     1392.92141, 1283.28583, 1157.77822, 993.75822, 813.35343, 670.32686,
#     523.53586, 380.25834, 240.20632, 139.34326, 70, 0
# ])
#
# # 生成误差范围内的新数据点
# noise_factor = 0.03  # 误差范围 ±5%
# new_data = original_data * (1 + np.random.uniform(-noise_factor, noise_factor, original_data.shape))
#
# new_data
#
# print(new_data)



# 画轴心图
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('D:/a_study/exe/fengqing_exe/轴心图数据.csv', header=None)  # 假设没有列名，修改文件路径

# 获取第一列和第二列作为增量数据
delta_x = data[0].tolist()  # 第一列作为x坐标增量
delta_y = data[1].tolist()  # 第二列作为y坐标增量

# 初始化起点
x = [0]  # 起始位置x
y = [0]  # 起始位置y

# 计算每个点的坐标
for i in range(len(delta_x)):
    x.append(x[-1] + delta_x[i])
    y.append(y[-1] + delta_y[i])

# 设置全局字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 适用于 Windows
matplotlib.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题
# 绘制轨迹
plt.plot(x, y, marker='o')

# 设置标题和坐标轴标签
plt.title("轴心轨迹图")  # 图名
plt.xlabel("X 位移 (μm)")  # X轴名称
plt.ylabel("Y 位移 (μm)")  # Y轴名称

# 显示图例
plt.legend()

# 显示图形
plt.show()


# import pandas as pd
# import matplotlib.pyplot as plt
#
# # 读取 CSV 文件
# df = pd.read_csv("D:/a_study\exe/fengqing_exe/轴心数据1.csv")
#
# # 假设 CSV 文件的第一列是 x，第二列是 y
# x = df.iloc[:, 0]
# y = df.iloc[:, 1]
#
# # 画点图（散点图）
# plt.scatter(x, y, marker='o', color='b', alpha=0.7)
# plt.xlabel("X轴")
# plt.ylabel("Y轴")
# plt.title("散点图")
# plt.grid(True)
#
# # 显示图像
# plt.show()

