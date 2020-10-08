# -*- coding: utf-8 -*-
# Use python 3.8
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from k2_interface import UiMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("images\\icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
    app.setWindowIcon(icon)

    win = UiMainWindow()
    win.show()

    sys.exit(app.exec_())