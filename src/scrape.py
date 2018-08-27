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
    def __init__(self):
        
        self.baseurl = 'https://www.basketball-reference.com/'
        self.teams = ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW'\
                    ,'HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK'\
                    ,'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
    
        self.team_dic = {'Dallas':'DAL','Boston':'BOS','Toronto':'TOR','Denver':'DEN','Philadelphia':'PHI'\
            , 'New York':'NYK','Orlando':'ORL','Cleveland':'CLE','Detroit':'DET', 'Miami':'MIA'\
            , 'Charlotte':'CHO','Houston':'HOU','San Antonio':'SAS','LA Clippers':'LAC','Washington':'WAS'\
            , 'Oklahoma City':'OKC', 'Milwaukee':'MIL','Phoenix':'PHO','Sacramento':'SAC','New Orleans':'NOP'\
            , 'Indiana':'IND','Portland':'POR','Brooklyn':'BRK', 'Golden State':'GSW','Chicago':'CHI'\
            , 'LA Lakers':'LAL','Memphis':'MEM','Atlanta':'ATL','Utah':'UTA','Minnesota':'MIN'}

    def _box_score_url_creator_bbref(self,team:str,year:str)->list:
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

        return [self.baseurl + '/teams/' + team + '/' + year + '_games.html']

    def  _get_box_score_url(self,url,games=82):
        '''
        returns boxscore link container
        '''
        container = []
        for link in url.find_all('a'):
            k = str(link.get('href'))
            if k.startswith('/boxscores/20'):
                container.append(k)
        return container[:games]
    
    def _url_list_generator(self,teams:list,years:list):
        biglist = {}
        for team in teams:
            biglist[team] = {}
            biglist[team]['year'] = {}
            for year in years:
                biglist[team]['year'][year] = self._box_score_url_creator_bbref(team,year)
        return biglist

    def _soup_maker(self,dct:dict):
        '''
        returns dictonary of boxscore links separated by team and year
        '''
        boxscores = {}
        for team in dct.keys():
            boxscores[team] = {}
            boxscores[team]['year'] = {}
            for year in dct[team]['year'].keys():
                url = dct[team]['year'][year][0]
                r = requests.get(url)
                soup = BeautifulSoup(r.content,'html.parser')
                boxscores[team]['year'][year] = self._get_box_score_url(url,games=82)
                time.sleep(3)
        return boxscores

#populates urls for each team for each year and then generates a dictionary to scrape from
    