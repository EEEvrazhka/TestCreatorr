# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestCreator.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(320, 10, 431, 41))
        self.lineEdit.setStyleSheet("background-color: #f0f0f0; /* Цвет фона */\n"
"    color: #333; /* Цвет текста */\n"
"    font-size: 16px; /* Размер шрифта */\n"
"    font-family: Arial, sans-serif; /* Шрифт */\n"
"    padding: 10px; /* Отступы внутри QLabel */\n"
"    border: 2px solid #007BFF; /* Цвет и толщина рамки */\n"
"    border-radius: 5px; /* Закругление углов */\n"
"    text-align: center; /* Выравнивание текста по центру */")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(590, 70, 161, 41))
        self.pushButton.setStyleSheet("background-color: #007BFF; /* Цвет фона кнопки */\n"
"    color: white; /* Цвет текста */\n"
"    font-size: 16px; /* Размер шрифта */\n"
"    font-family: Arial, sans-serif; /* Шрифт */\n"
"    padding: 10px 20px; /* Отступы внутри кнопки */\n"
"    border: none; /* Без рамки */\n"
"    border-radius: 5px; /* Закругление углов */\n"
"    cursor: pointer; /* Указатель при наведении */")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 490, 201, 41))
        self.pushButton_2.setStyleSheet("background-color: #007BFF; /* Цвет фона кнопки */\n"
"    color: white; /* Цвет текста */\n"
"    font-size: 16px; /* Размер шрифта */\n"
"    font-family: Arial, sans-serif; /* Шрифт */\n"
"    padding: 10px 20px; /* Отступы внутри кнопки */\n"
"    border: none; /* Без рамки */\n"
"    border-radius: 5px; /* Закругление углов */\n"
"    cursor: pointer; /* Указатель при наведении */")
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setText(_translate("MainWindow", "Введите название теста"))
        self.pushButton.setText(_translate("MainWindow", "Добавить тест"))
        self.pushButton_2.setText(_translate("MainWindow", "Выйти из приложения"))
