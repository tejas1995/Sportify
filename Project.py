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

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.cric = QtGui.QCheckBox('Cricket', self)
        self.cric.move(20, 20)
        self.cric.stateChanged.connect(self.addWidget0)
        
        self.bask = QtGui.QCheckBox('Basketball', self)
        self.bask.move(100, 20)
        self.bask.stateChanged.connect(self.addWidget1)

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
        self.test = [None, None]

    def addWidget0(self, state):
        print 'Cricket'
        self.addWidget(0, state)

    def addWidget1(self, state):
        print 'Basketball'
        self.addWidget(1, state)

    def addWidget(self, sportNum, state):
        if state == QtCore.Qt.Checked:
            self.test[sportNum] = Test(listTeams[sportNum])
            self.scrollLayout.addWidget(self.test[sportNum])
        else:
            self.scrollLayout.removeWidget(self.test[sportNum])
            self.test[sportNum].deleteLater()
            self.test[sportNum] = None

    def printf(self):
        listi = [[], []]
        for i in range(2):
            for j in range(len(listTeams[i])):
                if self.test[i].listCheckboxes[j].isChecked():
                    listi[i].append(j)      
            print listi[i]        
            for j in listi[i]:
                pTeam[i].append(listTeams[i][j])

class Test(QtGui.QWidget):
    def __init__( self, listTeams, parent=None):
        super(Test, self).__init__(parent)
        self.listCheckboxes = []

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

        layout = QtGui.QVBoxLayout()
        for i in range(len(listTeams)/2):
            layout.addLayout(hBox[i])
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
basketBallGame = Basketball('http://scores.espn.go.com/nba/scoreboard')

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
        
