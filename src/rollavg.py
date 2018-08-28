
import copy
import datetime
import numpy as np 
import pandas as pd 
from collections import defaultdict


avg_list_no_pct = ['mp', 'fg', 'fga', 'fg3','fg3a', 'ft', 'fta', 'orb', 'drb', 'trb', 'ast',
       'stl', 'blk', 'tov', 'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg3', 'opp_fg3a', 'opp_ft', 'opp_fta', 'opp_orb', 'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl',
       'opp_blk', 'opp_tov', 'opp_pf', 'opp_pts']

avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5','avg_fg3a_last_5','avg_ft_last_5',
 'avg_fta_last_5','avg_orb_last_5',
'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5','avg_blk_last_5','avg_tov_last_5',
'avg_pf_last_5','avg_pts_last_5','avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5','avg_opp_fg3_last_5','avg_opp_fg3a_last_5',
'avg_opp_ft_last_5','avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5','avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5','avg_opp_blk_last_5','avg_opp_tov_last_5',
 'avg_opp_pf_last_5','avg_opp_pts_last_5']

teams    =    ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']


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
    
    #create column for games with double digit spreads
    df['s_double'] = df.spread.apply(lambda x: 1 if x >= 10 else(1 if x <= -10 else 0))
    df['s_less_3'] = df.spread.apply(lambda x: 1 if abs(x) < 3 else 0)
    df.index = range(len(df))
    return df.drop(columns=['b2b_list','dt_list'],axis=1)

def season_sampler(teams,year,spread_df,boxscore_df):
    avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                    'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                    'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                    'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                    'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                    'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                    'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                    'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                    'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5','avg_opp_pts_last_5']
    
    d = defaultdict(int)
    for team in teams:
        box_team = copy.deepcopy(boxscore_df[(boxscore_df.team==team)&(boxscore_df.year==year)])
        sp = copy.deepcopy(spread_df[(spread_df.team==team)& (spread_df.year==year)])
        box_team.index = range(len(box_team))
        sp.index = range(len(sp))
        sp.drop(columns=['team','year','g','date','result','opp','score','ou','total','score_diff','spread_diff'],inplace=True)
        ats_record = np.insert((np.cumsum(sp.ats.values[:81]))/range(1,82),0,0.0)
        sp['ats_record'] = ats_record
        roll_avg = copy.deepcopy(box_team[avg_list_no_pct].rolling(5, min_periods=1).mean())
        roll_avg.columns = avg_5_no_pct
        insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
        insertion.columns = avg_5_no_pct
        roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
        roll_avg.index = range(len(roll_avg))
        combined_df = pd.concat([sp,roll_avg],axis=1)
        d[team] = combined_df
        
    return d

#add function to change home to away


def season_sampler(teams,year,spread_df,boxscore_df):
    avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                    'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                    'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                    'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                    'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                    'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                    'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                    'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                    'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5','avg_opp_pts_last_5']
    
    d = defaultdict(int)
    for team in teams:
        box_team = copy.deepcopy(boxscore_df[(boxscore_df.team==team)&(boxscore_df.year==year)])
        sp = copy.deepcopy(spread_df[(spread_df.team==team)& (spread_df.year==year)])
        box_team.index = range(len(box_team))
        sp.index = range(len(sp))
        sp.drop(columns=['team','year','g','date','result','opp','score','ou','total','score_diff','spread_diff'],inplace=True)
        ats_record = np.insert((np.cumsum(sp.ats.values[:81]))/range(1,82),0,0.0)
        sp['ats_record'] = ats_record
        roll_avg = copy.deepcopy(box_team[avg_list_no_pct].rolling(5, min_periods=1).mean())
        roll_avg.columns = avg_5_no_pct
        insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
        insertion.columns = avg_5_no_pct
        roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
        roll_avg.index = range(len(roll_avg))
        combined_df = pd.concat([sp,roll_avg],axis=1)
        d[team] = combined_df
        
    return d

    s_team = copy.deepcopy(df[(df.t==team) & (df.year==year)])
    s_opp = copy.deepcopy(df[(df.opp==opp) & (df.year==year)])
    fg_fg3_ft     =  ['fg','fg3','ft','opp_fg','opp_fg3','opp_ft']
    avg_5_fg_fg3_ft =  ['avg_fg_last_5','avg_fg3_last_5','avg_ft_last_5',
                    'avg_opp_fg_last_5','avg_opp_fg3_last_5','avg_opp_ft_last_5']
    s_team.index = range(len(s_team))
    box_team = copy.deepcopy(df[(df.team==team)&(df.year==year)])
    box_team.index = range(len(box_team))
    roll_avg = copy.deepcopy(box_team[fg_fg3_ft].rolling(5, min_periods=1).mean())
    roll_avg.columns = avg_5_fg_fg3_ft
    insertion = pd.DataFrame(np.zeros(len(fg_fg3_ft))).T
    insertion.columns = avg_5_fg_fg3_ft
    roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
    roll_avg.index = range(len(roll_avg))



def single_game_