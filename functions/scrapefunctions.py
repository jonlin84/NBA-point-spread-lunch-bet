import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import scipy.stats as stats

#returns basketball-refrence.com/teams/{teamname}/{year}_games.html
def box_score_url_creator(team:str,year:str,baseurl:str)->list:
    return [baseurl + '/teams/' + team + '/' + year + '_games.html']


#returns big dictionary of teams:{'year'{year:[html]}}
#team name, 'year' dictornary with year# key and list of string value
#example {'HOU':{'year':{1994:[www.worldchampions.com]}}}
def url_list_generator(teams:list,years:list):
    biglist = {}
    baseurl = 'https://www.basketball-reference.com'
    for team in teams:
        biglist[team] = {}
        biglist[team]['year'] = {}
        for year in years:
            biglist[team]['year'][int(year)] = box_score_url_creator(team,year,baseurl)
    return biglist

#taking big list and making containers
def soup_maker(dct:dict):
    boxscores = {}
    for team in dct.keys():
        boxscores[team] = {}
        for year in dct[team]['year'].keys():
            boxscores[team]['year'] = {}
            url = dct[team]['year'][year][0]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            boxscores[team]['year'][int(year)] = get_box_score_url(soup)
            time.sleep(3)

#returns a list of urls extensions to boxscores from a team for a particular year
#soup should be the parsed content from a team/year's url
def get_box_score_url(soup):
    container = []
    for link in soup.find_all('a'):
        k = str(link.get('href'))
        if k.startswith('/boxscores/20'):
            container.append(k)
    return container[:82]

#second attempt to make soup, this did not work as intended...DEBUG <---
def soup_maker(dct:dict):
    boxscores = {}
    for team in dct.keys():
        boxscores[team] = {}
        for year in dct[team]['year'].keys():
            boxscores[team]['year'] = {}
            url = dct[team]['year'][int(year)][0]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            boxscores[team]['year'][int(year)] = get_box_score_url(soup)
            time.sleep(3)
    return boxscores

#Write a function that extracts data and stores it in proper dictionaries
#Basica box score stats for each team and also information on officals
#assume first official is HEAD OFFICIAL?

#html = r.content, returns dictionary of box score totals
def scrape_stats_from_page(html,team:str):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select(f'#box_{team.lower()}_basic tfoot tr td')
    return {item.attrs.get('data-stat'): item.text for item in items}

#--------------------------------------------------------------
#all relevant functions I used

#code to create dictionary with
#probably bad practice but
# iterates over each row and populates a dictionary 
#returns dictionary
def create_dct_content_spread(df):
    biglist = {}
    for i in range(len(df.content)):
        if df.team[i] not in biglist.keys():
            biglist[df.team[i]] = {}
        if df.year[i] not in biglist[df.team[i]].keys():
            biglist[df.team[i]][df.year[i]] = {}
        soup = BeautifulSoup(df.content[i], 'html.parser')
        for count,items in enumerate(soup.select('tbody tr'),1):
            biglist[df.team[i]][spreads_df.year[i]][count] = []
            temp = []
            for item in items.select('td'):
                temp.append(item.get_text())
            biglist[df.team[i]][df.year[i]][count] += temp
    return biglist

'''
list of variables to use for iterations

teams    =    ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']

years    =    ['2014','2015','2016','2017','2018']

team_dic = {  'Dallas':'DAL','Boston':'BOS','Toronto':'TOR','Denver':'DEN','Philadelphia':'PHI'\
            , 'New York':'NYK','Orlando':'ORL','Cleveland':'CLE','Detroit':'DET'\
            , 'Miami':'MIA','Charlotte':'CHO','Houston':'HOU','San Antonio':'SAS','LA Clippers':'LAC','Washington':'WAS'\
            , 'Oklahoma City':'OKC', 'Milwaukee':'MIL','Phoenix':'PHO','Sacramento':'SAC','New Orleans':'NOP'\
            , 'Indiana':'IND','Portland':'POR','Brooklyn':'BRK', 'Golden State':'GSW','Chicago':'CHI'\
            , 'LA Lakers':'LAL','Memphis':'MEM','Atlanta':'ATL','Utah':'UTA','Minnesota':'MIN'}

team_variables = ['fg','fga','fg3','fg3a','ft','fta', 'orb','drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pts', 'pf', \
'opp_fg', 'opp,fga', 'opp_fg3', 'opp_fg3a', 'opp_ft', 'opp_fta', 'opp_orb', 'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov', 'opp_pf', 'opp_pts']
'''

#function to change the string in opponent to 3 letter abbreviation consistent for search
#used in spread dataframe.
def switch_to_key(x):
    for k,v in team_dic.items():
        if k in x:
            return v

#takes dataframe and list of teams('strings') 

def dataframe_separator(df,teams:list):
    #returns a dictionary with team abbreviation as keys and dataframes as values
    lst = []
    for team in teams:
        lst.append(copy.deepcopy(df[df.team == f'{team}']))
    return dict(zip(teams,lst))

#this is a redundant function, above function preserves df no need to cast to dataframe
'''
def dic_df_maker(dct,teams):
    dic_df = {}
    for team in teams:
        dic_df[team] = pd.DataFrame(dct[team])
    return dic_df
'''

