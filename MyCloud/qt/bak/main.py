import sys
import os
import qtawesome
root_path = os.getcwd()
sys.path.append(f'{root_path}\\qt')
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui, QtWidgets
from UI.Ui_main_window import Ui_MainWindow
from UI.Ui_login import Ui_LoginWindow
from UI.Ui_register import Ui_RegisterWindow
from UI.Ui_transfer import Ui_TransferWindow
from utils.VerificationCode import WidgetCode
from utils.FramelessDialog import *


ABSOLUTE_PATH = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
BACKGROUND_COLOR = '#F8F8FF'  # 主界面底色
TITLE_COLOR = '#F0E68C'  # 标题栏颜色
FUNC_COLOR = '#FFFFE0'  # 功能栏颜色
LIGHT_FUNC_COLOR = '#FFFFF0'  # 到功能栏颜色的过渡色
HOVER_COLOR = '#00BFFF'  # 按钮点击时的文字颜色
GRAY_COLOR = '#EEF0F6'  # 万能的灰色
GLOBAL_BUTTON = """
QPushButton{
    border:none;
    background:%s
}
QPushButton:hover{
    background:%s;
    border-radius:10px;
    color:%s;
}
#closeButton{
    background:%s;
    max-width: 36px;
    max-height: 36px;
    font-size: 12px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover{
    color: white;
    border:none;
    background: red;
}
#minButton{
    background:%s;
    max-width: 36px;
    max-height: 36px;
    font-family: "Webdings";
    font-size: 12px;
    qproperty-text: "0";
    border-radius: 10px;
}
#minButton:hover{
    color:black;
    border:none;
    background: %s;
}
""" % (FUNC_COLOR, GRAY_COLOR, HOVER_COLOR, TITLE_COLOR, TITLE_COLOR, BACKGROUND_COLOR)


# 经过基本美化的窗体
class BasicWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BasicWindow, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False  # 判断是否按下鼠标
        self.setFixedSize(self.width(), self.height())
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏

    def doShow(self):
        """淡入
        """
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        """淡出
        """
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def mousePressEvent(self, event):
        """鼠标左键按下变小手

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
    def mouseReleaseEvent(self, event):
        """鼠标左键放开变回箭头

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = False
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        """鼠标拖动窗口

        Arguments:
            event -- 事件
        """
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position) #更改窗口位置
            event.accept()


