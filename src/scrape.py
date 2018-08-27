import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import scipy.stats as stats
import copy
import numpy as np


class Scrape():
    '''
    This is used to grab boxscore data for each NBA team
    '''
    self.teams = ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
    
    self.team_dic = {  'Dallas':'DAL','Boston':'BOS','Toronto':'TOR','Denver':'DEN','Philadelphia':'PHI'\
            , 'New York':'NYK','Orlando':'ORL','Cleveland':'CLE','Detroit':'DET'\
            , 'Miami':'MIA','Charlotte':'CHO','Houston':'HOU','San Antonio':'SAS','LA Clippers':'LAC','Washington':'WAS'\
            , 'Oklahoma City':'OKC', 'Milwaukee':'MIL','Phoenix':'PHO','Sacramento':'SAC','New Orleans':'NOP'\
            , 'Indiana':'IND','Portland':'POR','Brooklyn':'BRK', 'Golden State':'GSW','Chicago':'CHI'\
            , 'LA Lakers':'LAL','Memphis':'MEM','Atlanta':'ATL','Utah':'UTA','Minnesota':'MIN'}

    def __init__(self):
        return self
    
    
    def _box_score_url_creator(self,team:str,year:str,baseurl:str)->list:
        '''
        returns url to team schedule
        '''
        if team == 'CHO' & int(year) < 2015:
                team = 'CHA'
        if team == 'BRK' & int(year) < 2013:
                team = 'NJN'
        if team == 'NOP' & int(year) < 2012:
                team = 'NOH'
        if team == 'OKC' & int(year) < 2009:
                team = 'SEA'

        return [baseurl + '/teams/' + team + '/' + year + '_games.html']

    def  _get_box_score_url(self,url,games=82):
        
        container = []
        for link in url.find_all('a'):
            k = str(link.get('href'))
            if k.startswith('/boxscores/20'):
                container.append(k)
        return container[:games]