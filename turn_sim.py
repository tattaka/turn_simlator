import sys
import os
import re
import csv

import numpy as np

from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

import serial


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.init_serial()
        self.dataseries = 1
        self.cycle = 20  # update cycle
        self.dx = self.cycle / 1000
        self.data_range = 200 * 2  # 表示されるデータの数
        self.initUI()

    def init_serial(self):
        self.ser = Myserial()

    def initUI(self):
        self.setWindowTitle('Serial Plot Monitor')

        self.plot_button = QPushButton("start", self)
        self.plot_button.setCheckable(True)
        self.plot_button.toggled.connect(self.slot_plot_button_toggled)
        self.plot_button.setIcon(QtGui.QIcon('resource/icon1.jpg'))

        self.reset_button = QPushButton("reset", self)
        self.reset_button.clicked.connect(self.slot_reset_button_pushed)
        self.reset_button.setIcon(QtGui.QIcon('resource/icon2.jpg'))

        self.save_button = QPushButton("save", self)
        self.save_button.clicked.connect(self.slot_save_button_pushed)
        self.save_button.setIcon(QtGui.QIcon('resource/IMG_1776.PNG'))

        self.label1 = QLabel("baudrate: " + '%d' % self.ser.baudrate())
        self.label2 = QLabel("port: " + self.ser.port())
        self.spinbox = QSpinBox(self)
        self.spinbox.setPrefix("series: ")
        self.spinbox.setRange(1, 4)


        self.guiplot = pg.PlotWidget()
        self.guiplot.plotItem.getAxis('left').setTickSpacing(major = 1, minor = 0.1)
        self.guiplot.plotItem.getAxis('bottom').setTickSpacing(major = 1, minor = 0.1)
        self.zoomplot = pg.PlotWidget()
        self.zoomplot.plotItem.getAxis('left').setTickSpacing(major = 1, minor = 0.1)
        self.zoomplot.plotItem.getAxis('bottom').setTickSpacing(major = 1, minor = 0.1)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.plot_button)
        layout2.addWidget(self.reset_button)
        layout2.addWidget(self.save_button)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.label1)
        layout3.addWidget(self.label2)
        layout3.addWidget(self.spinbox)

        layout = QVBoxLayout()
        layout.addWidget(self.guiplot)
        layout.addWidget(self.zoomplot)

        layout.addLayout(layout3)
        layout.addLayout(layout2)
        self.setLayout(layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_graph)

    def slot_plot_button_toggled(self, checked):
        if checked:
            self.start_plotting()
        else:
            self.stop_plotting()

    def slot_reset_button_pushed(self):
        self.count = 0
        self.dataseries = self.spinbox.value()
        self.data_init()
        self.graphplot()
        self.zoomplot.clear()
        self.zoomplot.plotItem.setRange(
            xRange=(0, 0 + self.data_range * 0.55 * self.dx), padding=0)

    def slot_save_button_pushed(self):
        self.stop_plotting()
        self.f = open('save_data.csv', 'w')
        self.w = csv.writer(self.f)
        try:
            for i in range(len(self.data)):
                self.w.writerow(self.data[i, 0:self.dataseries+1])
            self.f.close()
        except:
            pass

    def start_plotting(self):

        self.init_serial()
        self.label1.setText("baudrate: " + '%d' % self.ser.baudrate())
        self.label2.setText("port: " + self.ser.port())
        self.plot_button.setText('stop')
        self.dataseries = self.spinbox.value()
        self.count = 0
        self.data_init()
        self.graphplot()
        self.guiplot.clear()
        self.zoomplot.clear()
        self.timer.start(self.cycle)

    def stop_plotting(self):
        self.plot_button.setText('start')
        self.timer.stop()
        self.zoomlooking()

    def update_zoomPlot(self):
        self.zoomplot.setXRange(*self.lr.getRegion(), padding=0)

    def update_zoomRegion(self):
        self.lr.setRegion(self.zoomplot.getViewBox().viewRange()[0])

    def data_init(self):
        #self.data = np.zeros(self.dataseries+1)
        #self.data = np.array([self.data])
        self.data = np.array([[self.count, np.sin(self.count * np.pi), np.cos(self.count * np.pi), np.sin(self.count * np.pi)*np.cos(self.count * np.pi), np.sin(self.count * np.pi)+np.cos(self.count * np.pi)]])

    def update_graph(self):
        self.count = self.count + self.dx
        if self.ser.port() != "None":
            count = 0
            data = np.zeros(self.dataseries)
            data = np.array([data])
            while self.ser.inWaiting() > 0:
                data_temp = list(map(float, re.findall(r'\d+\.\d+', self.ser.data())))
                if len(data_temp) < self.dataseries:
                    data_temp = np.append(data_temp, np.zeros(self.dataseries-len(data_temp)))
                elif len(data_temp) > self.dataseries:
                    del(data_temp[self.dataseries:])

                data = np.append(data,  np.array([data_temp]), axis=0)
                count = count + 1

            data = np.delete(data, 0, axis = 0)
            for i in range(1, count + 1):
                v1 = np.array([self.count + self.dx - self.dx * (1 - i / count)])
                v2 = data[i-1]
                data_temp = np.concatenate([v1, v2], axis=0)
                data = np.array([data_temp])
                self.data = np.append(self.data, np.array([data[i - 1]]), axis=0)
            #self.graphplot()
        self.data = np.append(self.data, np.array(
            [[self.count, np.sin(self.count * np.pi), np.cos(self.count * np.pi), np.sin(self.count * np.pi)*np.cos(self.count * np.pi), np.sin(self.count * np.pi)+np.cos(self.count * np.pi)]]), axis=0)
        self.graphplot()

    def graphplot(self):
        self.guiplot.clear()
        if self.count > self.dx * self.data_range / 2:
            self.guiplot.plotItem.setRange(xRange=(
                self.count - self.data_range * 0.5 * self.dx, self.count + self.data_range * 0.05 * self.dx), padding=0)
        else:
            self.guiplot.plotItem.setRange(
                xRange=(0, 0 + self.data_range * 0.55 * self.dx), padding=0)
        for i in range(1, self.dataseries + 1):
            self.guiplot.plotItem.addItem(pg.PlotCurveItem(x=self.data[:, 0],
                                                           y=self.data[:, i]
                                                           ))

    def zoomlooking(self):
        if self.count > self.dx * self.data_range / 2:
            self.lr = pg.LinearRegionItem(
                [self.count - self.data_range * 0.40 * self.dx, self.count - self.data_range * 0.20 * self.dx])
        else:
            self.lr = pg.LinearRegionItem(
                [self.data_range * 0.1 * self.dx, self.data_range * 0.3 * self.dx])
        self.lr.setZValue(-10)
        self.guiplot.addItem(self.lr)
        for i in range(1, self.dataseries + 1):
            self.zoomplot.plotItem.addItem(pg.PlotCurveItem(x=self.data[:, 0],
                                                           y=self.data[:, i]
                                                           ))
        self.lr.sigRegionChanged.connect(self.update_zoomPlot)
        self.zoomplot.sigXRangeChanged.connect(self.update_zoomRegion)
        self.update_zoomPlot()


class Myserial():
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.timeout = 0
        for file in os.listdir('/dev'):
            if "tty.usb" in file:
                self.ser.port = '/dev/' + file
                self.ser.open()

    def baudrate(self):
        return self.ser.baudrate

    def port(self):
        if self.ser.port != None:
            return self.ser.port
        else:
            return "None"

    def data(self):
        if self.ser.port != None:
            data = self.ser.readline()#.strip().rsplit()
            return data
        else:
            return None

    def inWaiting(self):
        return self.ser.in_waiting


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
