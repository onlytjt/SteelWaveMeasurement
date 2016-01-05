#!/usr/bin/python
# -*- coding:utf-8 -*-

import MainWindow
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def main():
    app = QApplication(sys.argv)
    ui = MainWindow.MainUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
