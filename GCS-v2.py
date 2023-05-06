# TFAC Ground Control UI v2, a more bare-bones version of UI v1

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QBrush, QPen
from pyqtgraph import *
import pyqtgraph as pg
from datetime import datetime
import serial

class GUI(QWidget):
    def __init__(self):
        super(GUI, self).__init__()

        # runs window setup, where the main gui window is initialized and all other functions are run
        self.window_setup() 

        # timer 
        self.timer = QtCore.QTimer()  # type: ignore
        self.timer.setInterval(300)

        self.timer.timeout.connect(self.breakData)
        self.timer.timeout.connect(self.updateData)
        self.timer.timeout.connect(self.state_Box)
        self.timer.timeout.connect(self.updateDateTime)

        # updates data in every 350 milliseconds
        self.timer.start()
        
    def window_setup(self):
        # window setup
        self.setStyleSheet("background-color: gray;" "QLabel{font-size: 24pt;}")
        self.setWindowTitle("TFAC Ground Control v2")
        self.setGeometry(0, 0, 525, 486)
            
        # run the other functions
        self.time_box()
        self.time_Date()
        self.TFAC_times()
        self.stateInit()
        self.main_TLMBox()
        self.mainData() 
        self.dataSeparator()
        self.miscData()

        # show the main window    
        self.show() 
    
    def time_box(self):
        Time_Box = QLabel('   ', self) # nothing 
        Time_Box.move(5, 10)
        Time_Box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        Time_Box.resize(300, 60)   
    
    def main_TLMBox(self):
        mainTLM_Box = QLabel('   ', self) # nothing 
        mainTLM_Box.move(12, 80)
        mainTLM_Box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        mainTLM_Box.resize(500, 400)

    def time_Date(self):
        DatePlaceHolder = QLabel('Date: ', self)
        DatePlaceHolder.move(17, 14)
        DatePlaceHolder.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt;") # is this the best way to do it? idk, does it work. Yes

        self.actualdate = QLabel('0000-00-00', self)
        self.actualdate.move(56, 14)
        self.actualdate.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        # Time, same thing as date
        TimePlaceHolder = QLabel('Time: ', self)
        TimePlaceHolder.move(17, 45)
        TimePlaceHolder.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        self.TimeIST = QLabel('00:00:00', self)
        self.TimeIST.move(56, 45)
        self.TimeIST.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt;")

        ISTLabel = QLabel('IST', self)
        ISTLabel.move(118, 45)
        ISTLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")
    
    def TFAC_times(self):
        # tfac is the name of my flight computer, this function basically shows the on time and flight time sent by the fc

        # on time
        OnTimeLabel = QLabel('On Time:', self) 
        OnTimeLabel.move(169, 14)
        OnTimeLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        self.RealOnTime = QLabel('1328.5', self)
        self.RealOnTime.move(235, 14)
        self.RealOnTime.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        OntimeSecLabel = QLabel('s', self)
        OntimeSecLabel.move(270, 14)
        OntimeSecLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        # flight time
        Flight_TimeLabel = QLabel('Flight Time:', self)
        Flight_TimeLabel.move(169, 45)
        Flight_TimeLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        self.ActualFltTime = QLabel('47', self)
        self.ActualFltTime.move(250, 45)
        self.ActualFltTime.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

        Flt_Time_secLabel = QLabel('s', self)
        Flt_Time_secLabel.move(275, 45)
        Flt_Time_secLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 11pt")

    def stateInit(self):
        self.sysState = QLabel("INIT", self)
        self.sysState.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.sysState.move(320, 10)
        self.sysState.setStyleSheet("background-color: #FFC0CB;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "font-size: 14pt;"
                                    "border-radius :5px")
        self.sysState.resize(200, 60)

        self.SYSSTATE = QLabel("10", self)
        self.SYSSTATE.move(600, 30)
 
    def dataSeparator(self):
        # this is a line that seperates the main tlm data with others
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)  # type: ignore
        line.setLineWidth(1)
        line.move(25, 390)
        line.resize(480, 10)
        line.setStyleSheet( "background-color: #FFFFFF")

    def mainData(self):
        # code that displays altitude
        altLabel = QLabel("Altitude:", self)
        altLabel.move(130, 100)
        altLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realAlt = QLabel("-1042.03", self)
        self.realAlt.move(230, 100)
        self.realAlt.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        altUnitLabel = QLabel("m", self)
        altUnitLabel.move(330, 100)
        altUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        # code that displays velocity
        velLabel = QLabel("Velocity:", self)
        velLabel.move(130, 150)
        velLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realVel = QLabel("-1368.02", self) # this is the variable that updates with data sent from the fc
        self.realVel.move(230, 150)
        self.realVel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        velUnitLabel = QLabel("m/s", self)
        velUnitLabel.move(330, 150)
        velUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        # code that displays acceleration
        accLabel = QLabel("Acceleration:", self)
        accLabel.move(83, 200)
        accLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realAcc = QLabel("-1234.96", self) # this is the variable that updates with data sent from the fc
        self.realAcc.move(230, 200)
        self.realAcc.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        accUnitLabel = QLabel("m/s²", self)
        accUnitLabel.move(330, 200)
        accUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        # code that displays latitude
        latLabel = QLabel("Latitude:", self)
        latLabel.move(127, 250)
        latLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realLat = QLabel("-82.48668098296324", self) # this is the variable that updates with data sent from the fc
        self.realLat.move(230, 250) 
        self.realLat.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        LatUnitLabel = QLabel("°", self)
        LatUnitLabel.move(369, 250)
        LatUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        # code that displays longitude
        longLabel = QLabel("Longitude:", self)
        longLabel.move(105, 300)
        longLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realLong = QLabel("-111.09375056954971", self) # this is the variable that updates with data sent from the fc
        self.realLong.move(225, 300)
        self.realLong.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        LongUnitLabel = QLabel("°", self)
        LongUnitLabel.move(369, 300)
        LongUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")
    
        # code that displays GNSS alt
        gpsAltLabel = QLabel("Alt ASL:", self)
        gpsAltLabel.move(130, 350)
        gpsAltLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        self.realgpsAlt = QLabel("-1000.00", self) # this is the variable that updates with data sent from the fc
        self.realgpsAlt.move(220, 350)
        self.realgpsAlt.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")

        gpsAltLabel = QLabel("m", self)
        gpsAltLabel.move(320, 350)
        gpsAltLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 18pt")
    
    def miscData(self):
        # code that displays temp
        tempLabel = QLabel("Temp:", self)
        tempLabel.move(25, 410)
        tempLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        self.realTemp = QLabel("50.34", self)
        self.realTemp.move(75, 410)
        self.realTemp.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        tempUnitLabel = QLabel("°C", self)
        tempUnitLabel.move(118, 410)
        tempUnitLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        # code that displays Sats
        SatsLabel = QLabel("Sats:", self)
        SatsLabel.move(25, 445)
        SatsLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        self.realSIV = QLabel("20", self)
        self.realSIV.move(65, 445)
        self.realSIV.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        # code that displays pyro altitudes
        p1AltLabel = QLabel("PY1 Alt: 200", self)
        p1AltLabel.move(200, 410)
        p1AltLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        p1AltUnit = QLabel("m", self)
        p1AltUnit.move(295, 410)
        p1AltUnit.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        p2AltLabel = QLabel("PY2 Alt: 0", self)
        p2AltLabel.move(200, 445)
        p2AltLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        p2AltUnit = QLabel("m", self)
        p2AltUnit.move(275, 445)
        p2AltUnit.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        # code that displays GNSS pDOP and Fix
        pdopLabel = QLabel("pDOP:", self)
        pdopLabel.move(400, 410)
        pdopLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        self.realpDOP = QLabel("9.34", self)
        self.realpDOP.move(455, 410)
        self.realpDOP.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        fixLabel = QLabel("Fix:", self)
        fixLabel.move(400, 445)
        fixLabel.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")

        self.realfix = QLabel("9", self)
        self.realfix.move(430, 445)
        self.realfix.setStyleSheet("background-color: #00FFFFFF;" "font-size: 13pt")
    
    def breakData(self):
        allData = ser.readline()
        allData = allData.decode()
        allData = allData.strip()
        
        # split data
        allData = str(allData)
        
        self.Acc, self.Vel, self.OnTme, self.FltTme, self.baroAlt, self.baroTemp, self.state, self.gpsSats, self.gpsPDOP, self.gpsfix, self.gpsLat, self.gpsLon, self.gnssAlt = allData.split(', ')

    def updateDateTime(self):
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        self.TimeIST.setText(current_time)
        self.actualdate.setText(current_date)
        
    def updateData(self):
        # updating all the placeholder data with real data from the flight computer

        # accel
        self.realAcc.setText(str(self.Acc))
        self.realVel.setText(str(self.Vel))

        # times
        self.RealOnTime.setText(self.OnTme)
        self.ActualFltTime.setText(self.FltTme)
        self.SYSSTATE.setText(str(self.state))

        # baro
        self.realAlt.setText(self.baroAlt)
        self.realTemp.setText(self.baroTemp)

        # gnss main
        self.realLat.setText(self.gpsLat)
        self.realLong.setText(self.gpsLon)
        self.realgpsAlt.setText(self.gnssAlt)

        # gnss misc
        self.realSIV.setText(self.gpsSats)
        self.realpDOP.setText(self.gpsPDOP)
        self.realfix.setText(self.gpsfix)
    
    def state_Box(self):
        # the system states on my flight computer, you can replace the values with your flight computer's states
        statestr = " "
        color = " "

        if (int(self.state) == 0):
            statestr = "INIT"
            color = "#FFC0CB" # hot pink
        elif (int(self.state) == 1):
            statestr = "IDLE"
            color = "#90EE90" # green
        elif (int(self.state) == 2):
            statestr = "ASCENT"
            color =  "#ADD8E6" # light blue
        elif (int(self.state) == 3):
            statestr = "DESCENT"
            color = "#FFC933" # yellow
        elif (int(self.state) == 4 or int(self.state) == 5):
            statestr = "LANDED"
            color = "#64EDD2" # teal

        self.sysState.setText(statestr) 
        self.sysState.setStyleSheet( "background-color:" + color + ";"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "font-size: 14pt;"
                                    "border-radius :5px")


ser = serial.Serial('COM9') # replace with your COM port

app = QApplication(sys.argv)
window = GUI()
window.show()

sys.exit(app.exec_())