#probably recode where it can take values from a dictionary vs roundabout way of converting to df
def team_sampler(team1:str,team2:str,avgs:dict,year:str,weight=.5,samples=1):
    '''
    takes two team inputs and a dictionary with teams as keys and values as averages and standard deviations
    the sample weight is with respect to team1
    '''

    team1_fg = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg.values[1])).rvs(samples).mean()
    
    team2_fg   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).fg.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).fg.values[1])).rvs(samples).mean()
    
    team1_fga  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fga.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fga.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fga.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fga.values[1])).rvs(samples).mean()
    
    team2_fga  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fga.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).fga.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fga.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).fga.values[1])).rvs(samples).mean()
    
    team1_fg3  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg3.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg3.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg3.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg3.values[1])).rvs(samples).mean()
    
    team2_fg3  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg3.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fg3.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg3.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fg3.values[1])).rvs(samples).mean()
    
    team1_fg3a = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg3a.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_fg3a.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg3a.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_fg3a.values[1])).rvs(samples).mean()
    
    team2_fg3a = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg3a.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fg3a.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg3a.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fg3a.values[1])).rvs(samples).mean()
    
    team1_ft   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).ft.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_ft.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).ft.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_ft.values[1])).rvs(samples).mean()
    
    team2_ft    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_ft.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).ft.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_ft.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).ft.values[1])).rvs(samples).mean()
    
    team1_fta   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fta.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_fta.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).fta.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_fta.values[1])).rvs(samples).mean()
    
    team2_fta   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fta.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fta.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fta.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fta.values[1])).rvs(samples).mean()
    
    team1_orb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).orb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_orb.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).orb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_orb.values[1])).rvs(samples).mean()
    
    team2_orb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_orb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).orb.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_orb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).orb.values[1])).rvs(samples).mean()
    
    team1_drb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).drb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_drb.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).drb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_drb.values[1])).rvs(samples).mean()
    
    team2_drb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_drb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).drb.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_drb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).drb.values[1])).rvs(samples).mean()
    
    #total rebounds should just be the sum of orb and drb which i will intially leave it out
    
    team1_ast    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).ast.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_ast.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).ast.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_ast.values[1])).rvs(samples).mean()
    
    team2_ast    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_ast.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).ast.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_ast.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).ast.values[1])).rvs(samples).mean()
    
    team1_stl    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).stl.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_stl.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).stl.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_stl.values[1])).rvs(samples).mean()
    
    team2_stl    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_stl.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).stl.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_stl.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).stl.values[1])).rvs(samples).mean()
    
    team1_blk    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).blk.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_blk.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).blk.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_blk.values[1])).rvs(samples).mean()
    
    team2_blk    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_blk.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).blk.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_blk.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).blk.values[1])).rvs(samples).mean()
    
    team1_tov    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).tov.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_tov.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).tov.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_tov.values[1])).rvs(samples).mean()
    
    team2_tov    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_tov.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).tov.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_tov.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).tov.values[1])).rvs(samples).mean()
    #team points should be an aggregation of other generated stats
    '''
    team1_pts    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).pts.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_pts.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).pts.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_pts.values[1])).rvs(samples).mean()
    
    team2_pts    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_pts.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).pts.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_pts.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).pts.values[1])).rvs(samples).mean()
    '''
    return [team1_fg, team1_fga, team1_fg3, team1_fg3a, team1_ft,team1_fta,team1_orb,team1_drb,team1_ast,team1_stl \
          , team1_blk,team1_tov,
            team2_fg, team2_fga, team2_fg3, team2_fg3a, team2_ft,team2_fta,team2_orb,team2_drb,team2_ast,team2_stl\
           ,team2_blk,team2_tov]


def create_dataframe_matchups(team1:str,team2:list,team_avg:dict,year:str,weight=.5,samples=1):
    lst = []
    columns = ['team1_fg','team1_fga','team1_fg3','team1_fg3a','team1_ft','team1_fta','team1_orb','team1_drb'\
          ,'team1_ast','team1_stl','team1_blk','team1_tov','team2_fg','team2_fga','team2_fg3','team2_fg3a'\
          ,'team2_ft','team2_fta','team2_orb','team2_drb'\
          ,'team2_ast','team2_stl','team2_blk','team2_tov']
    for team in team2:
        lst.append(team_sampler(team1,team,team_avg,year,weight,samples))
    df = pd.DataFrame(lst)
    df.columns = columns
    df.index = range(1,83)
    return df

def final_df_creator(team:str,year:str,spread_df,team_avg:dict,weight=.5,samples=1):
    '''
    takes 3 letter team abbreviation, the year as a string, the cleaned spread_df, dictionary and returns
    2 dataframes; final_df: all the transformed features and y: the labels
    
    weight: is the weighted distribution of the home team, currently it weights each season but feature implementations
    will attempt to adjust individual games, default = .5 (even weight for both team)

    sample: number of random samples from generated distributions to average, default = 1

    df = copy.deepcopy(spread_df[(spread_df.team == team) & (spread_df.year == year)])
    df.index = range(1,83)
    opp = df.opp.values
    new_df = create_dataframe_matchups(team,opp,team_avg,year,weight,samples)
    final_df = pd.concat([df[['spread','home']],new_df],axis=1)
    y_df = df.ats
    return final_df, y_df