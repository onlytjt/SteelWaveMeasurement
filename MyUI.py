# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'validui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1305, 765)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.label_title = QtGui.QLabel(self.centralWidget)
        self.label_title.setGeometry(QtCore.QRect(520, 20, 251, 41))
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(570, 80, 151, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_image = QtGui.QLabel(self.centralWidget)
        self.label_image.setGeometry(QtCore.QRect(30, 170, 1226, 100))
        self.label_image.setObjectName(_fromUtf8("label_image"))
        self.btn_auto_test = QtGui.QPushButton(self.centralWidget)
        self.btn_auto_test.setGeometry(QtCore.QRect(940, 590, 301, 71))
        self.btn_auto_test.setObjectName(_fromUtf8("btn_auto_test"))
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(46, 506, 48, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.edit_big_height = QtGui.QLineEdit(self.centralWidget)
        self.edit_big_height.setEnabled(False)
        self.edit_big_height.setGeometry(QtCore.QRect(100, 506, 531, 20))
        self.edit_big_height.setObjectName(_fromUtf8("edit_big_height"))
        self.label_5 = QtGui.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(46, 534, 48, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.edit_big_length = QtGui.QLineEdit(self.centralWidget)
        self.edit_big_length.setEnabled(False)
        self.edit_big_length.setGeometry(QtCore.QRect(100, 534, 531, 20))
        self.edit_big_length.setObjectName(_fromUtf8("edit_big_length"))
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(46, 562, 48, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.edit_small_height = QtGui.QLineEdit(self.centralWidget)
        self.edit_small_height.setEnabled(False)
        self.edit_small_height.setGeometry(QtCore.QRect(100, 562, 531, 20))
        self.edit_small_height.setObjectName(_fromUtf8("edit_small_height"))
        self.label_7 = QtGui.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(46, 590, 48, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.edit_small_length = QtGui.QLineEdit(self.centralWidget)
        self.edit_small_length.setEnabled(False)
        self.edit_small_length.setGeometry(QtCore.QRect(100, 590, 531, 20))
        self.edit_small_length.setObjectName(_fromUtf8("edit_small_length"))
        self.lineEdit_5 = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(950, 690, 191, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.btn_start_system = QtGui.QPushButton(self.centralWidget)
        self.btn_start_system.setGeometry(QtCore.QRect(940, 510, 151, 61))
        self.btn_start_system.setObjectName(_fromUtf8("btn_start_system"))
        self.btn_close_system = QtGui.QPushButton(self.centralWidget)
        self.btn_close_system.setGeometry(QtCore.QRect(1100, 510, 141, 61))
        self.btn_close_system.setObjectName(_fromUtf8("btn_close_system"))
        self.label_canny = QtGui.QLabel(self.centralWidget)
        self.label_canny.setGeometry(QtCore.QRect(30, 340, 1226, 100))
        self.label_canny.setObjectName(_fromUtf8("label_canny"))
        self.btn_savefile = QtGui.QPushButton(self.centralWidget)
        self.btn_savefile.setGeometry(QtCore.QRect(1160, 690, 75, 23))
        self.btn_savefile.setObjectName(_fromUtf8("btn_savefile"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_title.setText(_translate("MainWindow", "宝钢自动钢丝测量仪", None))
        self.label_2.setText(_translate("MainWindow", "开发单位：上海交通大学", None))
        self.label_image.setText(_translate("MainWindow", "图像显示区域1226*100", None))
        self.btn_auto_test.setText(_translate("MainWindow", "自动测量", None))
        self.label_4.setText(_translate("MainWindow", "大波波高", None))
        self.label_5.setText(_translate("MainWindow", "大波波长", None))
        self.label_6.setText(_translate("MainWindow", "小波波高", None))
        self.label_7.setText(_translate("MainWindow", "小波波长", None))
        self.btn_start_system.setText(_translate("MainWindow", "打开系统", None))
        self.btn_close_system.setText(_translate("MainWindow", "关闭系统", None))
        self.label_canny.setText(_translate("MainWindow", "边缘显示区域1226*100", None))
        self.btn_savefile.setText(_translate("MainWindow", "保存", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

