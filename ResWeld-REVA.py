import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFrame, QLineEdit,QMainWindow,QSplitter,QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication,QLine
from PyQt5.QtGui import QPixmap,QIcon,QFont,QPainter,QPen,QMovie
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
        self.left = 50
        self.top = 50
        self.width = 1400
        self.height = 900
        self.maxLen = 50
        
        self.voltageMeasurements = deque()
        self.currentMeasurements = deque()
        self.setVoltage1 = deque()
        self.setCurrent1 = deque()
        self.setVoltage2 = deque()
        self.setCurrent2 = deque()
        self.resistanceMeasurements = deque()
        self.graphTime = deque()
        self.buttonWidth = 150
        self.buttonHeight = 40
        self.inputWidth = 150
        self.inputHeight = 30
        self.labelWidth = 150
        self.labelHeight = 30

        self.graph()
        self.widget()

    def widget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        self.inputs()
        
        self.show()
    
    def inputs(self):
        
       
        self.label = QLabel(self) 
          
        
        
        self.frameAreaInputs = QFrame(self)
        self.frameAreaInputs.setGeometry(QRect(50,20,675,250))
        self.frameAreaInputs.setStyleSheet("border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        # loading image 
        self.pixmap = QPixmap('images/logo.svg') 
  
        # adding image to label 
        self.label.setPixmap(self.pixmap) 
  
        # Optional, resize label to image size 
        self.label.move(self.width-350,20)
    
        
    
        self.resistanceInputLabel = QLabel("Resistance(ohm) : ",self.frameAreaInputs)
        self.resistanceInputLabel.setGeometry(QRect(50,50,150,30))
        
        self.lengthInputLabel = QLabel("Length(mm) : ",self.frameAreaInputs)
        self.lengthInputLabel.setGeometry(QRect(50,100,150,30))
        
        self.widthInputLabel = QLabel("Width(mm) : ",self.frameAreaInputs)
        self.widthInputLabel.setGeometry(QRect(50,150,150,30))
        
        self.resistanceInput = QLineEdit(self.frameAreaInputs)
        self.resistanceInput.setGeometry(QRect(150,50,150,30))
        self.resistanceInput.setPlaceholderText("Resistance(ohm)")
        
        self.lengthInput = QLineEdit(self.frameAreaInputs)
        self.lengthInput.setGeometry(QRect(150,100,150,30))
        self.lengthInput.setPlaceholderText("Length of bond line")
        
        self.widthInput = QLineEdit(self.frameAreaInputs)
        self.widthInput.setGeometry(QRect(150,150,150,30))
        self.widthInput.setPlaceholderText("Width of bond line")
        
        
        
        self.calculateResistanceButton = QPushButton("CALCULATE RESISTANCE",self.frameAreaInputs)
        self.calculateResistanceButton.setGeometry(QRect(350,50, self.buttonWidth, self.buttonHeight))
        self.calculateResistanceButton.clicked.connect(self.calculate_resistance)
        
        self.calculateParameterseButton = QPushButton("CALCULATE PARAMETERS",self.frameAreaInputs)
        self.calculateParameterseButton.setGeometry(QRect(350,100, self.buttonWidth,self.buttonHeight))
        self.calculateParameterseButton.clicked.connect(self.calculate_parameters)
        
        self.missingDimension = QLabel("",self.frameAreaInputs)
        self.missingDimension.setGeometry(QRect(350,150,150,30))
        self.missingDimension.setStyleSheet("border-style: none;color: red")
        
        self.frameCycleInputs = QFrame(self)
        self.frameCycleInputs.setGeometry(QRect(50,300,675,300))
        self.frameCycleInputs.setStyleSheet("border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.voltageInputLabel = QLabel("Voltage(V) raise : ",self.frameCycleInputs)
        self.voltageInputLabel.setGeometry(QRect(50,50,150,30))
        
        self.currentInputLabel = QLabel("Current(A) raise : ",self.frameCycleInputs)
        self.currentInputLabel.setGeometry(QRect(50,100,150,30))
        
        self.timeInputLabel = QLabel("Time(s) raise : ",self.frameCycleInputs)
        self.timeInputLabel.setGeometry(QRect(50,150,150,30)) 
        
        self.voltageInput = QLineEdit(self.frameCycleInputs)
        self.voltageInput.setGeometry(QRect(150,50,150,30))
        self.voltageInput.setPlaceholderText("Voltage (raise)")
        
        self.curentInput = QLineEdit(self.frameCycleInputs)
        self.curentInput.setGeometry(QRect(150,100,150,30))
        self.curentInput.setPlaceholderText("Current (raise)")
        
        self.timeInput = QLineEdit(self.frameCycleInputs)
        self.timeInput.setGeometry(QRect(150,150,150,30))
        self.timeInput.setPlaceholderText("Time (raise)")
        
        self.voltageInputLabel2 = QLabel("Voltage(V) dwell : ",self.frameCycleInputs)
        self.voltageInputLabel2.setGeometry(QRect(400,50,150,30))
        
        self.currentInputLabel2 = QLabel("Current(A) dwell : ",self.frameCycleInputs)
        self.currentInputLabel2.setGeometry(QRect(400,100,150,30))
        
        self.timeInputLabel2 = QLabel("Time(s) dwell : ",self.frameCycleInputs)
        self.timeInputLabel2.setGeometry(QRect(400,150,150,30)) 
        
        self.voltageInput2 = QLineEdit(self.frameCycleInputs)
        self.voltageInput2.setGeometry(QRect(500,50,150,30))
        self.voltageInput2.setPlaceholderText("Voltage (dwell)")
        
        self.curentInput2 = QLineEdit(self.frameCycleInputs)
        self.curentInput2.setGeometry(QRect(500,100,150,30))
        self.curentInput2.setPlaceholderText("Current (dwell)")
        
        self.timeInput2 = QLineEdit(self.frameCycleInputs)
        self.timeInput2.setGeometry(QRect(500,150,150,30))
        self.timeInput2.setPlaceholderText("Time (dwell)")
        
        self.set_paramsButton = QPushButton("SET PARAMETERS",self.frameCycleInputs)
        self.set_paramsButton.setGeometry(QRect(500,200, self.buttonWidth,self.buttonHeight))
        self.set_paramsButton.clicked.connect(self.set_parameters)
        
        #PARAMETERS SHOWN
        self.frameCycleLabels = QFrame(self)
        self.frameCycleLabels.setGeometry(QRect(50,650,675,200))
        self.frameCycleLabels.setStyleSheet("border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.voltageLabel = QLabel("0 volts (raise)",self.frameCycleLabels)
        self.voltageLabel.setGeometry(QRect(50,50,150,20))
        self.voltageLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.currentLabel = QLabel("0 ampers (raise)",self.frameCycleLabels)
        self.currentLabel.setGeometry(QRect(50,100,150,20))
        self.currentLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.timeLabel = QLabel("0 seconds (raise)",self.frameCycleLabels)
        self.timeLabel.setGeometry(QRect(50,150,150,20))
        self.timeLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.voltageLabel2 = QLabel("0 volts (dwell)",self.frameCycleLabels)
        self.voltageLabel2.setGeometry(QRect(200,50,150,20))
        self.voltageLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        self.currentLabel2 = QLabel("0 ampers (dwell)",self.frameCycleLabels)
        self.currentLabel2.setGeometry(QRect(200,100,150,20))
        self.currentLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        self.timeLabel2 = QLabel("0 seconds (dwell)",self.frameCycleLabels)
        self.timeLabel2.setGeometry(QRect(200,150,150,20))
        self.timeLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        
        #RUN BUTTON
        self.runButton = QPushButton("RUN",self.frameCycleLabels)
        self.runButton.setGeometry(QRect(450,50, 200,100))
        self.runButton.clicked.connect(self.run_cycle_thread)
        self.runButton.setFont(QFont("Arial", 20))
        
        
        
        #REFERANCES
        self.frameReferances = QFrame(self)
        self.frameReferances.setGeometry(QRect(self.width-350,self.height-300,500,500))
        
        self.referencesLabel = QLabel("<h1>REFERENCES</h1>",self.frameReferances)
        self.referencesLabel.setGeometry(QRect(100,50,150,50))
        
        
        self.raiseHeatFluxLabel = QLabel("Raise Heat Flux :",self.frameReferances)
        self.raiseHeatFluxLabel.setGeometry(QRect(50,100,150,30))
        
        self.raiseHeatFluxInput = QLineEdit(self.frameReferances)
        self.raiseHeatFluxInput.setGeometry(QRect(150,100,150,30))
        self.raiseHeatFluxInput.setText("245")
        
        self.raiseTimeLabel = QLabel("Raise Time :",self.frameReferances)
        self.raiseTimeLabel.setGeometry(QRect(50,150,150,30))
        
        self.raiseTimeInput = QLineEdit(self.frameReferances)
        self.raiseTimeInput.setGeometry(QRect(150,150,150,30))
        self.raiseTimeInput.setText("13")
        
        self.dwellHeatFluxLabel = QLabel("Dwell Heat Flux :",self.frameReferances)
        self.dwellHeatFluxLabel.setGeometry(QRect(50,200,150,30))
        
        self.dwellHeatFluxInput = QLineEdit(self.frameReferances)
        self.dwellHeatFluxInput.setGeometry(QRect(150,200,150,30))
        self.dwellHeatFluxInput.setText("92")
        
        self.dwellTimeLabel = QLabel("Dwell Time :",self.frameReferances)
        self.dwellTimeLabel.setGeometry(QRect(50,250,150,30))
        
        self.dwellTimeInput = QLineEdit(self.frameReferances)
        self.dwellTimeInput.setGeometry(QRect(150,250,150,30))
        self.dwellTimeInput.setText("60")
        
        #EMERGENCYSTOP BUTTON
        self.stopButton = QPushButton(f"EMERGENCY\nSTOP",self)
        self.stopButton.setGeometry(QRect(self.width - 650, 20, 250,100))
        self.stopButton.clicked.connect(self.stop_cycle)
        self.stopButton.setIcon(QIcon(QPixmap("iamges/stop.png")))
        self.stopButton.setIconSize(QtCore.QSize(100,100))
        self.stopButton.setFont(QFont("Arial", 15))
        self.stopButton.setStyleSheet("color: red")
        
        #MANUAL SECTION
        self.manualSectionFrame = QFrame(self)
        self.manualSectionFrame.setGeometry(QRect(self.width-650,300, 250,300))
        self.manualSectionFrame.setFont(QFont("Arial", 20))
        self.manualSectionFrame.setStyleSheet("border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.manualLabel = QLabel("OUTPUT PROGRAM ",self.manualSectionFrame)
        self.manualLabel.setGeometry(QRect(40,10,200,30))
        self.manualLabel.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.voltageSetLabel = QLabel("Voltage",self.manualSectionFrame)
        self.voltageSetLabel.setGeometry(QRect(20,75,100,50))
        self.voltageSetLabel.setStyleSheet("border-style: none;font-size:30px; color : #c2c2c2")
        
        self.voltageSpinBox = QSpinBox(self.manualSectionFrame)
        self.voltageSpinBox.setGeometry(QRect(150,75, 75,50))
        
        self.currentSetLabel = QLabel("Current",self.manualSectionFrame)
        self.currentSetLabel.setGeometry(QRect(20,150,100,50))
        self.currentSetLabel.setStyleSheet("border-style: none;font-size:30px; color : #c2c2c2")
        
        self.currentSpinBox = QSpinBox(self.manualSectionFrame)
        self.currentSpinBox.setGeometry(QRect(150,150, 75,50))
        
        
        #INFO LABEL
        self.infoLabel = QLabel("",self)
        self.infoLabel.setGeometry(QRect(self.width-650,130, 250,50))
        self.infoLabel.setFont(QFont("Arial", 12))
        
        
        #CONNECTION CHECK BUTTON
        self.check_connectionButton = QPushButton("CHECK CONNECTION",self)
        self.check_connectionButton.setGeometry(QRect(self.width-200 ,self.height-700, self.buttonWidth,self.buttonHeight))
        self.check_connectionButton.clicked.connect(self.check_connection)
        
        self.check_connectionLabel = QLabel("",self)
        self.check_connectionLabel.setGeometry(QRect(self.width-200,self.height-650, self.buttonWidth,self.buttonHeight))
        
        #MEASUREMENTS PANEL
        self.measurementFrame = QFrame(self)
        self.measurementFrame.setGeometry(QRect(self.width-300,300,350,200))
        self.measurementFrame.setStyleSheet("border-style: none;font-size:30px")
        
        self.measuredLabel = QLabel("MEASUREMENTS",self.measurementFrame)
        self.measuredLabel.setGeometry(QRect(0,0,150,50))
        self.measuredLabel.setStyleSheet("color:rgb(30, 146, 202); font-size:20px")
        
        self.measuredVoltageLabel = QLabel("0 Volt",self.measurementFrame)
        self.measuredVoltageLabel.setGeometry(QRect(0,50,350,50))
        
        self.measuredCurrentLabel = QLabel("0 Amper",self.measurementFrame)
        self.measuredCurrentLabel.setGeometry(QRect(0,100,350,50))
         
        self.measuredResistanceLabel = QLabel("0 ohm",self.measurementFrame)
        self.measuredResistanceLabel.setGeometry(QRect(0,150,350,50))
        
        #RESET GRAPH BUTTON
        self.resetGraphButton = QPushButton("RESET GRAPH",self)
        self.resetGraphButton.setGeometry(QRect(self.width - 200, self.height-300 , self.buttonWidth,self.buttonHeight))
        self.resetGraphButton.clicked.connect(self.reset_graph)
    
    def stop_cycle(self):
        
        self.voltage1 = 0
        self.current1 = 0
        self.voltage2 = 0
        self.current2 = 0
        try:
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
            SGX50X200D.write('*RST')     
            SGX50X200D.close()
            rm.close()
        except:
            print("Cycle couldn't stop in emergency")
       
        
    def check_connection(self):
        
        try: 
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            time.sleep(1)
            
            SGX50X200D.close()
            rm.close()
            self.check_connectionButton.setStyleSheet("background-color: green")
            self.check_connectionLabel.setText("<h2>CONNECTED</h2>")
            self.check_connectionLabel.setStyleSheet("color: green")
            
        except:
            self.check_connectionButton.setStyleSheet("background-color: red")
            self.check_connectionLabel.setText("<h2>NOT CONNECTED</h2>")
            self.check_connectionLabel.setStyleSheet("color: red")
            
    
        
    def graph(self):
        
        self.graphUpdateSpeed = 1000
        self.appGraph = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        self.win.setGeometry(QRect(self.width-450,50, 750,750))
        
        self.p1 = self.win.addPlot(colspan=2,title = "V,I,R-t")
        
        #self.p1.setTitle("Voltage", color="r", size="10pt")
        
        
        self.p1.setLabel('left', 'Voltage,Current,Resistance', units='V,A,ohm')
        self.p1.setLabel('bottom', 'Time', units='s')
        self.p1.showGrid(y= True, x = True, alpha = 1.)
        
        self.graphWidth = self.win.frameGeometry().width()
        self.graphHeight = self.win.frameGeometry().height()
        
        
        
        self.curve1 = self.p1.plot(self.voltageMeasurements,self.graphTime,name = "Voltage",pen=pg.mkPen('r',width=2))
        
        self.curve2 = self.p1.plot(self.currentMeasurements,self.graphTime,name= "Current",pen=pg.mkPen('g',width=2))
        self.curve3 = self.p1.plot(self.setVoltage1,name = "Voltage raise Set", pen=pg.mkPen('r',style=QtCore.Qt.DashLine,width = 0.5))
        self.curve4 = self.p1.plot(self.setCurrent1,name = "Current raise Set",pen=pg.mkPen('g',style=QtCore.Qt.DashLine,width = 0.5))
        self.curve5 = self.p1.plot(self.setVoltage2,name = "Voltage dwell Set",pen=pg.mkPen('r',style=QtCore.Qt.DotLine,width = 0.5))
        self.curve6 = self.p1.plot(self.setCurrent2,name = "Current dwell Set",pen=pg.mkPen('g',style=QtCore.Qt.DotLine,width = 0.5))
        self.curve7 = self.p1.plot(self.resistanceMeasurements,self.graphTime,name = "Resistance",pen=pg.mkPen('b',width=2))
        
        self.legend = self.p1.addLegend(offset=(self.graphWidth-250, self.graphHeight-(self.graphHeight-20)))
        
        
        self.legend.addItem(self.curve1, name=self.curve1.opts['name'])
        self.legend.addItem(self.curve2, name=self.curve2.opts['name'])
        self.legend.addItem(self.curve3, name=self.curve3.opts['name'])
        self.legend.addItem(self.curve4, name=self.curve4.opts['name'])
        self.legend.addItem(self.curve5, name=self.curve5.opts['name'])
        self.legend.addItem(self.curve6, name=self.curve6.opts['name'])
        self.legend.addItem(self.curve7, name=self.curve7.opts['name'])
        
        
    
    def reset_graph(self):
        try:
            
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
        
        except:
            print("Reset Graph Error")
        
        
    def calculate_resistance(self):
        try: 
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            time.sleep(1)
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (10))
            time.sleep(2)
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5))
            time.sleep(3)
            temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
            self.measured_voltage = temp_values[0]
            time.sleep(1)
            temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
            self.measured_current = temp_values[0]
            self.resistanceValue = self.measured_voltage / self.measured_current
            self.resistanceInput.setText(f"{self.resistanceValue}")
            time.sleep(0.5)
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
            SGX50X200D.write('*RST')     
            SGX50X200D.close()
            rm.close()
            print("Resistance calculatd")
            return "Resistance calculatd"
        except:
            print("Error in resistance calculation")
            return "Error in resistance calculation"
        
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
            self.raiseVoltage = math.ceil((self.raiseCurrent * self.resistance) + 10)
            self.voltageInput.setText(f"{self.raiseVoltage}")
            
            #time
            self.timeInput.setText(f"{self.raiseTimeRef}")  
            
            if self.raiseVoltage > 49 :
                self.raiseVoltage = 49
                self.voltageInput.setText(f"{self.raiseVoltage}")
                
                self.raiseCurrent = math.ceil((self.raiseVoltage - 10) / self.resistance)
                self.curentInput.setText(f"{self.raiseCurrent}")
                
                self.raisePower = self.raiseCurrent * self.raiseCurrent * self.resistance
                self.raiseFlux = self.raisePower / self.area / 1000
                
                
                self.raiseTime = math.ceil(self.raiseHeatFlux / self.raiseFlux * self.raiseTimeRef)
                self.timeInput.setText(f"{self.raiseTime}")
           
            
            #dwell calculations
            self.dwellPower = self.dwellHeatFlux * self.area
            
            #current
            self.dwellCurrent = math.ceil(math.sqrt(self.dwellPower * 1000/self.resistance))
            self.curentInput2.setText(f"{self.dwellCurrent}")
            
            #voltage
            self.dwellVoltage = math.ceil((self.dwellCurrent * self.resistance) + 10)
            self.voltageInput2.setText(f"{self.dwellVoltage}")
            
            #time
            self.timeInput2.setText(f"{self.dwellTimeRef}")
            
            if self.dwellVoltage > 49 :
                self.dwellVoltage = 49
                self.voltageInput2.setText(f"{self.dwellVoltage}")
                
                self.dwellCurrent = math.ceil((self.dwellVoltage  - 10) / self.resistance)
                self.curentInput2.setText(f"{self.dwellCurrent}")
                
                self.dwellPower = self.dwellCurrent * self.dwellCurrent * self.resistance
                self.dwellFlux = self.dwellPower / self.area / 1000
                
                print(self.dwellPower)
                print(self.dwellFlux)
                print(self.raiseHeatFlux)
                self.dwellTime = math.ceil(self.dwellHeatFlux / self.dwellFlux * self.dwellTimeRef)
                self.timeInput2.setText(f"{self.dwellTime}")
            self.missingDimension.setText("")
            print("Parameters calculated")
            return "Parameters calculated"
        except:
            
            self.missingDimension.setText("Missing Input !")
            print("Missing input in coupon properties")
            return "Missing input"
        
    def set_parameters(self):
        try:
            self.voltage1 = int(self.voltageInput.text())
            self.current1 = int(self.curentInput.text())
            self.cycleTime1 = int(self.timeInput.text())
            
            self.voltage2 = int(self.voltageInput2.text())
            self.current2 = int(self.curentInput2.text())
            self.cycleTime2 = int(self.timeInput2.text())
            
            self.voltageLabel.setText(f"{self.voltage1} volt (raise)")
            self.currentLabel.setText(f"{self.current1} amper (raise)")
            self.timeLabel.setText(f"{self.cycleTime1} seconds (raise)")
            
            self.voltageLabel2.setText(f"{self.voltage2} volt (dwell)")
            self.currentLabel2.setText(f"{self.current2} amper (dwell)")
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
            print("Parameters are set")
            return "Parameters are set"
        except:
            return "Missing input"
            print("Missing input")
            
    def run_cycle_thread(self):
        try:
            self.runThread = threading.Thread(target=self.runCycle)
            self.runThread.start()
            print("Thread Completed")
            return "Thread Completed"
        except:
            print("Thread Couldn' t Completed")
            return "Thread Couldn' t Completed"
        
    def runCycle(self):
        try:
            
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            time.sleep(0.3)
            self.runButton.setStyleSheet("background-color: green")
            self.runButton.setText(f"CYCLE\nRUNNING")
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage1))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current1))
            
            for i in range((5 * self.cycleTime1) + (5 * self.cycleTime2) + 30) :
                
                if i < 5 * self.cycleTime1:
                    self.stepName = "Raise step"
                else:
                    self.stepName = "Dwell Step"
                self.infoLabel.setStyleSheet("color: white")
                if (self.cycleTime1 + self.cycleTime2) - (i/5) > 0:
                    
                    self.infoLabel.setText(f"Cycle running...({self.stepName})\nRemaining time {round((self.cycleTime1 + self.cycleTime2) - (i/5),2)} seconds.. ")
                else:
                    self.infoLabel.setText(f"Cycle completed...\nRemaining time 0 seconds.. ")
                
                
                if i == (5* self.cycleTime1):
                    SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage2))
                    SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current2))
                    time.sleep(0.1)
                if i == ((5 * self.cycleTime1) + (5 * self.cycleTime2)):
                    SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
                    SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))
                    time.sleep(0.1)
                time.sleep(0.1)
                
                temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
                self.measured_voltage = temp_values[0]
                self.voltageMeasurements.append(self.measured_voltage)
                self.measuredVoltageLabel.setText(f"Voltage {round(self.measured_voltage,2)} V")
                
                time.sleep(0.1)
                
                temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
                self.measured_current = temp_values[0]
                self.currentMeasurements.append(self.measured_current)
                self.measuredCurrentLabel.setText(f"Current {round(self.measured_current,2)} A")
                
                self.graphTime.append(i/5)
                
                if self.measured_voltage > 0 and self.measured_current > 0:
                    
                    self.resistanceMeasurements.append(self.measured_voltage/self.measured_current)
                    self.curve7.setData(self.graphTime,self.resistanceMeasurements)
                    self.measuredResistanceLabel.setText(f"Resistance {round(self.measured_voltage/self.measured_current,2)} ohm")
        
                self.curve1.setData(self.graphTime,self.voltageMeasurements)
                self.curve2.setData(self.graphTime,self.currentMeasurements)
                
                
                self.appGraph.processEvents()
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
            SGX50X200D.write('*RST')     
            SGX50X200D.close()
            rm.close()
            print("Cycle Completed")
            self.runButton.setStyleSheet("background-color: rgb(77,77,77)")
            self.runButton.setText("RUN")
            return "CYCLE COMPLETED"
        except:
            self.runButton.setStyleSheet("color: white")
            self.runButton.setText("RUN")
            self.infoLabel.setText("Cycle stopped due to an error...")
            self.infoLabel.setStyleSheet("color: red")
            print("Cycle ERROR")
            return "Cycle Error"
def main():
    app = QApplication(sys.argv)
    file = open("Combinear.qss","r")
    with file:
        qss  = file.read()
        app.setStyleSheet(qss)
    window = MainPage(title = "Resistance Welding")
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main() 