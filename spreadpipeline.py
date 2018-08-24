import datetime
import pandas as pd

teams    =    ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
#this function is to be run on pickled spread df (which has already been cleaned up to some degree)
#current runtime approximately 3 minutes on 12300 rows

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
    df['s_double'] = df.spread.apply(lambda x: 1 if x >= 10 else(1 if x <= -10 else 0))

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