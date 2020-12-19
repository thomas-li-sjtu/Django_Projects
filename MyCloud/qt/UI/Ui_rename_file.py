# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\MyCloud\qt\UI\rename_file.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RenameWindow(object):
    def setupUi(self, RenameWindow):
        RenameWindow.setObjectName("RenameWindow")
        RenameWindow.resize(516, 345)
        self.centralwidget = QtWidgets.QWidget(RenameWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 50, 441, 181))
        self.widget.setObjectName("widget")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 130, 101, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 60, 171, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(330, 60, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(10, 10, 441, 41))
        self.widget_3.setObjectName("widget_3")
        self.minButton = QtWidgets.QPushButton(self.widget_3)
        self.minButton.setGeometry(QtCore.QRect(350, 0, 41, 41))
        self.minButton.setText("")
        self.minButton.setObjectName("minButton")
        self.closeButton = QtWidgets.QPushButton(self.widget_3)
        self.closeButton.setGeometry(QtCore.QRect(390, 0, 41, 41))
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 101, 41))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        RenameWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RenameWindow)
        QtCore.QMetaObject.connectSlotsByName(RenameWindow)

    def retranslateUi(self, RenameWindow):
        _translate = QtCore.QCoreApplication.translate
        RenameWindow.setWindowTitle(_translate("RenameWindow", "文件重命名"))
        self.pushButton_2.setText(_translate("RenameWindow", "重命名"))
        self.label.setText(_translate("RenameWindow", "新文件名:"))
        self.label_3.setText(_translate("RenameWindow", "重命名"))
