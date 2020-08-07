import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFrame, QLineEdit
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication
import visa
import time



class MainPage(QWidget):
    def __init__(self, title = ""):
        super().__init__() #inherit init of QWidget
        self.title = title
        self.left = 200
        self.top = 200
        self.width = 1400
        self.height = 800
        self.widget()
    
    def widget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        
        #frame 1.step 
        self.frameInput1 = QFrame(self)
        self.frameInput1.setGeometry(QRect(40, 40, 400, 400))
        self.frameInput1.setFont(QtGui.QFont("Times",10, QtGui.QFont.Bold))
        #Tags
        self.labelVoltage1 = QLabel("Voltage(raise) :", self.frameInput1)
        self.labelVoltage1.setGeometry(QRect(0,0,150,30))
        
        
        self.labelCurrent1 = QLabel("Current(raise) :", self.frameInput1)
        self.labelCurrent1.setGeometry(QRect(0,50,150,30))
        
        
        self.labelTime1 = QLabel("Time(raise) :", self.frameInput1)
        self.labelTime1.setGeometry(QRect(0,100,150,30))
        
        
        
        #inputBoxes
        self.inputVoltage1 = QLineEdit("", self.frameInput1)
        self.inputVoltage1.setPlaceholderText("Voltage (Volt)")
        self.inputVoltage1.setGeometry(QRect(120,0,150,30))
        
        self.inputCurrent1 = QLineEdit("", self.frameInput1)
        self.inputCurrent1.setPlaceholderText("Current(ohm)")
        self.inputCurrent1.setGeometry(QRect(120,50,150,30))
        
        self.inputTime1 = QLineEdit("", self.frameInput1)
        self.inputTime1.setPlaceholderText("Time(second)")
        self.inputTime1.setGeometry(QRect(120,100,150,30))
        
        #frame 2.step 
        self.frameInput2 = QFrame(self)
        self.frameInput2.setGeometry(QRect(40, 220, 400, 400))
        self.frameInput2.setFont(QtGui.QFont("Times",10, QtGui.QFont.Bold))
        
        #Tags
        self.labelVoltage2 = QLabel("Voltage(dwell) :", self.frameInput2)
        self.labelVoltage2.setGeometry(QRect(0,0,150,30))
        
        
        self.labelCurrent2 = QLabel("Current(dwell) :", self.frameInput2)
        self.labelCurrent2.setGeometry(QRect(0,50,150,30))
        
        
        self.labelTime2 = QLabel("Time(dwell) :", self.frameInput2)
        self.labelTime2.setGeometry(QRect(0,100,150,30))
        
        
        
        #inputBoxes
        self.inputVoltage2 = QLineEdit("", self.frameInput2)
        self.inputVoltage2.setPlaceholderText("Voltage (Volt)")
        self.inputVoltage2.setGeometry(QRect(120,0,150,30))
        
        self.inputCurrent2 = QLineEdit("", self.frameInput2)
        self.inputCurrent2.setPlaceholderText("Current(ohm)")
        self.inputCurrent2.setGeometry(QRect(120,50,150,30))
        
        self.inputTime2 = QLineEdit("", self.frameInput2)
        self.inputTime2.setPlaceholderText("Time(second)")
        self.inputTime2.setGeometry(QRect(120,100,150,30))

        #Parameters frame
        self.paramsFrame = QFrame(self) 
        self.paramsFrame.setGeometry(QRect(40, 400, 400, 600))
        
        self.labelStep1 = QLabel("Raising Step",self.paramsFrame)
        self.labelStep1.setGeometry(QRect(0, 0, 150, 50))
        
        self.labelVoltage1 = QLabel("0 Volt",self.paramsFrame)
        self.labelVoltage1.setGeometry(QRect(0, 30, 150, 50))
        
        self.labelCurrent1 = QLabel("0 ohm",self.paramsFrame)
        self.labelCurrent1.setGeometry(QRect(0, 60, 150, 50))
        
        self.labelTime1 = QLabel("0 second",self.paramsFrame)
        self.labelTime1.setGeometry(QRect(0, 90, 150, 50))
        
        self.labelStep2 = QLabel("Dwell Step",self.paramsFrame)
        self.labelStep2.setGeometry(QRect(0, 150, 150, 50))
        
        self.labelVoltage2 = QLabel("0 Volt",self.paramsFrame)
        self.labelVoltage2.setGeometry(QRect(0, 180, 150, 50))
        
        self.labelCurrent2 = QLabel("0 ohm",self.paramsFrame)
        self.labelCurrent2.setGeometry(QRect(0, 210, 150, 50))
        
        self.labelTime2 = QLabel("0 second",self.paramsFrame)
        self.labelTime2.setGeometry(QRect(0, 240, 150, 50))
        
        #Cycle state
        self.cycleState_label = QLabel("",self)
        self.cycleState_label.setGeometry(QRect(500, 10, 150, 50))
        self.cycleState_label.setFont(QtGui.QFont("Times",10, QtGui.QFont.Bold))
         
        
        #Time
        self.cycleTime_label = QLabel("",self)
        self.cycleTime_label.setGeometry(QRect(500, 30, 150, 50))
        self.cycleTime_label.setFont(QtGui.QFont("Times",10, QtGui.QFont.Bold))
        
        
        #Set parameters button
        self.setButton = QPushButton("Set Parameters",self)
        self.setButton.setGeometry(QRect(40,370,100,30))
        self.setButton.clicked.connect(self.set_parameters)
        
        #Run cycle button
        self.runButton = QPushButton("Run Cycle",self)
        self.runButton.setGeometry(QRect(250,700,100,30))
        self.runButton.clicked.connect(self.run_cycle)
        
        #Quit button
        self.exitButton = QPushButton("Quit",self)
        self.exitButton.move(self.width - 100,self.height - 30)
        self.exitButton.clicked.connect(self.exit_window)
        
        #Measurements frame
        self.measureFrame = QFrame(self) 
        self.measureFrame.setGeometry(QRect(self.width - 400, self.height - 200, 400, 400))
        self.measureFrame.setFont(QtGui.QFont("Times",9, QtGui.QFont.Bold))
        
        #1.step measurement Labels
        self.measureLabel1 =  QLabel("Raise step",self.measureFrame)
        self.measureLabel1.setGeometry(QRect(0, 30, 150, 50))
        self.measureLabel1.setFont(QtGui.QFont("Times",11, QtGui.QFont.Bold))
        
        self.measureLabelVoltage1 =  QLabel("Measured 0 Volt",self.measureFrame)
        self.measureLabelVoltage1.setGeometry(QRect(0, 60, 150, 50))
        
        self.measureLabelCurrent1 =  QLabel("Measured 0 ohm",self.measureFrame)
        self.measureLabelCurrent1.setGeometry(QRect(0, 90, 150, 50))
        
        self.measureLabel2 =  QLabel("Dwell step",self.measureFrame)
        self.measureLabel2.setGeometry(QRect(250, 30, 150, 50))
        self.measureLabel2.setFont(QtGui.QFont("Times",11, QtGui.QFont.Bold))
        
        self.measureLabelVoltage2 =  QLabel("Measured 0 Volt",self.measureFrame)
        self.measureLabelVoltage2.setGeometry(QRect(250, 60, 150, 50))
        
        self.measureLabelCurrent2 =  QLabel("Measured 0 ohm",self.measureFrame)
        self.measureLabelCurrent2.setGeometry(QRect(250, 90, 150, 50))
        self.show()

    @pyqtSlot()
    def set_parameters(self):
        self.voltage1 = int(self.inputVoltage1.text())
        self.current1 = int(self.inputCurrent1.text())
        self.time1 = int(self.inputTime1.text())
        
        self.voltage2 = int(self.inputVoltage2.text())
        self.current2 = int(self.inputCurrent2.text())
        self.time2 = int(self.inputTime2.text())
        
        self.labelVoltage1.setText(f"{self.voltage1} Volts")
        self.labelCurrent1.setText(f"{self.current1} ohms")
        self.labelTime1.setText(f"{self.time1} seconds")
        
        self.labelVoltage2.setText(f"{self.voltage2} Volts")
        self.labelCurrent2.setText(f"{self.current2} ohms")
        self.labelTime2.setText(f"{self.time2} seconds")
    
    @pyqtSlot()
    def run_cycle(self):
        try:
            #connection
            rm = visa.ResourceManager()
            SGX50X200D = rm.open_resource('TCPIP0::169.254.237.223::inst0::INSTR')
            
            
            
            #raise step
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage1))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current1))
            try:
                self.cycleState_label.setText("Cycle Running...(dwell)")
                self.cycleState_label.setStyleSheet("color: blue")
            except:
                print("cannnot print")
            time.sleep(self.time1)
            try:
                #temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
                #self.measured_voltage1 = temp_values[0]
                temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
                self.measured_current1 = temp_values[0]
                #self.measureLabelVoltage1.setText(f"{self.measured_voltage1} Volts")
                self.measureLabelCurernt1.setText(f"{self.measured_current1} ohms")
            except:
                print("no measure1")
            try:
                
                self.cycleState_label.setText("Cycle Running...(dwell)")
                self.cycleState_label.setStyleSheet("color: blue")
            except:
                print("cannnot print")
            #dwell step
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (self.voltage2))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (self.current2))
            time.sleep(self.time2)
            try:
                temp_values = SGX50X200D.query_ascii_values(':MEASure:VOLTage?')
                self.measured_voltage2 = temp_values[0]
                temp_values = SGX50X200D.query_ascii_values(':MEASure:CURRent?')
                self.measured_current2 = temp_values[0]
                self.measureLabelVoltage2.setText(f"{self.measured_voltage2} Volts")
                self.measureLabelCurernt2.setText(f"{self.measured_current2} ohms")
            except:
                print("ne measure")

            #end step
            SGX50X200D.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0))
            SGX50X200D.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (0))
            
            self.cycleState_label.setText("Cycle Completed...")
            self.cycleState_label.setStyleSheet("color: green")
            
            
        except:
            print("Error")
            self.cycleState_label.setText("Cycle Cancelled...")
            self.cycleState_label.setStyleSheet("color: red")
            pass
        
    @pyqtSlot()
    def exit_window(self):
        QCoreApplication.instance().quit()
     
    @pyqtSlot()
    def time_count(self):
        for i in range(self.time1):
            self.cycleTime_label.setText(f"{i}")
            time.sleep(1)
        for i in range(self.time2):
            self.cycleTime_label.setText(f"{i}")
            time.sleep(1)
        
        

def main():
    app = QApplication(sys.argv)
    window = MainPage(title = "Resistance Welding")
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()      
        