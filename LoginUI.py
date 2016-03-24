# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.btn_exit = QtGui.QPushButton(Dialog)
        self.btn_exit.setGeometry(QtCore.QRect(220, 230, 75, 23))
        self.btn_exit.setObjectName(_fromUtf8("btn_exit"))
        self.btn_login = QtGui.QPushButton(Dialog)
        self.btn_login.setGeometry(QtCore.QRect(110, 230, 75, 23))
        self.btn_login.setObjectName(_fromUtf8("btn_login"))
        self.label_title = QtGui.QLabel(Dialog)
        self.label_title.setGeometry(QtCore.QRect(10, 40, 381, 61))
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.label_username = QtGui.QLabel(Dialog)
        self.label_username.setGeometry(QtCore.QRect(90, 120, 51, 16))
        self.label_username.setObjectName(_fromUtf8("label_username"))
        self.label_password = QtGui.QLabel(Dialog)
        self.label_password.setGeometry(QtCore.QRect(100, 170, 31, 16))
        self.label_password.setObjectName(_fromUtf8("label_password"))
        self.edit_username = QtGui.QLineEdit(Dialog)
        self.edit_username.setGeometry(QtCore.QRect(150, 120, 151, 20))
        self.edit_username.setObjectName(_fromUtf8("edit_username"))
        self.edit_password = QtGui.QLineEdit(Dialog)
        self.edit_password.setGeometry(QtCore.QRect(150, 170, 151, 20))
        self.edit_password.setObjectName(_fromUtf8("edit_password"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Login", None))
        self.btn_exit.setText(_translate("Dialog", "退出", None))
        self.btn_login.setText(_translate("Dialog", "登录", None))
        self.label_title.setText(_translate("Dialog", "变形钢丝测量系统用户登录", None))
        self.label_username.setText(_translate("Dialog", "用户名：", None))
        self.label_password.setText(_translate("Dialog", "密码：", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

