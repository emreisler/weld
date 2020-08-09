import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFrame, QLineEdit,QMainWindow
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication
import visa
import time
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore
import random
import os 
from multiprocessing import Pool 
import threading


class MainPage(QWidget):
    def __init__(self, title = ""):
        super().__init__() #inherit init of QWidget
        self.title = title
        self.left = 200
        self.top = 200
        self.width = 1400
        self.height = 800
        self.maxLen = 50
        
        self.voltageMeasurements = deque()
        self.currentMeasurements = deque()
        
        self.graph()
        self.widget()

    def widget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        self.inputs()
        self.buttons()
        self.show()
    
    def inputs(self):
        
        self.lengthInput = QLineEdit(self)
        self.lengthInput.setGeometry(QRect(50,50,150,20))
        self.lengthInput.setPlaceholderText("Length of bond line")
        
        self.widthInput = QLineEdit(self)
        self.widthInput.setGeometry(QRect(50,100,150,20))
        self.widthInput.setPlaceholderText("Width of bond line")
        
        self.voltageInput = QLineEdit(self)
        self.voltageInput.setGeometry(QRect(50,150,150,20))
        self.voltageInput.setPlaceholderText("Voltage")
        
        self.curentInput = QLineEdit(self)
        self.curentInput.setGeometry(QRect(50,200,150,20))
        self.curentInput.setPlaceholderText("Current")
        
        self.timeInput = QLineEdit(self)
        self.timeInput.setGeometry(QRect(50,250,150,20))
        self.timeInput.setPlaceholderText("time")
    
    def buttons(self):

        self.runButton = QPushButton("SET PARAMETERS",self)
        self.runButton.setGeometry(QRect(50,300,150,20))
        self.runButton.clicked.connect(self.set_parameters)
        
        self.runButton = QPushButton("RUN",self)
        self.runButton.setGeometry(QRect(50,350,150,20))
        
        self.runButton.clicked.connect(self.runCycle)
        
    def graph(self):
        
        self.graphUpdateSpeed = 1000
        self.appGraph = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        self.win.setGeometry(QRect(self.width-450,50, 750,750))

        self.p1 = self.win.addPlot(colspan=2)
        self.p1.setLabel('left', 'Voltage,Current', units='V,ohm')
        self.p1.setLabel('bottom', 'Time', units='s')
        
        self.curve1 = self.p1.plot(self.voltageMeasurements,pen=pg.mkPen('r'),symbol='x', symbolPen='b', symbolBrush=0.2, name='Voltage')
        self.curve2 = self.p1.plot(self.currentMeasurements,pen=pg.mkPen('g'),symbol='o', symbolPen='b', symbolBrush=0.2, name='Current')
        
    def set_parameters(self):
        self.voltage = int(self.voltageInput.text())
        self.current = int(self.curentInput.text())
        self.cycleTime = int(self.timeInput.text())
        
        print(self.voltage)
        print(self.current)
        print(self.cycleTime)   
        
    def runCycle(self):
        
        rm = visa.ResourceManager()
        SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
        time.sleep(0.5)
        SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage))
        SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current))
        time.sleep(0.2)
        for i in range(self.cycleTime):
            time.sleep(0.5)
            temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
            self.measured_voltage = temp_values[0]
            self.voltageMeasurements.append(self.measured_voltage); 
            
            time.sleep(0.5)
            
            temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
            self.measured_current = temp_values[0]
            self.currentMeasurements.append(self.measured_current); 
            
            self.curve1.setData(self.voltageMeasurements)
            self.curve2.setData(self.currentMeasurements)
            
            print(self.voltageMeasurements)
            print(self.currentMeasurements)

            self.appGraph.processEvents()
        SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
        SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
        SGX50X200D.write('*RST')     
        SGX50X200D.close()
        rm.close()    

def main():
    app = QApplication(sys.argv)
    window = MainPage(title = "Resistance Welding")
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main() 