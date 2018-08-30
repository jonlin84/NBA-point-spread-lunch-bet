import pandas as pd
import numpy as np
import copy



#returns rolling average,with first game as average of last season
def current_get_rolling_avg(team,year,df,team_avg,rolling_avg=5):
    avg_list_no_pct = ['mp', 'fg', 'fga', 'fg3','fg3a', 'ft', 'fta', 'orb', 'drb', 'trb', 'ast',
       'stl', 'blk', 'tov', 'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg3', 'opp_fg3a', 'opp_ft', 'opp_fta', 'opp_orb', 'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl',
       'opp_blk', 'opp_tov', 'opp_pf', 'opp_pts']
    
    
    avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                    'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                    'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                    'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                    'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                    'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                    'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                    'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                    'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5','avg_opp_pts_last_5']
    
    sp = df[(df['team']==team) & (df['year']==year)].copy()
    ats_record = np.insert((np.cumsum(sp.ats.values[:81]))/range(1,82),0,0.0)
    sp['ats_record'] = ats_record
    sp.index= range(len(sp.index))
    roll_avg = sp[avg_list_no_pct].rolling(rolling_avg, min_periods=1).mean()
    roll_avg.columns = avg_5_no_pct
    insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
    #insertion.columns = avg_5_no_pct
    if int(year) > 2014:
        insertion = pd.DataFrame(data=team_avg[team][(str(int(year)-1))][0][avg_list_no_pct]).T
    else:
        insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
    insertion.columns = avg_5_no_pct
    roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
    roll_avg.index = range(len(roll_avg))
    team_df = df[(df.team==team) & (df.year==year)]
    team_df.index = range(len(team_df))
    return pd.concat([team_df,roll_avg,sp['ats_record']],axis=1)

def create_df_season(teams,year,box,team_avg,rolling_avg=5):
    final = pd.DataFrame()
    for team in teams:
        current = current_get_rolling_avg(team,year,box,team_avg,rolling_avg)
        final = pd.concat([final,current],axis=0)
    final.index = range(len(final))
    return final
#final pipeline has to take raw data from a feed for the current games
#transform and combine to spread_box data and then train
#return output

#---------------------------------#
#where I'm scrapping the data from is past website data, need to find the correct route grab relevant spread
#data from correct page and format it into a single X_predict line


def transform_spread(spread,teams,year,box,team_avg,rolling_avg=5):
    avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                    'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                    'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                    'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                    'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                    'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                    'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                    'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                    'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5','avg_opp_pts_last_5']
    avg_5_no_pct_diff = ['avg_mp_last_5_diff','avg_fg_last_5_diff','avg_fga_last_5_diff','avg_fg3_last_5_diff',
 'avg_fg3a_last_5_diff','avg_ft_last_5_diff','avg_fta_last_5_diff','avg_orb_last_5_diff','avg_drb_last_5_diff',
 'avg_trb_last_5_diff','avg_ast_last_5_diff','avg_stl_last_5_diff','avg_blk_last_5_diff','avg_tov_last_5_diff',
 'avg_pf_last_5_diff','avg_pts_last_5_diff','avg_opp_mp_last_5_diff','avg_opp_fg_last_5_diff',
 'avg_opp_fga_last_5_diff','avg_opp_fg3_last_5_diff','avg_opp_fg3a_last_5_diff','avg_opp_ft_last_5_diff',
 'avg_opp_fta_last_5_diff','avg_opp_orb_last_5_diff','avg_opp_drb_last_5_diff','avg_opp_trb_last_5_diff',
 'avg_opp_ast_last_5_diff','avg_opp_stl_last_5_diff','avg_opp_blk_last_5_diff','avg_opp_tov_last_5_diff',
 'avg_opp_pf_last_5_diff','avg_opp_pts_last_5_diff']
    spread = spread.copy()
    spread.index = range(len(spread))
    spread_final = pd.DataFrame()
    
    rolling_avg_season = create_df_season(teams,year,box,team_avg,rolling_avg=5)
    for i in range(len(spread)):
        gameid = spread.gameid[i]
        team = spread.team[i]
        opp = spread.opp[i]
        team_stat = rolling_avg_season.loc[(rolling_avg_season['gameid']==gameid) & (rolling_avg_season['team']==team)]
        opp_stat = rolling_avg_season.loc[(rolling_avg_season['gameid']==gameid)& (rolling_avg_season['team']==opp)]
        diff = team_stat[avg_5_no_pct] - opp_stat[avg_5_no_pct]
        diff.columns = avg_5_no_pct_diff
        spread_final = pd.concat([spread_final,diff],axis=0)
    spread_final.index=range(len(spread_final))

    return pd.concat([spread,spread_final],axis=1)

drop_columns = ['team', 'year', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
       'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
       'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg3',
       'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_orb',
       'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov',
       'opp_pf', 'opp_pts', 't', 'y', 'g', 'date', 'opp', 'result', 'score', 'ou', 'total','score_diff', 'spread_diff', 'gameid', 'game_id']


def create_model_data(trans_df):
    '''
    returns X,y
    '''
    drop_columns = ['team', 'home','year', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
       'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
       'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg3',
       'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_orb',
       'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov',
       'opp_pf', 'opp_pts', 't', 'y', 'g', 'date', 'opp', 'result', 'score', 'ou', 'total','score_diff', 'spread_diff', 'gameid', 'game_id']
    X = trans_df.drop(columns=drop_columns)
    y = trans_df.ats
    return X.drop(columns='ats'), y 