# 主窗口
class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.is_open_tw = False  # 判断是否打开传输列表窗口
        self.m_flag = False  # 判断是否按下鼠标
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
        self.left_column = {'allfile_btn':0, 'doc_btn':1, 'img_btn':2, 'music_btn':3, 'video_btn':4, 'other_btn':5}  # 左边栏
        self.logo.setPixmap(QPixmap(f'{ABSOLUTE_PATH}/img/logo.png').scaled(self.logo.width(), self.logo.height()))  # 添加logo
        self.init_menu()    # 添加用户菜单
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        self.doShow()   # 淡入
        self.init_ui()  # 初始化界面

        # widget美化
        Qss =  'QWidget#widget{background-color:%s;}' % TITLE_COLOR
        Qss += 'QWidget#widget_2{background-color:%s;}' % GRAY_COLOR
        Qss += 'QWidget#widget_3{background-color:%s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_4{background-color:%s;}' % FUNC_COLOR
        Qss += 'QPushButton#user_btn{background-color:%s; border:none; border-radius:10px;}' % TITLE_COLOR
        Qss += '#upload_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (FUNC_COLOR, HOVER_COLOR)
        Qss += '#mkdir_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (FUNC_COLOR, HOVER_COLOR)
        Qss += '#transfer_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (FUNC_COLOR, HOVER_COLOR)
        for btn in self.left_column:
            Qss += '#%s{background-color:%s; border-radius:0;}' % (btn, GRAY_COLOR)
            Qss += '#%s:hover{background-color:%s; border-radius:0;}' % (btn, LIGHT_FUNC_COLOR)
            eval(f'self.{btn}').setCursor(QCursor(Qt.PointingHandCursor))  # 鼠标悬停按钮上时变小手
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss) # 边框部分qss重载

        # 所有按钮的初始化
        self.minButton.clicked.connect(self.showMinimized)
        self.minButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeButton.clicked.connect(self.doClose)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.user_btn.setText('USER')   # 用户名按钮
        self.user_btn.setGeometry(QtCore.QRect(970, 10, 100, 31))
        self.user_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/user.png'))
        self.user_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_btn.setIcon(qtawesome.icon('fa.cloud-upload'))  # 上传按钮
        self.upload_btn.setGeometry(QtCore.QRect(190, 8, 91, 37))
        self.upload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_btn.clicked.connect(self.btn_upload)
        self.mkdir_btn.setIcon(qtawesome.icon('fa.plus-square'))  # 新建文件夹按钮
        self.mkdir_btn.setGeometry(QtCore.QRect(290, 8, 141, 37))
        self.mkdir_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mkdir_btn.clicked.connect(self.btn_mkdir)
        self.back_btn.setIcon(qtawesome.icon('fa.chevron-left'))  # 回退按钮
        self.back_btn.setToolTip('回退')
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_btn.clicked.connect(self.btn_back)
        self.forward_btn.setIcon(qtawesome.icon('fa.chevron-right'))  # 前进按钮
        self.forward_btn.setToolTip('前进')
        self.forward_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.forward_btn.clicked.connect(self.btn_forward)
        self.refresh_btn.setIcon(qtawesome.icon('fa.refresh'))  # 刷新按钮
        self.refresh_btn.setToolTip('刷新')
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.btn_refresh)
        self.lineEdit.setPlaceholderText('搜索网盘文件')
        self.search_btn.setIcon(qtawesome.icon('fa.search'))  # 搜索按钮
        self.search_btn.setToolTip('搜索')
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.clicked.connect(self.btn_search) 
        self.transfer_btn.setIcon(qtawesome.icon('fa.exchange'))  # 传输列表按钮
        self.transfer_btn.setGeometry(QtCore.QRect(480, 8, 111, 37))
        self.transfer_btn.clicked.connect(self.btn_transfer)
        self.allfile_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/folder.png'))  # 全部文件按钮
        self.allfile_btn.clicked.connect(lambda: self.btn_left('allfile_btn'))
        self.doc_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/word.png'))  # 文档按钮
        self.doc_btn.clicked.connect(lambda: self.btn_left('doc_btn'))
        self.music_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/music.png'))  # 音乐按钮
        self.music_btn.clicked.connect(lambda: self.btn_left('music_btn'))
        self.video_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/video.png'))  # 视频按钮
        self.video_btn.clicked.connect(lambda: self.btn_left('video_btn'))
        self.other_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/unknown.png'))  # 其他按钮
        self.other_btn.clicked.connect(lambda: self.btn_left('other_btn'))
        self.img_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/img.png'))  # 图片按钮
        self.img_btn.clicked.connect(lambda: self.btn_left('img_btn'))

    def init_menu(self):
        """用户菜单栏初始化
        """
        self.menu = QMenu(self.user_btn)
        self.menu.addAction('注销', self.logout)
        self.user_btn.setMenu(self.menu)

    def init_ui(self):
        """初始化界面
        """
        self.allfile_btn.setStyleSheet('#allfile_btn{background-color:%s; color:%s; border-left:6px solid %s}' % (FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))
        self.stackedWidget.setCurrentIndex(0)

    def btn_left(self, left_btn):
        """左边栏按钮对应事件
        """
        eval(f'self.{left_btn}').setStyleSheet('#%s{background-color:%s; color:%s; border-left:6px solid %s}' % (left_btn, FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))  # 当前点击按钮高亮
        self.stackedWidget.setCurrentIndex(self.left_column[left_btn])  # 切换当前页面
        for btn in self.left_column:  # 其他按钮全部恢复
            if btn != left_btn:
                eval(f'self.{btn}').setStyleSheet('#%s{background-color:%s; border-radius:0;}' % (btn, GRAY_COLOR))

    def btn_transfer(self):
        """传输列表界面
        """
        def confirm_close(parameter):
            self.is_open_tw = parameter
        if not self.is_open_tw:
            self.transfer_window = Transfer_window()
            self.is_open_tw = True
            self.transfer_window.show()
            self.transfer_window.signal.connect(confirm_close)  # 确认传输窗口关闭
        else:
            self.warn_dialog = Warn_Dialog()
            self.warn_dialog.label.setText('请勿同时打开多个传输列表！')
            self.warn_dialog.show()

    def btn_upload(self):
        """文件上传
        """
        print('文件上传')
    
    def btn_mkdir(self):
        """新建文件夹
        """
        print("新建文件夹")

    def btn_back(self):
        """回退
        """
        print("回退")

    def btn_forward(self):
        """前进
        """
        print("前进")

    def btn_refresh(self):
        """刷新
        """
        print("刷新")

    def btn_search(self):
        """搜索网盘文件
        """
        file_search = self.lineEdit.text()
        print(f'搜索: {file_search}')

    def logout(self):
        """注销账户
        """
        self.login_window = Login_window()
        self.login_window.show()
        self.doClose()

    def doShow(self):
        """淡入
        """
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        """淡出
        """
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def mousePressEvent(self, event):
        """鼠标左键按下变小手

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
    def mouseReleaseEvent(self, event):
        """鼠标左键放开变回箭头

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = False
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        """鼠标拖动窗口

        Arguments:
            event -- 事件
        """
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position) #更改窗口位置
            event.accept()


