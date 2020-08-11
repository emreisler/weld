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
import math



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
        self.setVoltage1 = deque()
        self.setCurrent1 = deque()
        self.setVoltage2 = deque()
        self.setCurrent2 = deque()
        self.resistanceMeasurements = deque()
        self.graphTime = deque()
        
        
        
        self.graph()
        self.widget()

    def widget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        self.inputs()
        self.buttons()
        self.show()
    
    def inputs(self):
        
        self.lengthInputLabel = QLabel("Length(mm) : ",self)
        self.lengthInputLabel.setGeometry(QRect(50,10,150,30))
        
        self.widthInputLabel = QLabel("Width(mm) : ",self)
        self.widthInputLabel.setGeometry(QRect(50,50,150,30))
        
        self.widthInputLabel = QLabel("Resistance(ohm) : ",self)
        self.widthInputLabel.setGeometry(QRect(50,100,150,30))
        
        self.voltageInputLabel = QLabel("Voltage(V) : ",self)
        self.voltageInputLabel.setGeometry(QRect(50,150,150,30))
        
        self.currentInputLabel = QLabel("Current(A) : ",self)
        self.currentInputLabel.setGeometry(QRect(50,200,150,30))
        
        self.timeInputLabel = QLabel("Time(s) : ",self)
        self.timeInputLabel.setGeometry(QRect(50,250,150,30)) 
        
        self.lengthInput = QLineEdit(self)
        self.lengthInput.setGeometry(QRect(150,10,150,30))
        self.lengthInput.setPlaceholderText("Length of bond line")
        
        self.widthInput = QLineEdit(self)
        self.widthInput.setGeometry(QRect(150,50,150,30))
        self.widthInput.setPlaceholderText("Width of bond line")
        
        self.resistanceInput = QLineEdit(self)
        self.resistanceInput.setGeometry(QRect(150,100,150,30))
        self.resistanceInput.setPlaceholderText("Resistance(ohm)")
        
        
        
        self.voltageInput = QLineEdit(self)
        self.voltageInput.setGeometry(QRect(150,150,150,30))
        self.voltageInput.setPlaceholderText("Voltage (raise)")
        
        self.curentInput = QLineEdit(self)
        self.curentInput.setGeometry(QRect(150,200,150,30))
        self.curentInput.setPlaceholderText("Current (raise)")
        
        self.timeInput = QLineEdit(self)
        self.timeInput.setGeometry(QRect(150,250,150,30))
        self.timeInput.setPlaceholderText("Time (raise)")
        
        self.voltageInput2 = QLineEdit(self)
        self.voltageInput2.setGeometry(QRect(320,150,150,30))
        self.voltageInput2.setPlaceholderText("Voltage (dwell)")
        
        self.curentInput2 = QLineEdit(self)
        self.curentInput2.setGeometry(QRect(320,200,150,30))
        self.curentInput2.setPlaceholderText("Current (dwell)")
        
        self.timeInput2 = QLineEdit(self)
        self.timeInput2.setGeometry(QRect(320,250,150,30))
        self.timeInput2.setPlaceholderText("Time (dwell)")
        
        self.voltageLabel = QLabel("0 volts (raise)",self)
        self.voltageLabel.setGeometry(QRect(50,400,150,20))
        
        self.currentLabel = QLabel("0 ampers (raise)",self)
        self.currentLabel.setGeometry(QRect(50,450,150,20))
        
        self.timeLabel = QLabel("0 seconds (raise)",self)
        self.timeLabel.setGeometry(QRect(50,500,150,20))
        
        self.voltageLabel2 = QLabel("0 volts (dwell)",self)
        self.voltageLabel2.setGeometry(QRect(50,550,150,20))
        
        self.currentLabel2 = QLabel("0 ampers (dwell)",self)
        self.currentLabel2.setGeometry(QRect(50,600,150,20))
        
        self.timeLabel2 = QLabel("0 seconds (dwell)",self)
        self.timeLabel2.setGeometry(QRect(50,650,150,20))
        
        #REFERENCES
        self.referencesLabel = QLabel("<h1>REFERENCES</h1>",self)
        self.referencesLabel.setGeometry(QRect(600,10,150,50))
        
        
        self.raiseHeatFluxLabel = QLabel("Raise Heat Flux :",self)
        self.raiseHeatFluxLabel.setGeometry(QRect(550,100,150,30))
        
        self.raiseHeatFluxInput = QLineEdit(self)
        self.raiseHeatFluxInput.setGeometry(QRect(650,100,150,30))
        self.raiseHeatFluxInput.setText("245")
        
        self.raiseTimeLabel = QLabel("Raise Time :",self)
        self.raiseTimeLabel.setGeometry(QRect(550,150,150,30))
        
        self.raiseTimeInput = QLineEdit(self)
        self.raiseTimeInput.setGeometry(QRect(650,150,150,30))
        self.raiseTimeInput.setText("13")
        
        self.dwellHeatFluxLabel = QLabel("Dwell Heat Flux :",self)
        self.dwellHeatFluxLabel.setGeometry(QRect(550,200,150,30))
        
        self.dwellHeatFluxInput = QLineEdit(self)
        self.dwellHeatFluxInput.setGeometry(QRect(650,200,150,30))
        self.dwellHeatFluxInput.setText("92")
        
        self.dwellTimeLabel = QLabel("Dwell Time :",self)
        self.dwellTimeLabel.setGeometry(QRect(550,250,150,30))
        
        self.dwellTimeInput = QLineEdit(self)
        self.dwellTimeInput.setGeometry(QRect(650,250,150,30))
        self.dwellTimeInput.setText("60")
        
    
    def buttons(self):
        
        self.calculateResistanceButton = QPushButton("CALCULATE RESISTANCE",self)
        self.calculateResistanceButton.setGeometry(QRect(320,10,150,30))
        self.calculateResistanceButton.clicked.connect(self.calculate_resistance)
        
        self.calculateParameterseButton = QPushButton("CALCULATE PARAMETERS",self)
        self.calculateParameterseButton.setGeometry(QRect(320,50,150,30))
        self.calculateParameterseButton.clicked.connect(self.calculate_parameters)
        
        self.set_paramsButton = QPushButton("SET PARAMETERS",self)
        self.set_paramsButton.setGeometry(QRect(50,300,150,30))
        self.set_paramsButton.clicked.connect(self.set_parameters)
        
        self.runButton = QPushButton("RUN",self)
        self.runButton.setGeometry(QRect(50,350,150,30))
        self.runButton.clicked.connect(self.runCycle)
        
        self.resetGraphButton = QPushButton("RESET GRAPH",self)
        self.resetGraphButton.setGeometry(QRect(self.width - 200, self.height-100 ,150,30))
        self.resetGraphButton.clicked.connect(self.reset_graph)
        
    def graph(self):
        
        self.graphUpdateSpeed = 1000
        self.appGraph = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        self.win.setGeometry(QRect(self.width-450,50, 750,750))
        self.listView = QTableView()
        self.p1 = self.win.addPlot(colspan=2,title = "V,A-t")
        
        self.p1.setLabel('left', 'Voltage,Current', units='V,A')
        self.p1.setLabel('bottom', 'Time', units='s')
        self.p1.showGrid(y= True, x = True, alpha = 1.)
        
        
        self.curve1 = self.p1.plot(self.voltageMeasurements,self.graphTime,pen=pg.mkPen('r',width=3))
        self.curve2 = self.p1.plot(self.currentMeasurements,self.graphTime,pen=pg.mkPen('g',width=3))
        self.curve3 = self.p1.plot(self.setVoltage1,pen=pg.mkPen('w',style=QtCore.Qt.DotLine))
        self.curve4 = self.p1.plot(self.setCurrent1,pen=pg.mkPen('w',style=QtCore.Qt.DotLine))
        self.curve5 = self.p1.plot(self.setVoltage2,pen=pg.mkPen('w',style=QtCore.Qt.DashLine))
        self.curve6 = self.p1.plot(self.setCurrent2,pen=pg.mkPen('w',style=QtCore.Qt.DashLine))
        self.curve7 = self.p1.plot(self.resistanceMeasurements,self.graphTime,pen=pg.mkPen('b',width=3))
    
    def reset_graph(self):
        self.voltageMeasurements.clear()
        self.currentMeasurements.clear()
        self.setVoltage1.clear()
        self.setCurrent1.clear()
        self.setVoltage2.clear()
        self.setCurrent2.clear()
        self.resistanceMeasurements.clear()
        self.graphTime.clear()
        self.curve1.clear()
        self.curve2.clear()
        self.curve3.clear()
        self.curve4.clear()
        self.curve5.clear()
        self.curve6.clear()
        self.curve7.clear()
        
        
        
        
    def calculate_resistance(self):
        #rm = visa.ResourceManager()
        #SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
        #time.sleep(1)
        #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (10))
        #time.sleep(2)
        #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (1))
        #time.sleep(3)
        #temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
        #self.measured_voltage = temp_values[0]
        #time.sleep(1)
        #temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
        #self.measured_current = temp_values[0]
        #self.resistanceValue = self.measured_voltage / self.measured_current
        self.resistanceInput.setText("1.2")
        time.sleep(0.5)
        #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
        #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
        #SGX50X200D.write('*RST')     
        #SGX50X200D.close()
        #rm.close()
        
    def calculate_parameters(self):
        try:
            #REFERENCE INPUTS
            self.length = float(self.lengthInput.text())/1000
            self.width = float(self.widthInput.text())/1000
            self.resistance = float(self.resistanceInput.text())
            #calculate area
            self.area = self.length * self.width
            
            #REFERENCE HEAT FLUXES AND TIMES
            self.raiseHeatFlux = float(self.raiseHeatFluxInput.text())
            self.dwellHeatFlux = float(self.dwellHeatFluxInput.text())
            
            self.raiseTimeRef = int(self.raiseTimeInput.text())
            self.dwellTimeRef = int(self.dwellTimeInput.text())
            
            #raise calculations
            self.raisePower = self.raiseHeatFlux * self.area
            
            #☻current
            self.raiseCurrent = math.ceil(math.sqrt(self.raisePower*1000/self.resistance))
            self.curentInput.setText(f"{self.raiseCurrent}")
            
            #voltage
            self.raiseVoltage = math.ceil((self.raiseCurrent * self.resistance) + 5)
            self.voltageInput.setText(f"{self.raiseVoltage}")
            
            #time
            self.timeInput.setText(f"{self.raiseTimeRef}")  
            
            if self.raiseVoltage > 48 :
                self.raiseVoltage = 48
                self.voltageInput.setText(f"{self.raiseVoltage}")
                
                self.raiseCurrent = math.ceil(self.raiseVoltage / self.resistance)
                self.curentInput.setText(f"{self.raiseCurrent}")
                
                self.raisePower = self.raiseCurrent * self.raiseCurrent * self.resistance
                self.raiseFlux = self.raisePower / self.area / 1000
                
                print(self.raisePower)
                print(self.raiseFlux)
                print(self.raiseHeatFlux)
                self.raiseTime = math.ceil(self.raiseHeatFlux / self.raiseFlux * self.raiseTimeRef)
                self.timeInput.setText(f"{self.raiseTime}")
           
            
            #dwell calculations
            self.dwellPower = self.dwellHeatFlux * self.area
            
            #current
            self.dwellCurrent = math.ceil(math.sqrt(self.dwellPower*1000/self.resistance))
            self.curentInput2.setText(f"{self.dwellCurrent}")
            
            #voltage
            self.dwellVoltage = math.ceil((self.dwellCurrent * self.resistance) + 5)
            self.voltageInput2.setText(f"{self.dwellVoltage}")
            
            #time
            self.timeInput2.setText(f"{self.dwellTimeRef}")
            
            if self.dwellVoltage > 48 :
                self.dwellVoltage = 48
                self.voltageInput2.setText(f"{self.dwellVoltage}")
                
                self.dwellCurrent = math.ceil(self.dwellVoltage / self.resistance)
                self.curentInput2.setText(f"{self.dwellCurrent}")
                
                self.dwellPower = self.dwellCurrent * self.dwellCurrent * self.resistance
                self.dwellFlux = self.dwellPower / self.area / 1000
                
                print(self.dwellPower)
                print(self.dwellFlux)
                print(self.raiseHeatFlux)
                self.dwellTime = math.ceil(self.dwellHeatFlux / self.dwellFlux * self.dwellTimeRef)
                self.timeInput2.setText(f"{self.dwellTime}")
        except:
            print("eksik argüman")
        
    def set_parameters(self):
        self.voltage1 = int(self.voltageInput.text())
        self.current1 = int(self.curentInput.text())
        self.cycleTime1 = int(self.timeInput.text())
        
        self.voltage2 = int(self.voltageInput2.text())
        self.current2 = int(self.curentInput2.text())
        self.cycleTime2 = int(self.timeInput2.text())
        
        self.voltageLabel.setText(f"{self.voltage1} volts (raise)")
        self.currentLabel.setText(f"{self.current1} ohms (raise)")
        self.timeLabel.setText(f"{self.cycleTime1} seconds (raise)")
        
        self.voltageLabel2.setText(f"{self.voltage2} volts (dwell)")
        self.currentLabel2.setText(f"{self.current2} ohms (dwell)")
        self.timeLabel2.setText(f"{self.cycleTime2} seconds (dwell)")
        
        for i in range(200):
            self.setVoltage1.append(self.voltage1)
            self.setCurrent1.append(self.current1)
            self.setVoltage2.append(self.voltage2)
            self.setCurrent2.append(self.current2)
            
        self.curve3.setData(self.setVoltage1)
        self.curve4.setData(self.setCurrent1)
        self.curve5.setData(self.setVoltage2)
        self.curve6.setData(self.setCurrent2)
        
        
        print(self.voltage1)
        print(self.current1)
        print(self.cycleTime1)  
        print(self.voltage2)
        print(self.current2)
        print(self.cycleTime2)
        
    def runCycle(self):
        
        #rm = visa.ResourceManager()
        #SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
        time.sleep(0.5)
        #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage1))
        #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current1))
        
        for i in range((5 * self.cycleTime1) + (5 * self.cycleTime2) + 50) :
            
            #if i == (5* self.cycleTime1):
                #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage2))
                #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current2))
            #if i == (5 * self.cycleTime1) + (5 * self.cycleTime2):
                #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
                #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))
                
            time.sleep(0.1)
            
            #temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
            #self.measured_voltage = temp_values[0]
            self.voltageMeasurements.append(self.voltage1-random.randint(-1,1)); 
            
            time.sleep(0.1)
            
            #temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
            #self.measured_current = temp_values[0]
            self.currentMeasurements.append(self.current1-random.randint(-1,1)); 
            
            self.resistanceMeasurements.append(self.voltage1/self.current1)
            
            
            self.graphTime.append(i/5)
                
            self.curve1.setData(self.graphTime,self.voltageMeasurements,)
            self.curve2.setData(self.graphTime,self.currentMeasurements)
            self.curve7.setData(self.graphTime,self.resistanceMeasurements)
            #print(self.voltageMeasurements)
            #print(self.currentMeasurements)
            print(self.graphTime)
            
            

            self.appGraph.processEvents()
        #SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
        #SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
        #SGX50X200D.write('*RST')     
        #SGX50X200D.close()
        #rm.close()    
        return "CYCLE COMPLETED"
def main():
    app = QApplication(sys.argv)
    window = MainPage(title = "Resistance Welding")
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main() 