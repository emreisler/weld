import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFrame, QLineEdit,QMainWindow,QSpinBox,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication,QLine
from PyQt5.QtGui import QPixmap,QIcon,QFont
import visa
import time
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore
import random
import threading
import math
from pymodbus.client.sync import ModbusTcpClient
import csv

"""
Notes:
    1-curve isimleri düzeltilecek
    2-label,button widgetları class ile oluşturulacak
    3-Graph renk patterni tekrar düzenlenecek
    4-qss ile bağlantı kopma sorunu düzeltilecek
    5-Sıcaklığa göre akım değerleri devamlı güncellenecek
    6-Cycle step sayısı seçmeli olacak
    7-Thermocouple sayısı sınırsız olacak.
    8-Sıcaklıklar main window a yazdırılacak
    9-Main window kapandığında fonksiyonlar devam ediyor(Datalogger termokupl değeri alma)
"""



class MainPage(QWidget):
    def __init__(self, title = ""):
        super().__init__() #inherit init of QWidget
        self.title = title
        self.left = 50
        self.top = 50
        self.width = 1400
        self.height = 950
        self.maxLen = 50
        
        self.voltageMeasurements = deque()
        self.currentMeasurements = deque()
        self.setVoltage1 = deque()
        self.setCurrent1 = deque()
        self.setVoltage2 = deque()
        self.setCurrent2 = deque()
        self.setVoltage3 = deque()
        self.setCurrent3 = deque()
        self.resistanceMeasurements = deque()
        self.graphTime = deque()
        self.tc1Values = deque()
        self.tc2Values = deque()
        self.tc3Values = deque()
        self.tc4Values = deque()
        self.tc5Values = deque()
        self.buttonWidth = 150
        self.buttonHeight = 40
        self.inputWidth = 150
        self.inputHeight = 30
        self.labelWidth = 150
        self.labelHeight = 30
        self.host = '192.168.1.30' # PLC IP
        self.port = 502 # PLC PORT
        

        self.graph()
        self.widget()

    def widget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.file = open("Combinear.qss","r")
        with self.file:
            self.qss  = self.file.read()
            self.setStyleSheet(self.qss)
        self.inputs()
        
        self.show()
        
    
    def inputs(self):
        
       
        self.logoLabel = QLabel(self) 
         
        # loading image 
        self.pixmap = QPixmap('images/logo.svg') 
  
        # adding image to label 
        self.logoLabel.setPixmap(self.pixmap) 
  
        # Optional, resize label to image size 
        self.logoLabel.move(self.size().width()-350,20)
    
        self.frameAreaInputs = QFrame(self)
        self.frameAreaInputs.setGeometry(QRect(50,20,675,250))
        self.frameAreaInputs.setStyleSheet("border-width: 1; font-size : 15px;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.areaInputsLabel = QLabel("MESH PARAMETERS",self.frameAreaInputs)
        self.areaInputsLabel.setGeometry(QRect(250,10,200,30))
        self.areaInputsLabel.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.resistanceInputLabel = QLabel("Resistance(ohm) : ",self.frameAreaInputs)
        self.resistanceInputLabel.setGeometry(QRect(50,50,150,50))
        
        self.lengthInputLabel = QLabel("Length(mm) : ",self.frameAreaInputs)
        self.lengthInputLabel.setGeometry(QRect(50,100,150,50))
        
        self.widthInputLabel = QLabel("Width(mm) : ",self.frameAreaInputs)
        self.widthInputLabel.setGeometry(QRect(50,150,150,50))
        
        self.resistanceInput = QLineEdit(self.frameAreaInputs)
        self.resistanceInput.setGeometry(QRect(200,50,150,50))
        self.resistanceInput.setPlaceholderText("Resistance(ohm)")
        
        self.lengthInput = QLineEdit(self.frameAreaInputs)
        self.lengthInput.setGeometry(QRect(200,100,150,50))
        self.lengthInput.setPlaceholderText("Length of bond line")
        
        self.widthInput = QLineEdit(self.frameAreaInputs)
        self.widthInput.setGeometry(QRect(200,150,150,50))
        self.widthInput.setPlaceholderText("Width of bond line")
        
        
        
        self.calculateResistanceButton = QPushButton("CALCULATE RESISTANCE",self.frameAreaInputs)
        self.calculateResistanceButton.setGeometry(QRect(450,50, self.buttonWidth+50, self.buttonHeight))
        self.calculateResistanceButton.clicked.connect(self.calculate_resistance)
        
        self.calculateParameterseButton = QPushButton("CALCULATE PARAMETERS",self.frameAreaInputs)
        self.calculateParameterseButton.setGeometry(QRect(450,100, self.buttonWidth+50,self.buttonHeight))
        self.calculateParameterseButton.clicked.connect(self.calculate_parameters)
        
        self.missingDimension = QLabel("",self.frameAreaInputs)
        self.missingDimension.setGeometry(QRect(350,150,150,30))
        self.missingDimension.setStyleSheet("border-style: none;color: red")
        
        
        #CYCLE PARAMETER INPUTS
        self.frameCycleInputs = QFrame(self)
        self.frameCycleInputs.setGeometry(QRect(50,300,675,300))
        self.frameCycleInputs.setStyleSheet("border-width: 1;border-radius: 3;font-size : 15px; border-style: solid;border-color: rgb(100,100,100)")
        
        self.cyleInputLabel = QLabel("CYCLE PARAMETERS ",self.frameCycleInputs)
        self.cyleInputLabel.setGeometry(QRect(250,10,200,30))
        self.cyleInputLabel.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.voltageInputLabel = QLabel("Voltage(V) raise : ",self.frameCycleInputs)
        self.voltageInputLabel.setGeometry(QRect(50,50,150,50))
        
        self.currentInputLabel = QLabel("Current(A) raise : ",self.frameCycleInputs)
        self.currentInputLabel.setGeometry(QRect(50,100,150,50))
        
        self.timeInputLabel = QLabel("Time(s) raise : ",self.frameCycleInputs)
        self.timeInputLabel.setGeometry(QRect(50,150,150,50)) 
        
        self.voltageInput = QLineEdit(self.frameCycleInputs)
        self.voltageInput.setGeometry(QRect(200,50,50,50))
        self.voltageInput.setText("50")
        
        self.curentInput = QLineEdit(self.frameCycleInputs)
        self.curentInput.setGeometry(QRect(200,100,50,50))
        self.curentInput.setPlaceholderText("0")
        
        self.timeInput = QLineEdit(self.frameCycleInputs)
        self.timeInput.setGeometry(QRect(200,150,50,50))
        self.timeInput.setPlaceholderText("0")
        
        self.voltageInputLabel2 = QLabel("Voltage(V) 1st dwell : ",self.frameCycleInputs)
        self.voltageInputLabel2.setGeometry(QRect(250,50,150,50))
        
        self.currentInputLabel2 = QLabel("Current(A) 1st dwell : ",self.frameCycleInputs)
        self.currentInputLabel2.setGeometry(QRect(250,100,150,50))
        
        self.timeInputLabel2 = QLabel("Time(s) 1st dwell : ",self.frameCycleInputs)
        self.timeInputLabel2.setGeometry(QRect(250,150,150,50)) 
        
        self.voltageInput2 = QLineEdit(self.frameCycleInputs)
        self.voltageInput2.setGeometry(QRect(400,50,50,50))
        self.voltageInput2.setText("50")
        
        self.curentInput2 = QLineEdit(self.frameCycleInputs)
        self.curentInput2.setGeometry(QRect(400,100,50,50))
        self.curentInput2.setPlaceholderText("0")
        
        self.timeInput2 = QLineEdit(self.frameCycleInputs)
        self.timeInput2.setGeometry(QRect(400,150,50,50))
        self.timeInput2.setPlaceholderText("0")
        
        self.voltageInputLabel3 = QLabel("Voltage(V) 2nd dwell : ",self.frameCycleInputs)
        self.voltageInputLabel3.setGeometry(QRect(450,50,150,50))
        
        self.currentInputLabel3 = QLabel("Current(A) 2nd dwell : ",self.frameCycleInputs)
        self.currentInputLabel3.setGeometry(QRect(450,100,150,50))
        
        self.timeInputLabel3 = QLabel("Time(s) 2nd dwell : ",self.frameCycleInputs)
        self.timeInputLabel3.setGeometry(QRect(450,150,150,50)) 
        
        self.voltageInput3 = QLineEdit(self.frameCycleInputs)
        self.voltageInput3.setGeometry(QRect(600,50,50,50))
        self.voltageInput3.setText("50")
        
        self.curentInput3 = QLineEdit(self.frameCycleInputs)
        self.curentInput3.setGeometry(QRect(600,100,50,50))
        self.curentInput3.setPlaceholderText("0")
        
        self.timeInput3 = QLineEdit(self.frameCycleInputs)
        self.timeInput3.setGeometry(QRect(600,150,50,50))
        self.timeInput3.setPlaceholderText("0")
        
        self.set_paramsButton = QPushButton("SET PARAMETERS",self.frameCycleInputs)
        self.set_paramsButton.setGeometry(QRect(500,250, self.buttonWidth,self.buttonHeight))
        self.set_paramsButton.clicked.connect(self.set_parameters)
        
        #PARAMETERS SHOWN
        self.frameCycleLabels = QFrame(self)
        self.frameCycleLabels.setGeometry(QRect(50,650,675,250))
        self.frameCycleLabels.setStyleSheet("border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.step1Label = QLabel("STEP-1",self.frameCycleLabels)
        self.step1Label.setGeometry(QRect(50,10,200,30))
        self.step1Label.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.step2Label = QLabel("STEP-2",self.frameCycleLabels)
        self.step2Label.setGeometry(QRect(200,10,200,30))
        self.step2Label.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.step3Label = QLabel("STEP-3",self.frameCycleLabels)
        self.step3Label.setGeometry(QRect(350,10,200,30))
        self.step3Label.setStyleSheet("border-style: none;color : rgb(30, 146, 202); font-size : 20px")
        
        self.voltageLabel = QLabel("0 V (raise)",self.frameCycleLabels)
        self.voltageLabel.setGeometry(QRect(50,50,150,20))
        self.voltageLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.currentLabel = QLabel("0 A (raise)",self.frameCycleLabels)
        self.currentLabel.setGeometry(QRect(50,100,150,20))
        self.currentLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.timeLabel = QLabel("0 s (raise)",self.frameCycleLabels)
        self.timeLabel.setGeometry(QRect(50,150,150,20))
        self.timeLabel.setStyleSheet("border-style: none;font-size:15px")
        
        self.voltageLabel2 = QLabel("0 V (1st dwell)",self.frameCycleLabels)
        self.voltageLabel2.setGeometry(QRect(200,50,150,20))
        self.voltageLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        self.currentLabel2 = QLabel("0 A (1st dwell)",self.frameCycleLabels)
        self.currentLabel2.setGeometry(QRect(200,100,150,20))
        self.currentLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        self.timeLabel2 = QLabel("0 s (1st dwell)",self.frameCycleLabels)
        self.timeLabel2.setGeometry(QRect(200,150,150,20))
        self.timeLabel2.setStyleSheet("border-style: none;font-size:15px")
        
        self.voltageLabel3 = QLabel("0 V (2nd dwell)",self.frameCycleLabels)
        self.voltageLabel3.setGeometry(QRect(350,50,150,20))
        self.voltageLabel3.setStyleSheet("border-style: none;font-size:15px")
        
        self.currentLabel3 = QLabel("0 A 2nd dwell)",self.frameCycleLabels)
        self.currentLabel3.setGeometry(QRect(350,100,150,20))
        self.currentLabel3.setStyleSheet("border-style: none;font-size:15px")
        
        self.timeLabel3 = QLabel("0 s (2nd dwell)",self.frameCycleLabels)
        self.timeLabel3.setGeometry(QRect(350,150,150,20))
        self.timeLabel3.setStyleSheet("border-style: none;font-size:15px")
        
        
        #RUN BUTTON
        self.runButton = QPushButton("RUN",self.frameCycleLabels)
        self.runButton.setGeometry(QRect(510,50, 150,120))
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
        self.voltageSpinBox.valueChanged.connect(self.manual_voltage_thread)
        
        self.currentSetLabel = QLabel("Current",self.manualSectionFrame)
        self.currentSetLabel.setGeometry(QRect(20,150,100,50))
        self.currentSetLabel.setStyleSheet("border-style: none;font-size:30px; color : #c2c2c2")
        
        self.currentSpinBox = QSpinBox(self.manualSectionFrame)
        self.currentSpinBox.setGeometry(QRect(150,150, 75,50))
        self.currentSpinBox.valueChanged.connect(self.manual_current_thread)
        
        #TC VALUES
        self.tcMeasurementsFrame = QFrame(self)
        self.tcMeasurementsFrame.setGeometry(QRect(self.width-650,650, 300,250))
        self.tcMeasurementsFrame.setStyleSheet("font-size:15px; color : #c2c2c2;border-width: 1;border-radius: 3;border-style: solid;border-color: rgb(100,100,100)")
        
        self.tc1Label = QLabel("TC1 ",self.tcMeasurementsFrame)
        self.tc1Label.setGeometry(QRect(20,0,200,30))
        self.tc1Label.setStyleSheet("border-style: none")
        
        self.tc2Label = QLabel("TC2 ",self.tcMeasurementsFrame)
        self.tc2Label.setGeometry(QRect(20,40,200,30))
        self.tc2Label.setStyleSheet("border-style: none")
        
        self.tc3Label = QLabel("TC3 ",self.tcMeasurementsFrame)
        self.tc3Label.setGeometry(QRect(20,80,200,30))
        self.tc3Label.setStyleSheet("border-style: none")
        
        self.tc4Label = QLabel("TC4 ",self.tcMeasurementsFrame)
        self.tc4Label.setGeometry(QRect(20,120,200,30))
        self.tc4Label.setStyleSheet("border-style: none")
        
        self.tc5Label = QLabel("TC5 ",self.tcMeasurementsFrame)
        self.tc5Label.setGeometry(QRect(20,160,200,30))
        self.tc5Label.setStyleSheet("border-style: none")
        
        self.tcInfoButton = QPushButton("TEMPERATURES",self.tcMeasurementsFrame)
        self.tcInfoButton.setGeometry(QRect(20 ,200, self.buttonWidth,self.buttonHeight))
        self.tcInfoButton.setStyleSheet("font-size:15px; color :white")
        self.tcInfoButton.clicked.connect(self.get_temperatures_thread)
        
        self.stopTcMeasurement = QPushButton("STOP",self.tcMeasurementsFrame)
        self.stopTcMeasurement.setGeometry(QRect(200 ,200, self.buttonWidth-100,self.buttonHeight))
        self.stopTcMeasurement.setStyleSheet("font-size:15px; color :white")
        self.stopTcMeasurement.clicked.connect(self.stop_tc_measurement)
        
        #INFO LABEL
        self.infoLabel = QLabel("",self)
        self.infoLabel.setGeometry(QRect(self.width-650,130, 250,50))
        self.infoLabel.setFont(QFont("Arial", 12))
        
        
        #CONNECTION CHECK BUTTON
        self.check_connectionButton = QPushButton("CHECK CONNECTION",self)
        self.check_connectionButton.setGeometry(QRect(self.width-200 ,self.height-750, self.buttonWidth,self.buttonHeight))
        self.check_connectionButton.clicked.connect(self.check_connection)
        
        self.check_connectionLabel = QLabel("",self)
        self.check_connectionLabel.setGeometry(QRect(self.width-200,self.height-650, self.buttonWidth,self.buttonHeight))
        
        #MEASUREMENTS PANEL
        self.measurementFrame = QFrame(self)
        self.measurementFrame.setGeometry(QRect(self.width-250,300,350,200))
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
        
    def get_temperatures_thread(self):
        try:
            self.getTemperaturesThread = threading.Thread(target=self.get_temperatures)
            self.getTemperaturesThread.start()
            
            print("Thread Completed")
            return "Thread Completed"
        except:
            print("Thread Couldn' t Completed")
            return "Thread Couldn' t Completed"
        
    def get_temperatures(self):
        self.measureTemperature = True
        """
        self.client = ModbusTcpClient(self.host, self.port)
        self.client.connect()
        """
        while self.measureTemperature:
            try:
                
                self.tcValues = self.client.read_holding_registers(40,5,unit=0)
                assert(self.tcValues.function_code < 0x80)     # test that we are not an error
                
                self.tc1Label.setText(f"TC1 {self.tcValues.registers[0]/10} C°")
                self.tc2Label.setText(f"TC2 {self.tcValues.registers[1]/10} C°")
                self.tc3Label.setText(f"TC3 {self.tcValues.registers[2]/10} C°")
                self.tc4Label.setText(f"TC4 {self.tcValues.registers[3]/10} C°")
                self.tc5Label.setText(f"TC5 {self.tcValues.registers[4]/10} C°")
                time.sleep(0.5)
                print("Connected to DataLogger and temperatures are written on mainwindow")
            except:
                print("DataLogger connection error")
                return "Couldn't get temperatures from data logger"
        print("Thermocouple measurements has stopped")
        return "Thermocouple measurements has stopped"
            
    def stop_tc_measurement(self):
        self.measureTemperature = False
        return "Temperature reading is stopped"
        
    def stop_cycle(self):
    
        self.voltage1 = 0
        self.current1 = 0
        self.voltage2 = 0
        self.current2 = 0
        self.voltage3 = 0
        self.current3 = 0
        
    
        try:
            
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write('*RST')     
            SGX50X200D.close()
            rm.close()
            
            self.cycleContinue = False
            self.voltageLabel.setText("0 V (raise)")
            self.currentLabel.setText("0 A (raise)")
            self.timeLabel.setText("0 s (raise)")
            
            self.voltageLabel2.setText("0 V (1st dwell)")
            self.currentLabel2.setText("0 A (1st dwell)")
            self.timeLabel2.setText("0 s (1st dwell)")
            
            self.voltageLabel3.setText("0 V (2nd dwell)")
            self.currentLabel3.setText("0 A (2nd dwell)")
            self.timeLabel3.setText("0 s (2nd dwell)")
            print("Cycle stopped im emergency")
            return "Cycle stopped im emergency"
        except:
            print("Cycle couldn't stop in emergency")
            return "Cycle couldn't stop in emergency"
            
       
        
    def check_connection(self):
        
        try: 
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            time.sleep(0.5)
            SGX50X200D.close()
            rm.close()
            
            self.check_connectionButton.setStyleSheet("background-color: green")
            self.check_connectionButton.setText("CONNECTED")
            
        except:
            self.check_connectionButton.setStyleSheet("background-color: red")
            self.check_connectionButton.setText("NOT CONNECTED")
        
    def graph(self):
        
        self.appGraph = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Cycle Graph")
        self.win.setGeometry(QRect(50,50, 750,750))
        self.win.showMaximized()
        self.p1 = self.win.addPlot(colspan=2,title = "V,I,R-t")
        
        self.p1.setLabel('left', 'Voltage,Current,Resistance', units='V,A,ohm')
        self.p1.setLabel('bottom', 'Time', units='s')
        self.p1.showGrid(y= True, x = True, alpha = 1.)
        
        self.graphWidth = self.win.frameGeometry().width()
        self.graphHeight = self.win.frameGeometry().height()
        
        
        #Power Supply
        self.curve1 = self.p1.plot(self.voltageMeasurements,self.graphTime,name = "Voltage",pen=pg.mkPen('r',width=2))
        self.curve2 = self.p1.plot(self.currentMeasurements,self.graphTime,name= "Current",pen=pg.mkPen('g',width=2))
        self.curve3 = self.p1.plot(self.setVoltage1,name = "Voltage raise Set", pen=pg.mkPen('r',style=QtCore.Qt.DashLine,width = 0.5))
        self.curve4 = self.p1.plot(self.setCurrent1,name = "Current raise Set",pen=pg.mkPen('g',style=QtCore.Qt.DashLine,width = 0.5))
        self.curve5 = self.p1.plot(self.setVoltage2,name = "Voltage 1st dwell Set",pen=pg.mkPen('r',style=QtCore.Qt.DotLine,width = 0.5))
        self.curve6 = self.p1.plot(self.setCurrent2,name = "Current 1st dwell Set",pen=pg.mkPen('g',style=QtCore.Qt.DotLine,width = 0.5))
        self.curve13 = self.p1.plot(self.setVoltage3,name = "Voltage 2nd dwell Set",pen=pg.mkPen('r',style=QtCore.Qt.DotLine,width = 1))
        self.curve14 = self.p1.plot(self.setCurrent3,name = "Current 2nd dwell Set",pen=pg.mkPen('g',style=QtCore.Qt.DotLine,width = 1))
        self.curve7 = self.p1.plot(self.resistanceMeasurements,self.graphTime,name = "Resistance",pen=pg.mkPen('b',width=2))
        
        #DataLogger
        self.curve8 = self.p1.plot(self.tc1Values,self.graphTime,name = "TC1",pen=pg.mkPen('c',width=2))
        self.curve9 = self.p1.plot(self.tc2Values,self.graphTime,name = "TC2",pen=pg.mkPen('m',width=2))
        self.curve10 = self.p1.plot(self.tc3Values,self.graphTime,name = "TC3",pen=pg.mkPen('y',width=2))
        self.curve11 = self.p1.plot(self.tc4Values,self.graphTime,name = "TC4",pen=pg.mkPen('r',width=2))
        self.curve12 = self.p1.plot(self.tc5Values,self.graphTime,name = "TC5",pen=pg.mkPen('w',width=2))
        
        #AddLegend
        self.legend = self.p1.addLegend(offset=(1600, 20))
        
        self.legend.addItem(self.curve1, name=self.curve1.opts['name'])
        self.legend.addItem(self.curve2, name=self.curve2.opts['name'])
        self.legend.addItem(self.curve3, name=self.curve3.opts['name'])
        self.legend.addItem(self.curve4, name=self.curve4.opts['name'])
        self.legend.addItem(self.curve5, name=self.curve5.opts['name'])
        self.legend.addItem(self.curve6, name=self.curve6.opts['name'])
        self.legend.addItem(self.curve7, name=self.curve7.opts['name'])
        self.legend.addItem(self.curve8, name=self.curve8.opts['name'])
        self.legend.addItem(self.curve9, name=self.curve9.opts['name'])
        self.legend.addItem(self.curve10, name=self.curve10.opts['name'])
        self.legend.addItem(self.curve11, name=self.curve11.opts['name'])
        self.legend.addItem(self.curve12, name=self.curve12.opts['name'])
        self.legend.addItem(self.curve13, name=self.curve13.opts['name'])
        self.legend.addItem(self.curve14, name=self.curve14.opts['name'])
    
    def reset_graph(self):
        try:
            self.voltageMeasurements.clear()
            self.currentMeasurements.clear()
            self.setVoltage1.clear()
            self.setCurrent1.clear()
            self.setVoltage2.clear()
            self.setCurrent2.clear()
            self.setVoltage3.clear()
            self.setCurrent3.clear()
            self.resistanceMeasurements.clear()
            self.graphTime.clear()
            self.tc1Values.clear()
            self.tc2Values.clear()
            self.tc3Values.clear()
            self.tc4Values.clear()
            self.tc5Values.clear()
            self.curve1.clear()
            self.curve2.clear()
            self.curve3.clear()
            self.curve4.clear()
            self.curve5.clear()
            self.curve6.clear()
            self.curve7.clear()
            self.curve8.clear()
            self.curve9.clear()
            self.curve10.clear()
            self.curve11.clear()
            self.curve12.clear()
            self.curve13.clear()
            self.curve14.clear()
            self.voltageLabel.setText("0 V (raise)")
            self.currentLabel.setText("0 A (raise)")
            self.timeLabel.setText("0 s (raise)")
            
            self.voltageLabel2.setText("0 V (1st dwell)")
            self.currentLabel2.setText("0 A (1st dwell)")
            self.timeLabel2.setText("0 s (1st dwell)")
            
            self.voltageLabel3.setText("0 V (2nd dwell)")
            self.currentLabel3.setText("0 A (2nd dwell)")
            self.timeLabel3.setText("0 s (2nd dwell)")
            print("Graph is reset")
            return "Graph is reset"
        except:
            print("Reset Graph Error")
            return "Reset Graph Error"
        
    def calculate_resistance(self):
        try: 
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            time.sleep(1)
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (5))
            time.sleep(2)
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (10))
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
    def manual_voltage_thread(self):
        try:
            self.manualVoltageThread = threading.Thread(target=self.manual_voltage)
            self.manualVoltageThread.start()
            print("Thread Completed")
            return "Thread Completed"
        except:
            print("Thread Couldn' t Completed")
            return "Thread Couldn' t Completed"
        
        
    def manual_voltage(self):
        try:
           self.manualVoltage = int(self.voltageSpinBox.text()) 
           
           rm = visa.ResourceManager()
           SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
           SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.manualVoltage))
           
           print("Manual Voltage set")
           return "Manual Voltage set"
        except:
            print("Manual Voltage Couldn' t be set")
            return "Manual Voltage Couldn' t be set"
        
    def manual_current_thread(self):
        try:
            self.manualCurrentThread = threading.Thread(target=self.manual_current)
            self.manualCurrentThread.start()
            print("Thread Completed")
            return "Thread Completed"
        except:
            print("Thread Couldn' t Completed")
            return "Thread Couldn' t Completed"
        
        
    def manual_current(self):
        try:
           self.manualVoltage = int(self.voltageSpinBox.text()) 
           
           rm = visa.ResourceManager()
           SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
           SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.manualVoltage))
           
           print("Manual Current set")
           return "Manual Current set"
        except:
            print("Manual Current Couldn' t be set")
            return "Manual Current Couldn' t be set"
        
    def set_parameters(self):
        try:
            self.voltage1 = int(self.voltageInput.text())
            self.current1 = int(self.curentInput.text())
            self.cycleTime1 = int(self.timeInput.text())
            
            self.voltage2 = int(self.voltageInput2.text())
            self.current2 = int(self.curentInput2.text())
            self.cycleTime2 = int(self.timeInput2.text())
            
            self.voltage3 = int(self.voltageInput3.text())
            self.current3 = int(self.curentInput3.text())
            self.cycleTime3 = int(self.timeInput3.text())
            
            self.voltageLabel.setText(f"{self.voltage1} V (raise)")
            self.currentLabel.setText(f"{self.current1} A (raise)")
            self.timeLabel.setText(f"{self.cycleTime1} s (raise)")
            
            self.voltageLabel2.setText(f"{self.voltage2} V (1st dwell)")
            self.currentLabel2.setText(f"{self.current2} A (1st dwell)")
            self.timeLabel2.setText(f"{self.cycleTime2} s (1st dwell)")
            
            self.voltageLabel3.setText(f"{self.voltage3} V (2nd dwell)")
            self.currentLabel3.setText(f"{self.current3} A (2nd dwell)")
            self.timeLabel3.setText(f"{self.cycleTime3} s (2nd dwell)")
            
            for i in range(200):
                self.setVoltage1.append(self.voltage1)
                self.setCurrent1.append(self.current1)
                self.setVoltage2.append(self.voltage2)
                self.setCurrent2.append(self.current2)
                self.setVoltage3.append(self.voltage3)
                self.setCurrent3.append(self.current3)
                
            self.curve3.setData(self.setVoltage1)
            self.curve4.setData(self.setCurrent1)
            self.curve5.setData(self.setVoltage2)
            self.curve6.setData(self.setCurrent2)
            self.curve13.setData(self.setVoltage1)
            self.curve14.setData(self.setCurrent1)
            
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
            
            try:
                
                self.client = ModbusTcpClient(self.host, self.port)
                self.client.connect()
                print("Connected to DataLogger")
            except:
                print("DataLogger connection error")
                pass
            try:
                rm = visa.ResourceManager()
                SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            except:
                print("Power Supply connection error")
                pass
            
            time.sleep(0.3)
            self.runButton.setStyleSheet("background-color: green; color:white")
            self.runButton.setText(f"CYCLE\nRUNNING")
            self.runButton.setEnabled(False)
            
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.current1))
            
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.voltage1))
            
            
            
            self.cycleContinue = True
            
            for i in range((2 * self.cycleTime1) + (2 * self.cycleTime2) + (2*self.cycleTime3) + 30):
                if self.cycleContinue == True:
                    print(self.cycleContinue)
                    print(i)
                    if i < 2 * self.cycleTime1:
                        self.stepName = "1st Step (raise)"
                    elif 2 * self.cycleTime1 < i < 2 * self.cycleTime2:
                        self.stepName = "2nd Step (dwell at melting)"
                    else:
                        self.stepName = "3rd step (dwell at rystallization)"
                        
                    self.infoLabel.setStyleSheet("color: white")
                    
                    if (self.cycleTime1 + self.cycleTime2 + self.cycleTime3) - (i/2) > 0:
                        
                        self.infoLabel.setText(f"Cycle running...({self.stepName})\nRemaining time {round((self.cycleTime1 + self.cycleTime2 + self.cycleTime3) - (i/2),2)} seconds.. ")
                    else:
                        self.infoLabel.setText(f"Cycle completed...\nRemaining time 0 seconds.. ")
                    
                    
                    if i == (2 * self.cycleTime1):
                        
                        SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.voltage2))
                        SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.current2))
                        
                        
                    if i == ((2 * self.cycleTime1) + (2 * self.cycleTime2)):
                        
                        SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.voltage3))
                        SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.current3))
                        
                    if i == ((2 * self.cycleTime1) + (2 * self.cycleTime2) + (2 * self.cycleTime3)):
                        SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))
                        SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
                        
                        
                    time.sleep(0.25)
                    try:
                        
                        temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
                        self.measured_voltage = temp_values[0]
                        
                        self.voltageMeasurements.append(self.measured_voltage)
                        self.measuredVoltageLabel.setText(f"Voltage {round(self.measured_voltage,2)} V")
                    except:
                        print("Voltage couldn' t measured")
                        
                    time.sleep(0.25)
                    try:
                        
                        temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
                        self.measured_current = temp_values[0]
                        
                        self.currentMeasurements.append(self.measured_current)
                        self.measuredCurrentLabel.setText(f"Current {round(self.measured_current,2)} A")
                    except:
                        print("Current couldn' t measured")
                        pass
                    
                    self.graphTime.append(i/2)
                    
                    try:
                        self.resistanceMeasurements.append(self.measured_voltage/self.measured_current)
                        self.curve7.setData(self.graphTime,self.resistanceMeasurements)
                        self.measuredResistanceLabel.setText(f"Resistance {round(self.measured_voltage/self.measured_current,2)} ohm")
                    except:
                        print("Resistance couldn't calculated")
                    
                    try:
                    
                        self.tcValues = self.client.read_holding_registers(40,5,unit=0)
                        assert(self.tcValues.function_code < 0x80)     # test that we are not an error
                        
                        self.tc1Values.append(self.tcValues.registers[0]/10)
                        self.tc2Values.append(self.tcValues.registers[1]/10)
                        self.tc3Values.append(self.tcValues.registers[2]/10)
                        self.tc4Values.append(self.tcValues.registers[3]/10)
                        self.tc5Values.append(self.tcValues.registers[4]/10)
                        
                        self.curve8.setData(self.graphTime,self.tc1Values)
                        self.curve9.setData(self.graphTime,self.tc2Values)
                        self.curve10.setData(self.graphTime,self.tc3Values)
                        self.curve11.setData(self.graphTime,self.tc4Values)
                        self.curve12.setData(self.graphTime,self.tc5Values)
                        
                    except:
                        print("Datalogger data reading error")
                    self.curve1.setData(self.graphTime,self.voltageMeasurements)
                    self.curve2.setData(self.graphTime,self.currentMeasurements)
                    
                    
                    self.appGraph.processEvents()
            
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))  
            SGX50X200D.write('*RST')     
            SGX50X200D.close()
            rm.close()
            
            self.runButton.setStyleSheet("background-color: rgb(77,77,77); :hover : background-color: rgba(183, 134, 32, 20%);border: 1px solid #b78620;")
            self.runButton.setText("RUN")
            self.voltageMeasurements.clear()
            self.currentMeasurements.clear()
            self.setVoltage1.clear()
            self.setCurrent1.clear()
            self.setVoltage2.clear()
            self.setCurrent2.clear()
            self.setVoltage3.clear()
            self.setCurrent3.clear()
            self.resistanceMeasurements.clear()
            self.graphTime.clear()
            self.tc1Values.clear()
            self.tc2Values.clear()
            self.tc3Values.clear()
            self.tc4Values.clear()
            self.tc5Values.clear()
            self.runButton.setEnabled(True)
            print("Cycle Completed")
            return "CYCLE COMPLETED"
        except:
            self.runButton.setStyleSheet("color: white")
            self.runButton.setText("RUN")
            self.infoLabel.setText("Cycle stopped due to an error...")
            self.infoLabel.setStyleSheet("color: red")
            self.runButton.setEnabled(True)
            print("Cycle ERROR")
            return "Cycle Error"
        
    def closeEvent(self,event):
        self.reply = QMessageBox.question(self,"Window Close","Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            self.cycleContinue = False
            self.measureTemperature = False
            self.win.close()
            sys.exit()
            event.accept()
        else:
            event.ignore()
        
def main():
    app = QApplication(sys.argv)
    window = MainPage(title = "Resistance Welding")
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main() 