# 登陆窗口
class Login_window(BasicWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        super(Login_window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_4.setObjectName('closeButton')
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setObjectName('minButton')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # 密码输入不可见

        # widget美化
        Qss =  'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_2{background-color: %s;}' % TITLE_COLOR
        # 注册按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        # 登陆按钮
        Qss += 'QPushButton#pushButton{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss) # 边框部分qss重载

        self.pushButton.clicked.connect(self.btn_login)
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.doClose)
        self.code = WidgetCode(self.widget_3, minimumHeight=35, minimumWidth=80)  # 添加验证码
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        self.doShow()

    # 登陆按钮事件
    def btn_login(self):
        """登陆按钮事件
        """
        user_name = self.lineEdit.text()  # 获取用户输入的用户名
        password = self.lineEdit_2.text()  # 获取用户输入的密码
        code_check = self.code.check(self.lineEdit_3.text())  # 验证码验证
        if not code_check:
            self.main_window = Main_window()
            self.main_window.show()
            self.close()
        else:
            self.doShakeWindow(self)
            self.warn_dialog = Warn_Dialog()
            self.warn_dialog.label.setText('验证码错误！')
            self.warn_dialog.show()

    def btn_register(self):
        """注册按钮事件
        """
        self.register_window = Register_window()
        self.register_window.show()
        self.close()

    def doShakeWindow(self, target):
        """窗口抖动动画

        Arguments:
            target {窗口对象} -- 目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))
        animation.start(animation.DeleteWhenStopped)

    
# # 登陆窗口
# class Login_window(QMainWindow, Ui_LoginWindow):
#     def __init__(self, parent=None):
#         super(Login_window, self).__init__(parent)
#         self.setupUi(self)
#         self.m_flag = False  # 判断是否按下鼠标
#         self.setFixedSize(self.width(), self.height())
#         # self.setWindowOpacity(0.9) # 设置窗口透明度
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
#         self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
#         self.pushButton_4.setObjectName('closeButton')
#         self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
#         self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
#         self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
#         self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
#         self.pushButton_3.setObjectName('minButton')
#         self.lineEdit_2.setEchoMode(QLineEdit.Password)  # 密码输入不可见

#         # widget美化
#         Qss =  'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
#         Qss += 'QWidget#widget_2{background-color: %s;}' % TITLE_COLOR
#         # 注册按钮
#         Qss += 'QPushButton#pushButton_2{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         Qss += 'QPushButton#pushButton_2:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         Qss += 'QPushButton#pushButton_2:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         # 登陆按钮
#         Qss += 'QPushButton#pushButton{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         Qss += 'QPushButton#pushButton:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         Qss += 'QPushButton#pushButton:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
#         Qss += GLOBAL_BUTTON
#         self.setStyleSheet(Qss) # 边框部分qss重载

#         self.pushButton.clicked.connect(self.btn_login)
#         self.pushButton_2.clicked.connect(self.btn_register)
#         self.pushButton_3.clicked.connect(self.showMinimized)
#         self.pushButton_4.clicked.connect(self.doClose)
#         self.code = WidgetCode(self.widget_3, minimumHeight=35, minimumWidth=80)  # 添加验证码
#         self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
#         self.animation.setDuration(500)  # 持续时间0.5秒
#         self.doShow()

#     # 登陆按钮事件
#     def btn_login(self):
#         """登陆按钮事件
#         """
#         user_name = self.lineEdit.text()  # 获取用户输入的用户名
#         password = self.lineEdit_2.text()  # 获取用户输入的密码
#         code_check = self.code.check(self.lineEdit_3.text())  # 验证码验证
#         if not code_check:
#             self.main_window = Main_window()
#             self.main_window.show()
#             self.close()
#         else:
#             self.doShakeWindow(self)
#             self.warn_dialog = Warn_Dialog()
#             self.warn_dialog.label.setText('验证码错误！')
#             self.warn_dialog.show()

#     def btn_register(self):
#         """注册按钮事件
#         """
#         self.register_window = Register_window()
#         self.register_window.show()
#         self.close()

#     def doShakeWindow(self, target):
#         """窗口抖动动画

#         Arguments:
#             target {窗口对象} -- 目标控件
#         """
#         if hasattr(target, '_shake_animation'):
#             # 如果已经有该对象则跳过
#             return

#         animation = QPropertyAnimation(target, b'pos', target)
#         target._shake_animation = animation
#         animation.finished.connect(lambda: delattr(target, '_shake_animation'))

#         pos = target.pos()
#         x, y = pos.x(), pos.y()

#         animation.setDuration(200)
#         animation.setLoopCount(2)
#         animation.setKeyValueAt(0, QPoint(x, y))
#         animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
#         animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
#         animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
#         animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
#         animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
#         animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
#         animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
#         animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
#         animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
#         animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
#         animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
#         animation.setEndValue(QPoint(x, y))
#         animation.start(animation.DeleteWhenStopped)

#     def doShow(self):
#         """淡入
#         """
#         try:
#             # 尝试先取消动画完成后关闭窗口的信号
#             self.animation.finished.disconnect(self.close)
#         except:
#             pass
#         self.animation.stop()
#         # 透明度范围从0逐渐增加到1
#         self.animation.setStartValue(0)
#         self.animation.setEndValue(1)
#         self.animation.start()

#     def doClose(self):
#         """淡出
#         """
#         self.animation.stop()
#         self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
#         # 透明度范围从1逐渐减少到0
#         self.animation.setStartValue(1)
#         self.animation.setEndValue(0)
#         self.animation.start()

#     def mousePressEvent(self, event):
#         """鼠标左键按下变小手

#         Arguments:
#             event -- 事件
#         """
#         if event.button() == QtCore.Qt.LeftButton:
#             self.m_flag = True
#             self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
#             event.accept()
#             self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
#     def mouseReleaseEvent(self, event):
#         """鼠标左键放开变回箭头

#         Arguments:
#             event -- 事件
#         """
#         if event.button() == QtCore.Qt.LeftButton:
#             self.m_flag = False
#             self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

#     def mouseMoveEvent(self, event):
#         """鼠标拖动窗口

#         Arguments:
#             event -- 事件
#         """
#         if QtCore.Qt.LeftButton and self.m_flag:
#             self.move(event.globalPos() - self.m_Position) #更改窗口位置
#             event.accept()



# 注册窗口
class Register_window(QMainWindow, Ui_RegisterWindow):
    def __init__(self, parent=None):
        super(Register_window, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False  # 判断是否按下鼠标
        self.setFixedSize(self.width(), self.height())
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
        self.pushButton_4.setObjectName('closeButton')
        self.pushButton_3.setObjectName('minButton')
        self.lineEdit_2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_3.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        # widget美化
        Qss =  'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_3{background-color: %s;}' % TITLE_COLOR
        # 注册按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss) # 边框部分qss重载

        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.doClose)
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        self.doShow()

    def btn_register(self):
        """登陆按钮事件
        """
        self.login_window = Login_window()
        self.login_window.show()
        self.close()

    def doShow(self):
        """淡入
        """
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        """淡出
        """
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def mousePressEvent(self, event):
        """鼠标左键按下变小手

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
    def mouseReleaseEvent(self, event):
        """鼠标左键放开变回箭头

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = False
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        """鼠标拖动窗口

        Arguments:
            event -- 事件
        """
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position) #更改窗口位置
            event.accept()



