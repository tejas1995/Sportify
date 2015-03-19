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
        self.score1 = []
        self.score2 = []
        self.match_time = []
        self.match_status = []

        response = urllib2.urlopen(self.site)
        html = response.read()
        parsed_html = BeautifulSoup(html)
        
        matchList = parsed_html.body.find_all('div', attrs={'class':'mod-container mod-no-header-footer mod-scorebox mod-nba-scorebox in-game '})

        for match in matchList:
            x1 = match.find('div', attrs={'class':'team away'})
            team1 = x1.find('p', attrs={'class': 'team-name'}).text
            score1 = x1.find('li', attrs={'class': 'finalScore'}).text

            x2 = match.find('div', attrs={'class':'team home'})
            team2 = x2.find('p', attrs={'class': 'team-name'}).text
            score2 = x2.find('li', attrs={'class': 'finalScore'}).text

            match_status = match.find('div', attrs={'class':'game-status'}).text
            
            self.team1.append(team1)
            self.team2.append(team2)			
            self.score1.append(score1)
            self.score2.append(score2)
            self.match_status.append(match_status)

            if ':' in match_status:
                c = 0
                time = 0

                while not match_status[c] == ':':
                    time = time*10 + ord(match_status[c])-48
                    c = c+1
				
                time = time*60
				
                sTime = 0
                c = match_status.index(':')+1
                sTime = (ord(match_status[c])-48)*10 + ord(match_status[c+1])-48
                time = time + sTime
                time = (ord(match_status[c+3])-48)*720 - time
                
                self.match_time.append(time)
            else:
                self.match_status.append(match_status)
                self.match_time.append(0)
            
        if not len(self.team1) == len(self.oldTime):
            self.oldTime = []
            for i in range(len(self.team1)):
                self.oldTime.append(0)

    def set_prefs(self,teams):
        new_teams=[]
        for team in teams:
            new_teams.append(team[:3])
        self.teams= self.teams + new_teams
    
    def scoreString(self):
        score = ""
        for i in range(0, len(self.team1)):
            try:
                if( self.team1[i][:3] in self.teams or self.team2[i][:3] in self.teams):
                    if self.match_time[i] - self.oldTime[i] >= 120 or (self.match_time[i] == 0 and not self.oldTime[i] == 0):
                        score = score + self.team1[i]
                        for j in range(20 - len(self.team1[i])):
                            score = score + ' '
                        score = score + str(self.score1[i]) + '\n' + self.team2[i]
                        for j in range(20 - len(self.team2[i])):
                            score = score + ' '
                        score = score + str(self.score2[i]) + '\n'
                        score = score + self.match_status[i] + '\n'
                        self.oldTime[i] = self.match_time[i]
            except:
                return ""
        
        return score  

