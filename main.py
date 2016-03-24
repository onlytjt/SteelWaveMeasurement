#!/usr/bin/python
# -*- coding:utf-8 -*-


import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from LoginDialog import LoginDialog
from MainWindow import MainUI


def login():
    dialog = LoginDialog()
    if dialog.exec_():
        return True
    else:
        return False

def main():
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    if dialog.exec_():
        mainWindow = MainUI()
        mainWindow.setUsername(dialog.username)
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
