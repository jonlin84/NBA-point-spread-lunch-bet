import time
import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import pandas as pd
import scipy.stats as stats
import copy
import numpy as np


class Scrape():
    '''
    This is used to grab boxscore data for each NBA team puts in boxscore collection the chosen
    mongodb name
    Pass a list of years you want scraped ex. ['2009','2010','2011']
    '''

    def __init__(self,years:list,dbname):
        
        self.dbname = dbname
        self.client = MongoClient()
        self.years = years
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

        self.sp = {'BOS':'20722','PHI':'20731','BRK':'20749','NYK':'20747','TOR':'20742','DET':'20743','CLE':'20735','CHI':'20732','IND':'20737','MIL':'20725','CHO':'20751','MIA':'20726','ORL':'20750'
        ,'ATL':'20734','WAS':'20746','OKC':'20728','POR':'20748','DEN':'20723','UTA':'20738','MIN':'20744','SAC':'20745','PHO':'20730','LAL':'20739','LAC':'20736','GSW':'20741','DAL':'20727',
         'MEM':'20729','HOU':'20740','SAS':'20724','NOP':'20733'}

        self.baselink = 'https://www.oddsshark.com/stats/gamelog/basketball/nba/'
    
    def build_db(self):
        big_list = self._url_list_generator()
        boxscores = self._soup_maker(big_list)
        self._insert_db(boxscores)
        
    
    def _box_score_url_creator_bbref(self,team:str,year:str)->list:
        '''
        returns url to team schedule
        '''
        if (team == 'CHO') & (int(year) < 2015):
                team = 'CHA'
        if (team == 'BRK') & (int(year) < 2013):
                team = 'NJN'
        if (team == 'NOP') & (int(year) < 2012):
                team = 'NOH'
        if (team == 'OKC') & (int(year) < 2009):
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
                container.append(self.baseurl+k)
        return container[:games]
    
    def _url_list_generator(self):
        biglist = {}
        for team in self.teams:
            biglist[team] = {}
            biglist[team]['year'] = {}
            for year in self.years:
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
                boxscores[team]['year'][year] = self._get_box_score_url(soup,games=82)
                time.sleep(3)
        return boxscores
    
    def _insert_db(self,dct):
        for team in self.teams:
            for year in self.years:
                for items in dct[team]['year'][year]:
                    r = requests.get(items)
                    time.sleep(3)
                    boxscore = {'team':team,
                                'year': year,
                                'url':items,
                                'content': r.content }
                    self.client[self.dbname]['boxscores'].insert_one(boxscore)
    
    def spread_populator(self):
        for team in self.teams:
            for year in years:
                url = self.baselink + self.sp[team] + '/' + year
                r = requests.get(url)
                time.sleep(10)
                spreadlist = {'team':team,
                             'year': year,
                             'url':url,
                             'content': r.content }
                self.client[self.dbname]['spreads'].insert_one(spreadlist)

