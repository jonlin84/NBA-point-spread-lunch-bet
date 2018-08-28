import pandas as pd
import numpy as np
import copy



#takes pickled df with spread and boxscore information sorted by team/year



def create_team_avg_with_rolling(df,team,year):
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
    
    sp = copy.deepcopy(df[(df.team==team) & (df.year==year)])
    ats_record = np.insert((np.cumsum(sp.ats.values[:81]))/range(1,82),0,0.0)
    sp['ats_record'] = ats_record
    sp.index= range(len(sp.index))
    roll_avg = copy.deepcopy(sp[avg_list_no_pct].rolling(5, min_periods=1).mean())
    roll_avg.columns = avg_5_no_pct
    insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
    insertion.columns = avg_5_no_pct
    roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
    roll_avg.index = range(len(roll_avg))
    team_df = copy.deepcopy(df[(df.team==team) & (df.year==year)])
    team_df.index = range(len(team_df))
    return pd.concat([team_df,sp['ats'],roll_avg],axis=1)

def season_df_compiler(df,teams,year):
    final = pd.DataFrame()
    for team in teams:
        final = pd.concat([final,create_team_avg_with_rolling(df,team,year)])
    final.index = range(len(final))
    return final

def transform_test(df,teams):
    container = pd.DataFrame()
    counter = 0
    avg_5_no_pct =  ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                    'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                    'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                    'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                    'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                    'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                    'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                    'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                    'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5','avg_opp_pts_last_5']
    for team in teams:
        team1 = copy.deepcopy(df[df.team==team])
        team1.index = range(len(team1))
        for i in range(len(team1)):
            avg_5_diff =['avg_mp_last_5_diff','avg_fg_last_5_diff','avg_fga_last_5_diff','avg_fg3_last_5_diff',
 'avg_fg3a_last_5_diff','avg_ft_last_5_diff','avg_fta_last_5_diff','avg_orb_last_5_diff','avg_drb_last_5_diff',
 'avg_trb_last_5_diff','avg_ast_last_5_diff','avg_stl_last_5_diff','avg_blk_last_5_diff','avg_tov_last_5_diff',
 'avg_pf_last_5_diff','avg_pts_last_5_diff','avg_opp_mp_last_5_diff','avg_opp_fg_last_5_diff','avg_opp_fga_last_5_diff',
 'avg_opp_fg3_last_5_diff','avg_opp_fg3a_last_5_diff','avg_opp_ft_last_5_diff','avg_opp_fta_last_5_diff','avg_opp_orb_last_5_diff',
 'avg_opp_drb_last_5_diff','avg_opp_trb_last_5_diff','avg_opp_ast_last_5_diff','avg_opp_stl_last_5_diff',
 'avg_opp_blk_last_5_diff','avg_opp_tov_last_5_diff','avg_opp_pf_last_5_diff','avg_opp_pts_last_5_diff']
            opp = team1.opp[i]
            team2 = copy.deepcopy(df[df.team==opp])
            team2.index=range(len(team2))
            team1_line = copy.deepcopy(team1[(team1.date.iloc[i] == team2.date) & (team==team2.opp)])
            team2_line = copy.deepcopy(team2[(team2.date == team1.date.iloc[i]) & (team==team2.opp)])
            team1_stats = copy.deepcopy(team1_line[avg_5_no_pct])
            team2_stats = copy.deepcopy(team2_line[avg_5_no_pct])
            team1_stats.columns = range(len(team1_stats.columns))
            team2_stats.columns = range(len(team2_stats.columns))
            team3 = team1_stats - team2_stats
            team3.columns = avg_5_diff
            container = pd.concat([container,team3],axis=0)
    container.index=range(len(container))
    return container


avg_5_no_pct_diff = ['avg_mp_last_5_diff',
 'avg_fg_last_5_diff',
 'avg_fga_last_5_diff',
 'avg_fg3_last_5_diff',
 'avg_fg3a_last_5_diff',
 'avg_ft_last_5_diff',
 'avg_fta_last_5_diff',
 'avg_orb_last_5_diff',
 'avg_drb_last_5_diff',
 'avg_trb_last_5_diff',
 'avg_ast_last_5_diff',
 'avg_stl_last_5_diff',
 'avg_blk_last_5_diff',
 'avg_tov_last_5_diff',
 'avg_pf_last_5_diff',
 'avg_pts_last_5_diff',
 'avg_opp_mp_last_5_diff',
 'avg_opp_fg_last_5_diff',
 'avg_opp_fga_last_5_diff',
 'avg_opp_fg3_last_5_diff',
 'avg_opp_fg3a_last_5_diff',
 'avg_opp_ft_last_5_diff',
 'avg_opp_fta_last_5_diff',
 'avg_opp_orb_last_5_diff',
 'avg_opp_drb_last_5_diff',
 'avg_opp_trb_last_5_diff',
 'avg_opp_ast_last_5_diff',
 'avg_opp_stl_last_5_diff',
 'avg_opp_blk_last_5_diff',
 'avg_opp_tov_last_5_diff',
 'avg_opp_pf_last_5_diff',
 'avg_opp_pts_last_5_diff']

drop_columns= [ 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
       'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
       'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg3',
       'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_orb',
       'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov',
       'opp_pf', 'opp_pts', 't', 'y', 'g', 'date', 'opp', 'result', 'score', 'ou', 'total', 'home', 'score_diff', 'spread_diff']