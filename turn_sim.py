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

        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene(self.graphicsView)
        self.scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(self.scene)

        self.plot_button = QPushButton("plot", self)
        self.plot_button.setCheckable(True)
        self.plot_button.toggled.connect(self.slot_plot_button_toggled)

        self.save_button = QPushButton("save", self)
        self.save_button.clicked.connect(self.slot_save_button_pushed)

        validator = QDoubleValidator(-400, 400, 2)
        self.paramEdit1 = QLineEdit()
        self.paramEdit1.setValidator(validator)
        param1layout = QHBoxLayout()
        param1layout.addWidget(QLabel("inner:"))
        param1layout.addWidget(self.paramEdit1)
        param1layout.addWidget(QLabel("[mm]"))

        self.paramEdit2 = QLineEdit()
        self.paramEdit2.setValidator(validator)
        param2layout = QHBoxLayout()
        param2layout.addWidget(QLabel("radius:"))
        param2layout.addWidget(self.paramEdit2)
        param2layout.addWidget(QLabel("[mm]"))

        self.paramOutput1 = QLineEdit()
        self.paramOutput1.setValidator(validator)
        self.paramOutput1.setReadOnly(True)
        param3layout = QHBoxLayout()
        param3layout.addWidget(QLabel("outer:"))
        param3layout.addWidget(self.paramOutput1)
        param3layout.addWidget(QLabel("[mm]"))

        self.combo = QComboBox(self)
        self.combo.addItem("-- select --")
        self.combo.addItem("90(search)")
        self.combo.addItem("45")
        self.combo.addItem("90(short)")
        self.combo.addItem("135")
        self.combo.addItem("180")
        self.combo.addItem("90(slanting)")
        self.combo.activated[str].connect(self.slot_pattern_combo)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.plot_button)
        layout2.addWidget(self.save_button)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.combo)
        layout3.addLayout(param1layout)
        layout3.addLayout(param2layout)
        layout3.addLayout(param3layout)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.graphicsView)

        mainlayout = QHBoxLayout()

        layout1.addLayout(layout2)
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout3)
        self.setLayout(mainlayout)

    def slot_plot_button_toggled(self, checked):
        if checked:
            if self.pattern == "90(search)":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 200
                    self.paramEdit1.setText(str(350-start_y))
                else:
                    start_y = 350 - float(self.paramEdit1.text())
                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)
                angle = 90
                if self.paramEdit2.text() == "":
                    radius = 75
                    self.paramEdit2.setText(str(radius))
                else:
                    radius = float(self.paramEdit2.text())
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 355, end_y)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(end_x-200))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)
            elif self.pattern == "45":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 275
                    self.paramEdit1.setText(str(0))
                else:
                    start_y = 275 - float(self.paramEdit1.text())
                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)
                angle = 45
                if self.paramEdit2.text() == "":
                    radius = 200
                    self.paramEdit2.setText(str(radius))
                else:
                    radius = float(self.paramEdit2.text())
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, end_x+end_y-50, 50)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(np.sqrt(2*(end_y-50)*(end_y-50))))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)
            elif self.pattern == "90(short)":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 275
                    self.paramEdit1.setText(str(0))
                else:
                    start_y = 275 - float(self.paramEdit1.text())
                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)
                angle = 90
                if self.paramEdit2.text() == "":
                    radius = 150
                    self.paramEdit2.setText(str(radius))
                else:
                    radius = float(self.paramEdit2.text())
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 355, end_y)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(end_x-200))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)
            elif self.pattern == "135":
                self.maze_draw(self.pattern)
            elif self.pattern == "180":
                self.maze_draw(self.pattern)
            elif self.pattern == "90(slanting)":
                self.maze_draw(self.pattern)
        else:
            pass

    def slot_save_button_pushed(self):
        try:
            pass
        except:
            pass

    def slot_pattern_combo(self, pattern):
        self.pattern = pattern
        self.maze_draw(pattern)
    def maze_draw(self, pattern):
        if pattern == "90(search)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(345, 45, 10, 160)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "45":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 45, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(rect4)
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "90(short)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(345, 45, 10, 160)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "135":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(345, 195, 10, 160)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(rect5)
            self.scene.addItem(QGraphicsRectItem(195, 345, 160, 10))
        elif pattern == "180":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(195, 345, 160, 10)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(QGraphicsRectItem(345, 195, 10, 160))
            self.scene.addItem(rect5)
        elif pattern == "90(slanting)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 195, 10, 160)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(345, 195, 10, 160)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(rect1)
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 345, 160, 10))
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(rect5)
            self.scene.addItem(QGraphicsRectItem(195, 345, 160, 10))
        else:
            self.scene.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
