import sys
from bs4 import BeautifulSoup
import urllib2
from Sport import *

class Basketball(Sport):
    def __init__(self, site):
        Sport.__init__(self, site)
        self.teams = []
        self.image = ""
        self.title = "Basketball Update"
        self.oldTime = []

    def parsePage(self):
        self.team1 = []
        self.team2 = []
        self.score = []
        self.match_time = []
        self.match_status = []

        response= urllib2.urlopen(self.site)
        html = response.read()
        parsed_html = BeautifulSoup(html)
        
        matchList = parsed_html.body.find_all('tr', attrs={'class':'component-scoreboard-list live'})

        for match in matchList:
            team1 = match.find('div', attrs={'class':'team left'}).h3.text
            team2 = match.find('div', attrs={'class':'team right'}).h3.text

            score = match.find('div', attrs={'class':'scores'}).text

            match_status = match.find('span', attrs={'class':'time'}).text

            self.team1.append(team1)
            self.team2.append(team2)			
            self.score.append(score)

            if ':' in match_status:
                self.match_status.append(match_status[:3] + " Quarter " + match_status[4:])
                c = self.match_status[len(self.match_status)-1].index('|')+2
                time = 0

                while not self.match_status[len(self.match_status)-1][c] == ':':
                    time = time*10 + ord(self.match_status[len(self.match_status)-1][c])-48
                    c = c+1
				
                time = time*60
				
                sTime = 0
                c = self.match_status[len(self.match_status)-1].index(':')+1
                sTime = (ord(self.match_status[len(self.match_status)-1][c])-48)*10 + ord(self.match_status[len(self.match_status)-1][c+1])-48
                time = time + sTime
                time = (ord(self.match_status[len(self.match_status)-1][0])-48)*720 - time
                
                self.match_time.append(time)
            else:
                self.match_status.append(match_status)
                self.match_time.append(0)

    def set_prefs(self,teams):
        new_teams=[]
        for team in teams:
            new_teams.append(team[:3])
        self.teams= self.teams + new_teams
    
    def scoreString(self):
        score = ""
        for i in range(0, len(self.team1)):
            if( self.team1[i][:3] in self.teams or self.team2[i][:3] in self.teams):
                try:
                    x = 0
                    while self.score[i][x] < '0' or self.score[i][x] > '9':
                        x += 1
                    y = x
                    while self.score[i][y] >= '0' and self.score[i][y] <= '9':
                        y += 1
                    score1 = self.score[i][x:y]

                    x = y
                    while self.score[i][x] < '0' or self.score[i][x] > '9':
                        x += 1
                    y = x
                    while self.score[i][y] >= '0' and self.score[i][y] <= '9':
                        y += 1
                    score2 = self.score[i][x:y]
                except:
                    return 0

                if self.match_time[i] - self.oldTime[i] >= 10:
                    score += self.team1[i] + '\t' + str(score1) + '\n'
                    score += self.team2[i] + '\t' + str(score2) + '\n'
                    score += self.match_status[i] + '\n\n'
                    self.oldTime = self.match_time[:]
        return score  

