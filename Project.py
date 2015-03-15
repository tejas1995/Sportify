from bs4 import BeautifulSoup
import urllib2
import time
import pynotify
import datetime
from Cricket import *
from Basketball import *
from PyQt4 import QtGui, QtCore
import sys
pteam = []
list_teams=['Afghanistan','Australia','Bangladesh','England','India' ,'Ireland','New Zealand', 'Pakistan','Scotland', 'South Africa','Sri Lanka', 'United Arab Emirates', 'West Indies',  'Zimbabwe']
listi = []

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.cric = QtGui.QCheckBox('Cricket', self)
        self.cric.move(20, 20)
        self.cric.stateChanged.connect(self.addWidget)
        
        self.bask = QtGui.QCheckBox('Basketball', self)
        self.bask.move(100, 20)
        self.bask.stateChanged.connect(self.addbWidget)

        self.addButton = QtGui.QPushButton('Submit')
        self.addButton.clicked.connect(self.printf)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.bask)
        self.mainLayout.addWidget(self.cric)
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self,state):
        if state == QtCore.Qt.Checked:
            self.test = Test()
            self.scrollLayout.addWidget(self.test)
        else:
            self.scrollLayout.removeWidget(self.test)
            self.test.deleteLater()
            self.test = None
    def addbWidget(self,state):
        pass
    def printf(self):
        for i in range(len(list_teams)):
            if self.test.list_checkboxes[i].isChecked():
                  listi.append(i)      
        print listi        
        for i in listi:
            pteam.append(list_teams[i])

            
class Test(QtGui.QWidget):
    def __init__( self, parent=None):
        super(Test, self).__init__(parent)
        self.list_checkboxes=[]
        layout = QtGui.QHBoxLayout()

        for i in range(len(list_teams)):
            self.list_checkboxes.append(QtGui.QCheckBox(list_teams[i], self))
            self.list_checkboxes[i].move(20, 20+40*i)
            self.list_checkboxes[i].stateChanged.connect(self.selectstuff)
            layout.addWidget(self.list_checkboxes[i])

        self.setLayout(layout)
    def selectstuff(self,state):
        pass
    
app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
print pteam
 
def send_message(title, scoreString):
    pynotify.init("image")
    notice = pynotify.Notification(title, scoreString, "cricket.jpg").show()
    return notice

cricketGame=Cricket('http://www.espncricinfo.com/ci/engine/match/index.html?view=live')  
basketBallGame = Basketball('http://www.si.com/nba/schedule')

timeOld = datetime.datetime.now().replace(microsecond=0)
cricketGame.set_prefs(pteam)
cricketGame.parsePage()
cricketGame.updateWickets()

basketBallGame.parsePage()
basketBallGame.oldTime = basketBallGame.match_time[:];

while(True):
    timeNew = datetime.datetime.now().replace(microsecond=0)
    diff = timeNew - timeOld
    hours = (diff.seconds)/3600
    minutes= (diff.seconds - hours*3600)/60
    seconds = (diff.seconds - (hours*3600 + minutes*60))
	
    
    try:
        cricketGame.parsePage()
    except:
        continue

    if seconds > 30:
        score = cricketGame.scoreString()
        if score:
            send_message(cricketGame.title, cricketGame.scoreString())
        timeOld = timeNew
    else:
        for i in range(len(cricketGame.inningsL1)):
            if not cricketGame.getWickets(cricketGame.currInn(cricketGame.inningsL1[i], cricketGame.inningsL2[i])) == cricketGame.wicketList[i]:
                send_message("WICKET!", cricketGame.scoreString(1))
                cricketGame.updateWickets()   
                timeOld = timeNew
        
    try:
        basketBallGame.parsePage()
    except:
        continue

    score = basketBallGame.scoreString()
    if score:
        send_message(basketBallGame.title, score)      