# 传输列表界面
class Transfer_window(QMainWindow, Ui_TransferWindow):
    signal = QtCore.pyqtSignal(bool)  # 传递是否关闭窗口的布尔值
    def __init__(self, parent=None):
        super(Transfer_window, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False  # 判断是否按下鼠标
        self.top_column = {'upload_btn':1, 'download_btn':0, 'complete_btn':2}  # 顶部栏
        self.setFixedSize(self.width(), self.height())
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        self.init_ui()  # 界面初始化

        Qss = GLOBAL_BUTTON
        Qss += 'QWidget#widget{background-color:%s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_2{background-color:%s;}' % TITLE_COLOR
        for btn in self.top_column:
            Qss += '#%s{background-color:%s; border-radius:0;}' % (btn, TITLE_COLOR)
            Qss += '#%s:hover{background-color:%s; border-radius:0;}' % (btn, LIGHT_FUNC_COLOR)
            eval(f'self.{btn}').setCursor(QCursor(Qt.PointingHandCursor))  # 鼠标悬停按钮上时变小手
        self.setStyleSheet(Qss) # 边框部分qss重载

        self.closeButton.clicked.connect(self.doClose)
        self.minButton.clicked.connect(self.showMinimized)
        self.upload_btn.clicked.connect(lambda: self.btn_top('upload_btn'))  # 上传列表按钮
        self.upload_btn.setIcon(qtawesome.icon('fa.upload'))
        self.download_btn.clicked.connect(lambda: self.btn_top('download_btn'))  # 下载列表按钮
        self.download_btn.setIcon(qtawesome.icon('fa.download'))
        self.complete_btn.clicked.connect(lambda: self.btn_top('complete_btn'))  # 传输完成按钮
        self.complete_btn.setIcon(qtawesome.icon('fa.check-square-o'))

    def init_ui(self):
        """界面初始化
        """
        self.download_btn.setStyleSheet('#download_btn{background-color:%s; color:%s; border-bottom:5px solid %s}' % (FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))
        self.stackedWidget.setCurrentIndex(0)

    def btn_top(self, top_btn):
        """顶部栏栏按钮对应事件
        """
        eval(f'self.{top_btn}').setStyleSheet('#%s{background-color:%s; color:%s; border-bottom:5px solid %s}' % (top_btn, FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))  # 当前点击按钮高亮
        self.stackedWidget.setCurrentIndex(self.top_column[top_btn])
        for btn in self.top_column:  # 其他按钮全部恢复
            if btn != top_btn:
                eval(f'self.{btn}').setStyleSheet('#%s{background-color:%s; border-radius:0;}' % (btn, TITLE_COLOR))    

    def doShow(self):
        """淡入
        """
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        """淡出
        """
        self.signal.emit(False)  # 发送窗口关闭的信号给父窗口
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def mousePressEvent(self, event):
        """鼠标左键按下变小手

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
    def mouseReleaseEvent(self, event):
        """鼠标左键放开变回箭头

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = False
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        """鼠标拖动窗口

        Arguments:
            event -- 事件
        """
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position) #更改窗口位置
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = Login_window()
    login_window.show()

    sys.exit(app.exec_())
