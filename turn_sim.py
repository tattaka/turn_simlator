import sys
import os
import re
import csv

import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Turn Simulator')

        self.plot_button = QPushButton("start", self)
        self.plot_button.setCheckable(True)
        self.plot_button.toggled.connect(self.slot_plot_button_toggled)

        self.reset_button = QPushButton("reset", self)
        self.reset_button.clicked.connect(self.slot_reset_button_pushed)

        self.save_button = QPushButton("save", self)
        self.save_button.clicked.connect(self.slot_save_button_pushed)

        self.label1 = QLabel("test1")
        self.label2 = QLabel("test2")

        layout2 = QHBoxLayout()
        layout2.addWidget(self.plot_button)
        layout2.addWidget(self.reset_button)
        layout2.addWidget(self.save_button)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.label1)
        layout3.addWidget(self.label2)

        layout = QVBoxLayout()

        layout.addLayout(layout3)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def slot_plot_button_toggled(self, checked):
        if checked:
            pass
        else:
            pass

    def slot_reset_button_pushed(self):
        pass

    def slot_save_button_pushed(self):
        try:
            pass
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
