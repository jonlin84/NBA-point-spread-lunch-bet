import datetime
import pandas as pd

teams    =    ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
#this function is to be run on pickled spread df (which has already been cleaned up to some degree)
#current runtime approximately 3 minutes on 12300 rows
spread_dct = {'BOS':'20722','PHI':'20731','BRK':'20749','NYK':'20747','TOR':'20742','DET':'20743','CLE':'20735','CHI':'20732','IND':'20737','MIL':'20725','CHO':'20751','MIA':'20726','ORL':'20750'
        ,'ATL':'20734','WAS':'20746','OKC':'20728','POR':'20748','DEN':'20723','UTA':'20738','MIN':'20744','SAC':'20745','PHO':'20730','LAL':'20739','LAC':'20736','GSW':'20741','DAL':'20727',
         'MEM':'20729','HOU':'20740','SAS':'20724','NOP':'20733'}
#takes dataframe of spread and extracts content from it and places it in a dictionary

years = ['2014', '2015', '2016', '2017', '2018']

baselink = 'https://www.oddsshark.com/stats/gamelog/basketball/nba/'
#db = clients.spreads
#function takes teamlist and puts it in 
def spread_populator(teamlist=teams,years=years,dct=spread_dct):
    '''
    scrapes spread data from oddsshark
    '''
    baselink = 'https://www.oddsshark.com/stats/gamelog/basketball/nba/'
    
    for team in teamlist:
        collection = db[f'{team}']
        for year in years:
            url = baselink + dct[team] + '/' + year
            r = requests.get(url)
            time.sleep(10)
            spreadlist = {'year': year,
                        'url':url,
                        'content': r.content }
            db[f'{team}'].insert_one(spreadlist)
#spreads = client.spreads
#spreadscombined = client.spreadscombined

def move_to_single_collection(teams)
    '''
    inputs each row from each collection into a single collection with a new team column
    '''
    for team in teams:
        for row in spreads[team].find():
            row['team'] = team
            spreadscombined.unified.insert_one(row)
#create dataframe from spreadscombined.unified
#spread_df = pd.DataFrame(list(spreadscombined.unified.find()))
#pass spread_df into create_dct_content_spread
#spread_df = spreads_df.drop(columns='parsed')
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
#test = pd.DataFrame(data=biglist)


extract_info = [[team,year,game,test[team][year][game][0],test[team][year][game][1],test[team][year][game][2],test[team][year][game][3],test[team][year][game][4],test[team][year][game][5],test[team][year][game][6],test[team][year][game][7],test[team][year][game][8]] for team in test.keys() for year in test[team].keys() for game in test[team][year].keys()]
#pass extracted info into a pandas dataframe 

new_spread_df = pd.DataFrame(data=extract_info)
new_spread_df.columns =['team','year','g','date','opp','gametype','result','score','ats','spread','ou','total']
new_spread_df['home'] = new_spread_df.opp.apply(lambda x: 1 if 'vs' in x else 0)
#go back and change the -999 to 0.0
new_spread_df.ats.apply(lambda x: 0 if x == 'L' else (1 if x =='W' else -999))

new_spread_df.spread = new_spread_df.spread.apply(lambda x: 0.0 if x == ' Ev' else x)
new_spread_df.spread = new_spread_df.spread.apply(lambda x:float(x) if x != '' else -999.0)
new_spread_df.total = new_spread_df.total.apply(lambda x: float(x) if x != '' else -999.0)
new = df[df.gametype=='REG'].copy()
new.score = new.score.apply(lambda x: x[1:].split('-')).apply(lambda x: [float(i) for i in x])
new['gametotal'] = new.score.copy()
new.gametotal = new.gametotal.apply(lambda x: sum(x)) 
new['ouDelta'] = new.gametotal - new.total
new['score_diff'] = new.score.copy()
new.score_diff = new.score_diff.apply(lambda x: x[0] - x[1])
new.ats = new.ats.apply(lambda x: 0 if x=='L' else 1)
new.result = new.result.apply(lambda x: 0 if x == "L" else 1)
#this still includes post season games
#at this iteration it is team,year,g,date,opp,gametype,results,score,ats,spread,ou,total,home





















def spread_transform(df):
    #changes date column to datetime format YYYY-MM-DD
    df['date'] = df.date.apply(lambda x: pd.to_datetime(x))

    #makes column with lists of last 5 days
    df['dt_list'] = df.date.apply(lambda x: [x - datetime.timedelta(days=d) for d in range(0,5)])

    #create column for number of games played in past 5 days by team including current date/game
    df['team_last_5'] = df.apply(lambda x:len(df.loc[df.date.isin(x['dt_list']) & (df['team']==x['team'])]),axis=1)
    
    #create column for number of games played in past 5 days by opponent including current date/game
    df['opp_last_5'] = df.apply(lambda x:len(df.loc[df.date.isin(x['dt_list']) & (df['team']==x['opp'])]),axis=1)

    #create column for back to back dates and column for team_b2b (yes = 1, no = 0)
    df['b2b_list'] = df.date.apply(lambda x: [x - datetime.timedelta(days=d) for d in range(0,2)])
    df['team_b2b'] = df.apply(lambda x:len(df.loc[df.date.isin(x['b2b_list']) & (df['team']==x['team'])])-1,axis=1)
    df['opp_b2b'] = df.apply(lambda x:len(df.loc[df.date.isin(x['b2b_list']) & (df['team']==x['opp'])])-1,axis=1)
    df['s_double'] = df.spread.apply(labda x: 1 if x >= 10 else(1 if x <= -10 else 0))

    return df.drop(columns=['b2b_list','dt_list'],axis=1)

    
def spread_expander(spread_df):
    spread = copy.deepcopy(spread_df[(spread_df.team==team)&(spread_df.year==year)])
    spread.index = range(len(spread))
    ats_record = np.insert((np.cumsum(spread.ats.values[:81]))/range(1,82),0,0.0)
    spread['ats_record'] = ats_record
    spread_dup = copy.deepcopy(spread)
    for i in range(len(spread)):
        team = team
        opp = spread.opp.loc[i]
        if spread.home[i] == 0:
            spread_dup.loc[i,'team'] = opp
            spread_dup.loc[i,'opp'] = team
    columns = spread_dup.columns.values
    columns[0] = 'home'
    spread_dup.columns = columns
    spread_dup_dum = pd.get_dummies(spread_dup[['home','opp']])
    
    return pd.concat([spread_dup[['spread','ats_record']],spread_dup_dum.drop(columns='home',axis=1)],axis=1)