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
        MainWindow.resize(1307, 671)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.label_title = QtGui.QLabel(self.centralWidget)
        self.label_title.setGeometry(QtCore.QRect(480, 10, 331, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.label_image = QtGui.QLabel(self.centralWidget)
        self.label_image.setGeometry(QtCore.QRect(130, 70, 1024, 125))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy)
        self.label_image.setObjectName(_fromUtf8("label_image"))
        self.btn_auto_test = QtGui.QPushButton(self.centralWidget)
        self.btn_auto_test.setGeometry(QtCore.QRect(950, 540, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_auto_test.sizePolicy().hasHeightForWidth())
        self.btn_auto_test.setSizePolicy(sizePolicy)
        self.btn_auto_test.setObjectName(_fromUtf8("btn_auto_test"))
        self.btn_start_system = QtGui.QPushButton(self.centralWidget)
        self.btn_start_system.setGeometry(QtCore.QRect(630, 540, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start_system.sizePolicy().hasHeightForWidth())
        self.btn_start_system.setSizePolicy(sizePolicy)
        self.btn_start_system.setObjectName(_fromUtf8("btn_start_system"))
        self.btn_close_system = QtGui.QPushButton(self.centralWidget)
        self.btn_close_system.setGeometry(QtCore.QRect(630, 600, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close_system.sizePolicy().hasHeightForWidth())
        self.btn_close_system.setSizePolicy(sizePolicy)
        self.btn_close_system.setObjectName(_fromUtf8("btn_close_system"))
        self.label_canny = QtGui.QLabel(self.centralWidget)
        self.label_canny.setGeometry(QtCore.QRect(130, 200, 1024, 125))
        self.label_canny.setObjectName(_fromUtf8("label_canny"))
        self.btn_savefile = QtGui.QPushButton(self.centralWidget)
        self.btn_savefile.setGeometry(QtCore.QRect(790, 600, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_savefile.sizePolicy().hasHeightForWidth())
        self.btn_savefile.setSizePolicy(sizePolicy)
        self.btn_savefile.setObjectName(_fromUtf8("btn_savefile"))
        self.progressBar = QtGui.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(180, 600, 301, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.table = QtGui.QTableWidget(self.centralWidget)
        self.table.setGeometry(QtCore.QRect(100, 330, 1081, 192))
        self.table.setObjectName(_fromUtf8("table"))
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.btn_show = QtGui.QPushButton(self.centralWidget)
        self.btn_show.setGeometry(QtCore.QRect(190, 540, 81, 41))
        self.btn_show.setObjectName(_fromUtf8("btn_show"))
        self.label_wave_height = QtGui.QLabel(self.centralWidget)
        self.label_wave_height.setGeometry(QtCore.QRect(270, 540, 131, 31))
        self.label_wave_height.setObjectName(_fromUtf8("label_wave_height"))
        self.btn_cancel = QtGui.QPushButton(self.centralWidget)
        self.btn_cancel.setGeometry(QtCore.QRect(950, 600, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.btn_focus = QtGui.QPushButton(self.centralWidget)
        self.btn_focus.setGeometry(QtCore.QRect(790, 540, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_focus.sizePolicy().hasHeightForWidth())
        self.btn_focus.setSizePolicy(sizePolicy)
        self.btn_focus.setObjectName(_fromUtf8("btn_focus"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_title.setText(_translate("MainWindow", "高晟变形钢丝自动测量仪", None))
        self.label_image.setText(_translate("MainWindow", "图像1024*125,从2048*250变换得来", None))
        self.btn_auto_test.setText(_translate("MainWindow", "自动测量", None))
        self.btn_start_system.setText(_translate("MainWindow", "打开系统", None))
        self.btn_close_system.setText(_translate("MainWindow", "关闭系统", None))
        self.label_canny.setText(_translate("MainWindow", "提取后图像1024*125,从2048*250变换得来", None))
        self.btn_savefile.setText(_translate("MainWindow", "保存", None))
        self.btn_show.setText(_translate("MainWindow", "波高值", None))
        self.label_wave_height.setText(_translate("MainWindow", "Wave Height", None))
        self.btn_cancel.setText(_translate("MainWindow", "取消测量", None))
        self.btn_focus.setText(_translate("MainWindow", "重新对焦", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

