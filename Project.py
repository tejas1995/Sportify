from bs4 import BeautifulSoup
import urllib2
import time
import pynotify
import datetime
from Cricket import *
from Basketball import *
from PyQt4 import QtGui, QtCore
import sys

pTeam = [[], []]

listTeams = [['Afghanistan','Australia','Bangladesh',
                    'England','India' ,'Ireland','New Zealand', 
                    'Pakistan','Scotland', 'South Africa','Sri Lanka', 
                    'United Arab Emirates', 'West Indies',  'Zimbabwe'],
                    
                    ['Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers',
                     'Grizzlies', 'Hawks', 'Heat', 'Hornets', 'Jazz',
                     'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 
                     'Nets', 'Nuggets', 'Pacers', 'Pelicans', 'Pistons', 
                     'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 
                     'Timberwolves', 'Trail Blazers', 'Warriors', 'Wizards', '76ers']]


listTimes = [['2 minutes', '5 minutes', '10 minutes', '15 minutes', '20 minutes', '30 minutes'],
             ['30 seconds', '1 minute', '2 minutes', '3 minutes', '5 minutes']]

timeList = [[120, 300, 600, 900, 1200, 1800],
            [30, 60, 120, 180, 300]]

#Default time settings
notifTime = [300, 120]
listTeamsSelected = [[],[]]

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.sportButtons = []
        self.sportButtons.append(QtGui.QRadioButton('Cricket', self))
        self.sportButtons[0].move(20, 20)
        self.sportButtons[0].toggled.connect(self.addWidget0)
        
        self.sportButtons.append(QtGui.QRadioButton('Basketball', self))
        self.sportButtons[1].move(100, 20)
        self.sportButtons[1].toggled.connect(self.addWidget1)

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
        self.mainLayout.addWidget(self.sportButtons[0])
        self.mainLayout.addWidget(self.sportButtons[1])
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        self.showMaximized()
        self.show()
        self.test = [None, None]

    def addWidget0(self, state):
        if self.sportButtons[0].isChecked():
            self.addWidget(0, state)

    def addWidget1(self, state):
        if self.sportButtons[1].isChecked():
            self.addWidget(1, state)

    def addWidget(self, sportNum, state):
        
        if not self.test[1-sportNum] == None:

            for j in range(len(listTeams[1-sportNum])):
                if self.test[1-sportNum].listCheckboxes[j].isChecked():
                    listTeamsSelected[1-sportNum].append(j)      
            for j in listTeamsSelected[1-sportNum]:
                pTeam[1-sportNum].append(listTeams[1-sportNum][j])

            for j in range(len(listTimes[1-sportNum])):
                if self.test[1-sportNum].listTimeButtons[j].isChecked():
                    notifTime[1-sportNum] = timeList[1-sportNum][j]
                
            self.scrollLayout.removeWidget(self.test[1-sportNum])
            self.test[1-sportNum].deleteLater()
            self.test[1-sportNum] = None

        self.test[sportNum] = Test(listTeams[sportNum], listTimes[sportNum])
        self.scrollLayout.addWidget(self.test[sportNum])

    def printf(self):
        for i in range(2):
            if self.test[i]:
                for j in range(len(listTeams[i])):
                    if self.test[i].listCheckboxes[j].isChecked():
                        listTeamsSelected[i].append(j)      
                for j in listTeamsSelected[i]:
                    pTeam[i].append(listTeams[i][j])

                for j in range(len(listTimes[i])):
                    if self.test[i].listTimeButtons[j].isChecked():
                        notifTime[i] = timeList[i][j]
                        
class Test(QtGui.QWidget):
    def __init__( self, listTeams, listTimes, parent=None):
        super(Test, self).__init__(parent)
        self.listCheckboxes = []
        self.listTimeButtons = []

        hBox = []
        for i in range(len(listTeams)/2):
            hBox.append([])
        for i in range(len(listTeams)/2):
            hBox[i] = QtGui.QHBoxLayout()
       
        for i in range(len(listTeams)):
            self.listCheckboxes.append(QtGui.QCheckBox(listTeams[i], self))
            self.listCheckboxes[i].move(20 + 40*(i/2), 20+40*(i%2))
            self.listCheckboxes[i].stateChanged.connect(self.selectstuff)
            hBox[i/2].addWidget(self.listCheckboxes[i])

        hLabel = QtGui.QHBoxLayout()
        hLabel.addWidget(QtGui.QLabel('Time between notifications:', self))

        hTimeBox = QtGui.QHBoxLayout()
        for i in range(len(listTimes)):
            self.listTimeButtons.append(QtGui.QRadioButton(listTimes[i], self))
            self.listTimeButtons[i].move(20, 20+40*i)
            hTimeBox.addWidget(self.listTimeButtons[i])

        layout = QtGui.QVBoxLayout()
        for i in range(len(listTeams)/2):
            layout.addLayout(hBox[i])
        layout.addLayout(hLabel)
        layout.addLayout(hTimeBox)
        self.setLayout(layout)

    def selectstuff(self,state):
        pass
    
def send_message(title, scoreString):
    pynotify.init("image")
    notice = pynotify.Notification(title, scoreString, "cricket.jpg").show()
    return notice

app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
print pTeam

cricketGame = Cricket('http://www.espncricinfo.com/ci/engine/match/index.html?view=live')  
basketBallGame = Basketball('http://scores.espn.go.com/nba/scoreboard', notifTime[1])

timeOld = datetime.datetime.now().replace(microsecond=0)
cricketGame.set_prefs(pTeam[0])
cricketGame.parsePage()
cricketGame.updateWickets()

basketBallGame.set_prefs(pTeam[1])
basketBallGame.parsePage()
basketBallGame.oldTime = basketBallGame.match_time[:];

while(True):
    timeNew = datetime.datetime.now().replace(microsecond=0)
    diff = timeNew - timeOld
    hours = (diff.seconds)/3600
    minutes= (diff.seconds - hours*3600)/60
    seconds = (diff.seconds - (hours*3600 + minutes*60))
	
    totalTime = 60*minutes + seconds
    
    try:
        cricketGame.parsePage()
    except:
        continue

    if totalTime >= notifTime[0]:
        score = cricketGame.scoreString()
        if score:
            send_message(cricketGame.title, score)
        timeOld = timeNew
    else:
        for i in range(len(cricketGame.inningsL1)):
            if cricketGame.getWickets(cricketGame.currInn(cricketGame.inningsL1[i],cricketGame.inningsL2[i])) == cricketGame.wicketList[i]+1:
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
