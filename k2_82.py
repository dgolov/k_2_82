# -*- coding: utf-8 -*-
# Use python 3.8

import sys
from PyQt5.QtWidgets import QApplication
from k2_interface import UiMainWindow


if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = UiMainWindow()
    win.init_ui()
    win.show()

    sys.exit(app.exec_())