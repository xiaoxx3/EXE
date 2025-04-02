# 风氢规划综合管理平台
# 包括登陆界面
from LoginUi import *
from zhuce import *
from InterfaceUI import *
from fengji import *
from zhiqing import *
from rengongtiaojie import *

from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout, QWidget
from PyQt5.QtGui import QPen, QFont
import pyqtgraph as pg
import sys
import pandas as pd

from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 登录页面,done
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_denglu()
        self.ui.setupUi(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框，后面再把他取消掉
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_denglu.clicked.connect(self.go_to_inter)    # 登录
        self.ui.pushButton_chuce.clicked.connect(self.go_to_inter_zhuce)    # 注册
        self.show()

    # 跳转主页面
    def go_to_inter(self):
        account = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if account == "123456" and password == "123456":
            self.win = InterfaceWindow()
            self.close()
        else:
            pass
    # 跳转注册页面
    def go_to_inter_zhuce(self):
        self.win = zhuce()
        self.close()

    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

# 注册页面,done
class zhuce(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_zhuce()
        self.ui.setupUi(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框，后面再把他取消掉
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_fanhui.clicked.connect(self.go_to_inter_denglu)
        self.show()

    def go_to_inter_denglu(self):
        self.win = LoginWindow()
        self.close()

    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

# 首页页面，让侠影画一个饼图
class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_inter()  # 绑定 UI,不同的UI就靠这个改
        self.ui.setupUi(self)  # 设置 UI 到当前窗口
        self.adjustSize()  # 让窗口自动调整到适合的大小

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明

        # 将ui中的widge换成xy图
        # 实时风速，每行都改
        self.shishifengsu = pg.PlotWidget()
        parent_layout = self.ui.shishifengsu.parentWidget().layout()
        parent_layout.removeWidget(self.ui.shishifengsu)
        self.ui.shishifengsu.deleteLater()
        parent_layout.addWidget(self.shishifengsu)
        self.shishifengsu.setBackground(None)    # 透明色背景色透明
        self.shishifengsu.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.shishifengsu.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.shishifengsu.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.shishifengsu.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        self.shishifengsu.setXRange(0, 24)  # X 轴范围
        self.shishifengsu.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.shishifengsu.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.shishifengsu.setYRange(0, 8)  # Y 轴范围
        self.shishifengsu.setLabel('left', '风速 (m/s)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\interface\风速.csv", self.shishifengsu)  # 跟着一起改

        # 风机发电量
        self.fengjifadian = pg.PlotWidget()
        parent_layout = self.ui.fengjifadian.parentWidget().layout()
        parent_layout.removeWidget(self.ui.fengjifadian)
        self.ui.fengjifadian.deleteLater()
        parent_layout.addWidget(self.fengjifadian)
        self.fengjifadian.setBackground(None)  # 透明色背景色透明
        self.fengjifadian.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.fengjifadian.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.fengjifadian.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.fengjifadian.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.fengjifadian.addLine(y=1, pen=pg.mkPen('black'))
        # self.fengjifadian.addLine(x=1, pen=pg.mkPen('black'))
        self.fengjifadian.setXRange(0, 24)  # X 轴范围
        self.fengjifadian.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.fengjifadian.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.fengjifadian.setYRange(0, 1)  # Y 轴范围
        self.fengjifadian.setLabel('left', '发电量 (kW)', **{'color': 'black', 'font-size': '10pt'})   # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\interface\风机发电量.csv", self.fengjifadian)  # 跟着一起改

        # 预计收益
        self.yujishouyi = pg.PlotWidget()
        parent_layout = self.ui.yujishouyi.parentWidget().layout()
        parent_layout.removeWidget(self.ui.yujishouyi)
        self.ui.yujishouyi.deleteLater()
        parent_layout.addWidget(self.yujishouyi)
        self.yujishouyi.setBackground(None)  # 透明色背景色透明
        self.yujishouyi.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.yujishouyi.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.yujishouyi.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.yujishouyi.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.yujishouyi.addLine(y=1, pen=pg.mkPen('black'))
        # self.yujishouyi.addLine(x=1, pen=pg.mkPen('black'))
        self.yujishouyi.setXRange(0, 24)  # X 轴范围
        self.yujishouyi.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.yujishouyi.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.yujishouyi.setYRange(0, 9000)  # Y 轴范围
        self.yujishouyi.setLabel('left', '收益 (元)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\interface\制氢预计收益.csv", self.yujishouyi)  # 跟着一起改

        # 实时电价
        self.shishidianjia = pg.PlotWidget()
        parent_layout = self.ui.shishidianjia.parentWidget().layout()
        parent_layout.removeWidget(self.ui.shishidianjia)
        self.ui.shishidianjia.deleteLater()
        parent_layout.addWidget(self.shishidianjia)
        self.shishidianjia.setBackground(None)  # 透明色背景色透明
        self.shishidianjia.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.shishidianjia.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.shishidianjia.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.shishidianjia.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.shishidianjia.addLine(y=1, pen=pg.mkPen('black'))
        # self.shishidianjia.addLine(x=1, pen=pg.mkPen('black'))
        self.shishidianjia.setXRange(0, 24)  # X 轴范围
        self.shishidianjia.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.shishidianjia.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.shishidianjia.setYRange(50, 160)  # Y 轴范围
        self.shishidianjia.setLabel('left', '电价', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\interface\实时电价.csv", self.shishidianjia)  # 跟着一起改

        self.show()

        self.ui.pushButton_main.clicked.connect(self.go_to_inter_main)
        self.ui.pushButton_fengji.clicked.connect(self.go_to_inter_fengji)
        self.ui.pushButton_zhiqing.clicked.connect(self.go_to_inter_zhiqing)
        self.ui.pushButton_rengong.clicked.connect(self.go_to_inter_rengong)

    def go_to_inter_main(self):
        self.win = InterfaceWindow()
        self.close()
    def go_to_inter_fengji(self):
        self.win = fengji()
        self.close()

    def go_to_inter_zhiqing(self):
        self.win = zhiqing()
        self.close()

    def go_to_inter_rengong(self):
        self.win = rengong()
        self.close()

    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # 读取数据画图
    def load_csv_and_plot(self, file_path, target_plot):
        try:
            # 读取 CSV 数据
            data = pd.read_csv(file_path)

            # 确保 CSV 里至少有两列
            if len(data.columns) < 2:
                print("CSV 数据格式错误，至少需要两列")
                return

            x = data.iloc[:, 0]  # 第一列作为 X 轴
            y = data.iloc[:, 1]  # 第二列作为 Y 轴

            # 清除旧图
            target_plot.clear()

            # 画新图
            target_plot.plot(x, y, pen=pg.mkPen('b', width=2))

        except Exception as e:
            print(f"读取 CSV 失败: {e}")

# 风机页面，加风速概率分布柱状图
class fengji(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_fengji()  # 绑定 UI,不同的UI就靠这个改
        self.ui.setupUi(self)  # 设置 UI 到当前窗口
        self.adjustSize()  # 让窗口自动调整到适合的大小

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明

        # 将ui中的widge换成xy图
        # 实时风速，每行都改
        self.shishifengsu = pg.PlotWidget()
        parent_layout = self.ui.shishifengsu.parentWidget().layout()
        parent_layout.removeWidget(self.ui.shishifengsu)
        self.ui.shishifengsu.deleteLater()
        parent_layout.addWidget(self.shishifengsu)
        self.shishifengsu.setBackground(None)    # 透明色背景色透明
        self.shishifengsu.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.shishifengsu.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.shishifengsu.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.shishifengsu.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.shishifengsu.addLine(y=1, pen=pg.mkPen('black'))
        # self.shishifengsu.addLine(x=1, pen=pg.mkPen('black'))
        self.shishifengsu.setXRange(0, 24)  # X 轴范围
        self.shishifengsu.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.shishifengsu.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.shishifengsu.setYRange(0, 8)  # Y 轴范围
        self.shishifengsu.setLabel('left', '风速 (m/s)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\fengji\风速.csv", self.shishifengsu)  # 跟着一起改

        # 风速概率
        # self.fengsugailv = pg.PlotWidget()
        # parent_layout = self.ui.fengsugailv.parentWidget().layout()
        # parent_layout.removeWidget(self.ui.fengsugailv)
        # self.ui.fengsugailv.deleteLater()
        # parent_layout.addWidget(self.fengsugailv)
        # self.fengsugailv.setBackground(None)  # 透明色背景色透明
        # self.fengsugailv.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        # self.fengsugailv.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        # self.fengsugailv.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        # self.fengsugailv.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.fengsugailv.setXRange(0, 24)  # X 轴范围
        # self.fengsugailv.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 25, 4)]])  # X 轴刻度间隔 4
        # self.fengsugailv.setLabel('bottom', '时间 (小时)', **{'color': 'black', 'font-size': '10pt'})
        # self.fengsugailv.setYRange(0, 10)  # Y 轴从 0 开始，最大值后续根据需要调整
        # # self.fengsugailv.addLine(y=1, pen=pg.mkPen('black'))
        # # self.fengsugailv.addLine(x=1, pen=pg.mkPen('black'))

        # 替换 UI 中的 fengsugailv 组件
        self.fengsugailv = pg.PlotWidget()
        parent_layout = self.ui.fengsugailv.parentWidget().layout()
        parent_layout.removeWidget(self.ui.fengsugailv)
        self.ui.fengsugailv.deleteLater()
        parent_layout.addWidget(self.fengsugailv)
        # 配置绘图组件
        self.setup_plot_widget(self.fengsugailv)
        # 加载 CSV 数据并绘制柱状图
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\fengji\风速概率.csv", self.fengsugailv)




        # 预发电量
        self.yufadianliang = pg.PlotWidget()
        parent_layout = self.ui.yufadianliang.parentWidget().layout()
        parent_layout.removeWidget(self.ui.yufadianliang)
        self.ui.yufadianliang.deleteLater()
        parent_layout.addWidget(self.yufadianliang)
        self.yufadianliang.setBackground(None)  # 透明色背景色透明
        self.yufadianliang.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.yufadianliang.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.yufadianliang.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.yufadianliang.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.yufadianliang.addLine(y=1, pen=pg.mkPen('black'))
        # self.yufadianliang.addLine(x=1, pen=pg.mkPen('black'))
        self.yufadianliang.setXRange(0, 24)  # X 轴范围
        self.yufadianliang.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.yufadianliang.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.yufadianliang.setYRange(0, 1)  # Y 轴范围
        self.yufadianliang.setLabel('left', '发电量 (kW)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\fengji\风机发电量.csv", self.yufadianliang)  # 跟着一起改

        self.show()

        self.ui.pushButton_main.clicked.connect(self.go_to_inter_main)
        self.ui.pushButton_fengji.clicked.connect(self.go_to_inter_fengji)
        self.ui.pushButton_zhiqing.clicked.connect(self.go_to_inter_zhiqing)
        self.ui.pushButton_rengong.clicked.connect(self.go_to_inter_rengong)


# 上面的
    def setup_plot_widget(self, plot_widget):
        """ 配置风速概率分布图的样式 """
        plot_widget.setBackground(None)  # 透明背景
        plot_widget.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        plot_widget.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        plot_widget.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        plot_widget.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色

    def load_csv_and_plot(self, file_path, target_plot):
        """ 读取 CSV 并绘制柱状图 """
        try:
            data = pd.read_csv(file_path)

            # 确保 CSV 至少有两列
            if len(data.columns) < 2:
                print("CSV 数据格式错误，至少需要两列")
                return

            x = data.iloc[:, 0].tolist()  # 第一列作为 X 轴
            y = data.iloc[:, 1].tolist()  # 第二列作为 Y 轴

            # 清除旧图
            target_plot.clear()

            # 设置 X 轴范围
            target_plot.setXRange(min(x), max(x))
            target_plot.setYRange(0, max(y) * 1.2)

            # 画柱状图
            bar_item = pg.BarGraphItem(x=x, height=y, width=0.5, brush='skyblue')
            target_plot.addItem(bar_item)

        except Exception as e:
            print(f"加载 CSV 失败: {e}")

    def go_to_inter_main(self):
        self.win = InterfaceWindow()
        self.close()

    def go_to_inter_fengji(self):
        self.win = fengji()
        self.close()

    def go_to_inter_zhiqing(self):
        self.win = zhiqing()
        self.close()

    def go_to_inter_rengong(self):
        self.win = rengong()
        self.close()
# 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # 读取数据画图
    def load_csv_and_plot(self, file_path, target_plot):
        try:
            # 读取 CSV 数据
            data = pd.read_csv(file_path)

            # 确保 CSV 里至少有两列
            if len(data.columns) < 2:
                print("CSV 数据格式错误，至少需要两列")
                return

            x = data.iloc[:, 0]  # 第一列作为 X 轴
            y = data.iloc[:, 1]  # 第二列作为 Y 轴

            # 清除旧图
            target_plot.clear()

            # 画新图
            target_plot.plot(x, y, pen=pg.mkPen('b', width=2))

        except Exception as e:
            print(f"读取 CSV 失败: {e}")

# 制氢页面，加实时供氢占比饼图
class PieChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = [82, 18]  # 饼图数据
        self.labels = ["风机发电", "电网购电"]  # 添加标签

        self.colors = [QColor(179, 212, 157), QColor(220, 73, 89)]  # 颜色
        self.setMinimumSize(100, 100)  # 设置最小尺寸

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿
        painter.setFont(QFont("Arial", 10))  # 设置字体

        rect = self.rect().adjusted(10, 10, -10, -10)  # 设置绘制区域
        total = sum(self.data)  # 计算总值
        start_angle = 0  # 起始角度

        for i, value in enumerate(self.data):
            span_angle = int(360 * (value / total) * 16)  # PyQt 使用 1/16 度单位
            painter.setBrush(QBrush(self.colors[i % len(self.colors)]))
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle  # 更新起始角度
class zhiqing(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_zhiqing()  # 绑定 UI,不同的UI就靠这个改
        self.ui.setupUi(self)  # 设置 UI 到当前窗口
        self.adjustSize()  # 让窗口自动调整到适合的大小

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明

        # 将ui中的widge换成xy图
        # 实时电价
        self.shishidianjia = pg.PlotWidget()
        parent_layout = self.ui.shishidianjia.parentWidget().layout()
        parent_layout.removeWidget(self.ui.shishidianjia)
        self.ui.shishidianjia.deleteLater()
        parent_layout.addWidget(self.shishidianjia)
        self.shishidianjia.setBackground(None)    # 透明色背景色透明
        self.shishidianjia.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.shishidianjia.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.shishidianjia.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.shishidianjia.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.shishidianjia.addLine(y=1, pen=pg.mkPen('black'))
        # self.shishidianjia.addLine(x=1, pen=pg.mkPen('black'))
        self.shishidianjia.setXRange(0, 24)  # X 轴范围
        self.shishidianjia.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.shishidianjia.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.shishidianjia.setYRange(50, 160)  # Y 轴范围
        self.shishidianjia.setLabel('left', '电价', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\zhiqing\实时电价.csv", self.shishidianjia)  # 跟着一起改

        # 风电利用率
        self.fengdianliyong = pg.PlotWidget()
        parent_layout = self.ui.fengdianliyong.parentWidget().layout()
        parent_layout.removeWidget(self.ui.fengdianliyong)
        self.ui.fengdianliyong.deleteLater()
        parent_layout.addWidget(self.fengdianliyong)
        self.fengdianliyong.setBackground(None)  # 透明色背景色透明
        self.fengdianliyong.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.fengdianliyong.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.fengdianliyong.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.fengdianliyong.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.fengdianliyong.addLine(y=1, pen=pg.mkPen('black'))
        # self.fengdianliyong.addLine(x=1, pen=pg.mkPen('black'))
        self.fengdianliyong.setXRange(0, 24)  # X 轴范围
        self.fengdianliyong.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.fengdianliyong.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.fengdianliyong.setYRange(0.85, 1.05)  # Y 轴范围
        self.fengdianliyong.setLabel('left', '百分比 (%)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\zhiqing\风电利用率.csv", self.fengdianliyong)  # 跟着一起改

        # 供氢占比
        # self.gongqingzhanbi = pg.PlotWidget()
        # parent_layout = self.ui.gongqingzhanbi.parentWidget().layout()
        # parent_layout.removeWidget(self.ui.gongqingzhanbi)
        # self.ui.gongqingzhanbi.deleteLater()
        # parent_layout.addWidget(self.gongqingzhanbi)
        # self.gongqingzhanbi.setBackground(None)  # 透明色背景色透明
        # self.gongqingzhanbi.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        # self.gongqingzhanbi.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        # self.gongqingzhanbi.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        # self.gongqingzhanbi.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.gongqingzhanbi.setXRange(0, 24)  # X 轴范围
        # self.gongqingzhanbi.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 25, 4)]])  # X 轴刻度间隔 4
        # self.gongqingzhanbi.setLabel('bottom', '时间 (小时)', **{'color': 'black', 'font-size': '10pt'})
        # self.gongqingzhanbi.setYRange(0, 10)  # Y 轴从 0 开始，最大值后续根据需要调整
        # # self.gongqingzhanbi.addLine(y=1, pen=pg.mkPen('black'))
        # # self.gongqingzhanbi.addLine(x=1, pen=pg.mkPen('black'))

        # 获取原 gongqingzhanbi 的父布局
        parent_layout = self.ui.gongqingzhanbi.parentWidget().layout()
        # 移除原 gongqingzhanbi
        parent_layout.removeWidget(self.ui.gongqingzhanbi)
        self.ui.gongqingzhanbi.deleteLater()
        # 用 PieChartWidget 替代
        self.gongqingzhanbi = PieChartWidget(self)
        parent_layout.addWidget(self.gongqingzhanbi)
        # self.gongqingzhanbi = PieChartWidget(self.ui.gongqingzhanbi)
        # self.gongqingzhanbi.setGeometry(0, 0, self.ui.gongqingzhanbi.width(), self.ui.gongqingzhanbi.height())  # 适配 shishi 大小
        # self.gongqingzhanbi.show()

        # 收益曲线
        self.shouyiquxian = pg.PlotWidget()
        parent_layout = self.ui.shouyiquxian.parentWidget().layout()
        parent_layout.removeWidget(self.ui.shouyiquxian)
        self.ui.shouyiquxian.deleteLater()
        parent_layout.addWidget(self.shouyiquxian)
        self.shouyiquxian.setBackground(None)  # 透明色背景色透明
        self.shouyiquxian.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.shouyiquxian.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.shouyiquxian.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.shouyiquxian.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.shouyiquxian.addLine(y=1, pen=pg.mkPen('black'))
        # self.shouyiquxian.addLine(x=1, pen=pg.mkPen('black'))
        self.shouyiquxian.setXRange(0, 24)  # X 轴范围
        self.shouyiquxian.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.shouyiquxian.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.shouyiquxian.setYRange(0, 9000)  # Y 轴范围
        self.shouyiquxian.setLabel('left', '收益 (元)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\zhiqing\制氢预计收益.csv", self.shouyiquxian)  # 跟着一起改

        self.show()

        self.ui.pushButton_main.clicked.connect(self.go_to_inter_main)
        self.ui.pushButton_fengji.clicked.connect(self.go_to_inter_fengji)
        self.ui.pushButton_zhiqing.clicked.connect(self.go_to_inter_zhiqing)
        self.ui.pushButton_rengong.clicked.connect(self.go_to_inter_rengong)

    def go_to_inter_main(self):
        self.win = InterfaceWindow()
        self.close()

    def go_to_inter_fengji(self):
        self.win = fengji()
        self.close()

    def go_to_inter_zhiqing(self):
        self.win = zhiqing()
        self.close()

    def go_to_inter_rengong(self):
        self.win = rengong()
        self.close()

    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # 读取数据画图
    def load_csv_and_plot(self, file_path, target_plot):
        try:
            # 读取 CSV 数据
            data = pd.read_csv(file_path)

            # 确保 CSV 里至少有两列
            if len(data.columns) < 2:
                print("CSV 数据格式错误，至少需要两列")
                return

            x = data.iloc[:, 0]  # 第一列作为 X 轴
            y = data.iloc[:, 1]  # 第二列作为 Y 轴

            # 清除旧图
            target_plot.clear()

            # 画新图
            target_plot.plot(x, y, pen=pg.mkPen('b', width=2))

        except Exception as e:
            print(f"读取 CSV 失败: {e}")

# 人工页面,done
class rengong(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_rengong()  # 绑定 UI,不同的UI就靠这个改
        self.ui.setupUi(self)  # 设置 UI 到当前窗口
        self.adjustSize()  # 让窗口自动调整到适合的大小

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明

        # 将ui中的widge换成xy图
        # 风力发电
        self.fenglifadian = pg.PlotWidget()
        parent_layout = self.ui.fenglifadian.parentWidget().layout()
        parent_layout.removeWidget(self.ui.fenglifadian)
        self.ui.fenglifadian.deleteLater()
        parent_layout.addWidget(self.fenglifadian)
        self.fenglifadian.setBackground(None)  # 透明色背景色透明
        self.fenglifadian.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.fenglifadian.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.fenglifadian.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.fenglifadian.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.fenglifadian.addLine(y=1, pen=pg.mkPen('black'))
        # self.fenglifadian.addLine(x=1, pen=pg.mkPen('black'))
        self.fenglifadian.setXRange(0, 24)  # X 轴范围
        self.fenglifadian.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.fenglifadian.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.fenglifadian.setYRange(0, 1)  # Y 轴范围
        self.fenglifadian.setLabel('left', '发电量 (kW)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\rengong\风机发电量.csv", self.fenglifadian)  # 跟着一起改

        # 制氢收益
        self.zhiqingshouyi = pg.PlotWidget()
        parent_layout = self.ui.zhiqingshouyi.parentWidget().layout()
        parent_layout.removeWidget(self.ui.zhiqingshouyi)
        self.ui.zhiqingshouyi.deleteLater()
        parent_layout.addWidget(self.zhiqingshouyi)
        self.zhiqingshouyi.setBackground(None)  # 透明色背景色透明
        self.zhiqingshouyi.getAxis('bottom').setPen(QPen(pg.mkColor('black')))  # X 轴黑色
        self.zhiqingshouyi.getAxis('left').setPen(QPen(pg.mkColor('black')))  # Y 轴黑色
        self.zhiqingshouyi.getAxis('bottom').setTextPen(QPen(pg.mkColor('black')))  # X 轴字体黑色
        self.zhiqingshouyi.getAxis('left').setTextPen(QPen(pg.mkColor('black')))  # Y 轴字体黑色
        # self.zhiqingshouyi.addLine(y=1, pen=pg.mkPen('black'))
        # self.zhiqingshouyi.addLine(x=1, pen=pg.mkPen('black'))
        self.zhiqingshouyi.setXRange(0, 24)  # X 轴范围
        self.zhiqingshouyi.getAxis('bottom').setTicks([[(i, str(i)) for i in range(0, 30, 5)]])  # x轴刻度间隔 4
        self.zhiqingshouyi.setLabel('bottom', '时间 (分钟)', **{'color': 'black', 'font-size': '10pt'})  # 设置x轴刻度
        self.zhiqingshouyi.setYRange(0, 9000)  # Y 轴范围
        self.zhiqingshouyi.setLabel('left', '收益 (元)', **{'color': 'black', 'font-size': '10pt'})  # 设置y轴刻度
        self.load_csv_and_plot(r"D:\a_study\exe\fengqing_exe\data\rengong\制氢预计收益.csv", self.zhiqingshouyi)  # 跟着一起改

        self.show()

        self.ui.pushButton_main.clicked.connect(self.go_to_inter_main)
        self.ui.pushButton_fengji.clicked.connect(self.go_to_inter_fengji)
        self.ui.pushButton_zhiqing.clicked.connect(self.go_to_inter_zhiqing)
        self.ui.pushButton_rengong.clicked.connect(self.go_to_inter_rengong)

    def go_to_inter_main(self):
        self.win = InterfaceWindow()
        self.close()

    def go_to_inter_fengji(self):
        self.win = fengji()
        self.close()

    def go_to_inter_zhiqing(self):
        self.win = zhiqing()
        self.close()

    def go_to_inter_rengong(self):
        self.win = rengong()
        self.close()

    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # 读取数据画图
    def load_csv_and_plot(self, file_path, target_plot):
        try:
            # 读取 CSV 数据
            data = pd.read_csv(file_path)

            # 确保 CSV 里至少有两列
            if len(data.columns) < 2:
                print("CSV 数据格式错误，至少需要两列")
                return

            x = data.iloc[:, 0]  # 第一列作为 X 轴
            y = data.iloc[:, 1]  # 第二列作为 Y 轴

            # 清除旧图
            target_plot.clear()

            # 画新图
            target_plot.plot(x, y, pen=pg.mkPen('b', width=2))

        except Exception as e:
            print(f"读取 CSV 失败: {e}")


if __name__ == '__main__':
    # 解决窗口与实际python代码运行窗口不一致
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    win = LoginWindow()     # 改这个切换不同页面
    sys.exit(app.exec_())
