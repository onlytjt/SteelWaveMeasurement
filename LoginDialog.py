#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from LoginUI import Ui_Dialog

class LoginDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)
        self.adjustUI()
        self.btn_login.clicked.connect(lambda: self.onClickedBtnLogin())
        self.btn_exit.clicked.connect(lambda: self.onClickedBtnExit())

    def adjustUI(self):
        self.setWindowIcon(QIcon("./res/sjtu.jpg"))  # 设置图标
        pe = QPalette()  # 设置标题的字体，字号，颜色
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setPalette(pe)
        self.label_title.setFont(QFont("Roman times", 15, QFont.Bold))
        self.edit_password.setEchoMode(QLineEdit.Password)


    def onClickedBtnLogin(self):
        f = file("./data/user.csv", "rb")
        reader = csv.reader(f)
        for row in reader:
            if unicode(self.edit_username.text()) == row[0].decode("gbk") and self.edit_password.text() == row[1]:
                self.username = row[0].decode("gbk")  # 将文件中gbk的格式解码为unicode格式，并保存
                self.accept()
                f.close()
                return
        f.close()
        QMessageBox.information(None, "Error", u"用户名或密码错误")


    def onClickedBtnExit(self):
        self.close()

