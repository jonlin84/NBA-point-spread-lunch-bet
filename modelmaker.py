import copy
import pandas as pd
import numpy as np
import pickle




class SpreadModel(object):
    '''
    creates model with specified inputs
    '''
    def __init__(self):
        
        
        self.box_df = pd.read_pickle('data/THEBIGDATAFRAME.pkl')
        self.team_avg = pd.read_pickle('data/team_avg.pkl')
        self.current_season = '2018'
        self.teams = ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL',
                      'MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL', 'PHI','PHO','POR','SAC','SAS',
                      'TOR','UTA','WAS']

        self.avg_list_no_pct = ['mp', 'fg', 'fga', 'fg3','fg3a', 'ft', 'fta', 'orb', 'drb', 'trb', 'ast',
                                'stl', 'blk', 'tov', 'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg3', 
                                'opp_fg3a', 'opp_ft', 'opp_fta', 'opp_orb', 'opp_drb', 'opp_trb', 'opp_ast', 
                                'opp_stl','opp_blk', 'opp_tov', 'opp_pf', 'opp_pts']
        
        self.avg_5_no_pct = ['avg_mp_last_5','avg_fg_last_5','avg_fga_last_5','avg_fg3_last_5',
                            'avg_fg3a_last_5','avg_ft_last_5','avg_fta_last_5','avg_orb_last_5',
                            'avg_drb_last_5','avg_trb_last_5','avg_ast_last_5','avg_stl_last_5',
                            'avg_blk_last_5','avg_tov_last_5','avg_pf_last_5','avg_pts_last_5',
                            'avg_opp_mp_last_5','avg_opp_fg_last_5','avg_opp_fga_last_5',
                            'avg_opp_fg3_last_5','avg_opp_fg3a_last_5','avg_opp_ft_last_5',
                            'avg_opp_fta_last_5','avg_opp_orb_last_5','avg_opp_drb_last_5',
                            'avg_opp_trb_last_5','avg_opp_ast_last_5','avg_opp_stl_last_5',
                            'avg_opp_blk_last_5','avg_opp_tov_last_5','avg_opp_pf_last_5',
                            'avg_opp_pts_last_5']


        self.avg_5_no_pct_diff = ['team_mp_last_avg_diff','team_fg_last_avg_diff','team_fga_last_avg_diff',
                        'team_fg3_last_avg_diff','team_fg3a_last_avg_diff','team_ft_last_avg_diff',
                        'team_fta_last_avg_diff','team_orb_last_avg_diff','team_drb_last_avg_diff',
                        'team_trb_last_avg_diff','team_ast_last_avg_diff','team_stl_last_avg_diff',
                        'team_blk_last_avg_diff','team_tov_last_avg_diff','team_pf_last_avg_diff',
                        'team_pts_last_avg_diff','opp_mp_last_avg_diff','opp_fg_last_avg_diff',
                        'opp_fga_last_avg_diff','opp_fg3_last_avg_diff','opp_fg3a_last_avg_diff',
                        'opp_ft_last_avg_diff','opp_fta_last_avg_diff','opp_orb_last_avg_diff',
                        'opp_drb_last_avg_diff','opp_trb_last_avg_diff','opp_ast_last_avg_diff',
                        'opp_stl_last_avg_diff','opp_blk_last_avg_diff','opp_tov_last_avg_diff',
                        'opp_pf_last_avg_diff','opp_pts_last_avg_diff']

        self.drop_columns = ['team','home', 'year', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
                        'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
                        'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg3',
                        'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_orb',
                        'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov','opp_pf', 
                        'opp_pts', 't', 'y', 'date', 'opp', 'result', 'score', 'ou', 'total','score_diff', 
                        'spread_diff', 'game_id','gameid','s_double','s_less_3']
    

    def _create_df_season(self,year,rolling_avg):
        final = pd.DataFrame()
        for team in self.teams:
            current = self._current_get_rolling_avg(team,year,rolling_avg)
            final = pd.concat([final,current],axis=0)
        final.index = range(len(final))
        return final

    



    def _current_get_rolling_avg(self,team,year,rolling_avg):
        '''
        return rolling_avg with selected previous games back and also at_the_spread record (ats_record)
        column
        '''
        
        box_df = pd.read_pickle('data/THEBIGDATAFRAME.pkl')
        sp = box_df[(box_df['team']==team) & (box_df['year']==year)].copy()
        sp.sort_values('g',inplace=True)
        ats_record = np.insert((np.cumsum(sp.ats.values[:len(sp)-1]))/range(1,len(sp)),0,0.0)
        sp['ats_record'] = ats_record
        sp.index= range(len(sp))
        roll_avg = sp[self.avg_list_no_pct].rolling(rolling_avg, min_periods=1).mean()
        roll_avg.columns = self.avg_5_no_pct
        if int(year) > 2014:
            insertion = pd.DataFrame(data=self.team_avg[team][(str(int(year)-1))][0][self.avg_list_no_pct]).T
        else:
            insertion = pd.DataFrame(np.zeros(len(self.avg_list_no_pct))).T
        insertion.columns = self.avg_5_no_pct
        roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
        roll_avg.index = range(len(roll_avg))
        team_df = box_df[(box_df['team']==team) & (box_df['year']==year)].copy()
        team_df.sort_values('g',inplace=True)
        team_df.index = range(len(team_df))
        return pd.concat([team_df,roll_avg,sp['ats_record']],axis=1)

    def _transform_spread(self,year,rolling_avg,without_first_games,spread_home_team):
        '''
        transforms dataframe:
            e.x. spread_home_team = True, year='2014', rolling_avg = 5
            returns df using 2014 team rolling averages of 5 days columns joined to spread data for
            home team 
        '''
        if spread_home_team == True:
            spread_df = pd.read_pickle('data/home_spread.pkl')
        else:
            spread_df = pd.read_pickle('data/away_spread.pkl')

        spread = spread_df[spread_df['year']==year].copy()
        spread.index = range(len(spread))
        spread_final = pd.DataFrame()
    
        rolling_avg_season = self._create_df_season(year,rolling_avg)
        for i in range(len(spread)):
            gameid = spread['game_id'][i]
            team = spread['team'][i]
            opp = spread['opp'][i]
            team_stat = rolling_avg_season[(rolling_avg_season['game_id']==gameid) & (rolling_avg_season['team']==team)].copy()
            opp_stat = rolling_avg_season[(rolling_avg_season['game_id']==gameid)& (rolling_avg_season['team']==opp)].copy()
            opp_stats =opp_stat[self.avg_5_no_pct]
            home_stats = team_stat[self.avg_5_no_pct]
            h_off = (home_stats.values[0][:16] + opp_stats.values[0][16:]) / 2
            o_off = (opp_stats.values[0][:16] + home_stats.values[0][16:]) / 2  
            diff = pd.concat([pd.DataFrame(h_off).T,pd.DataFrame(o_off).T],axis=1)
            diff.columns = self.avg_5_no_pct_diff
            diff['team_ats'] = team_stat['ats_record'].values
            diff['opp_ats'] = opp_stat['ats_record'].values
            
            spread_final = pd.concat([spread_final,diff],axis=0)
        spread_final.index=range(len(spread_final))

        return pd.concat([spread,spread_final],axis=1)
    
    def create_model_data(self,year='2014',rolling_avg=5,without_first_games=True,home_spread_team=True):
        '''
        returns transformed dataframe with X,y with or without first games
        '''
        df = self._transform_spread(year,rolling_avg,without_first_games,home_spread_team)
        X = df.drop(columns=self.drop_columns)
        y = df[['ats','g']]
        if without_first_games:
            return X[X.g > 1].drop(columns=['ats']), y[y.g > 1].drop(columns='g')
        else:
            return X.drop(columns=['ats']), y.drop(columns='g') 


    def matchup_predict_data(self,home:str,away:str,spread:float):
        '''
        Takes home team, away team as 3 letter string, spread as float
        returns transformed dataframe for predicting
        '''
        home_rolling = self._current_get_rolling_avg(home,self.current_season ,6)
        away_rolling = self._current_get_rolling_avg(away,self.current_season ,6)
        home_data = home_rolling.iloc[len(away_rolling)-1].copy()
        away_data = away_rolling.iloc[len(away_rolling)-1].copy()
        away_stats = away_data[self.avg_5_no_pct].copy()
        home_stats = home_data[self.avg_5_no_pct].copy()
        h_off = (home_stats[:16].values + away_stats[16:].values) / 2
        o_off = (away_stats[:16].values + home_stats[16:].values) / 2  
        diff = pd.concat([pd.DataFrame(h_off).T,pd.DataFrame(o_off).T],axis=1)
        diff.columns = self.avg_5_no_pct_diff
        diff['team_ats'] = home_data['ats_record']
        diff['opp_ats'] = away_data['ats_record']
        g = home_data['g']        
        if g == 82:
            g = 1
        else:
            g = g + 1

        team_5 = home_data['team_last_5']
        opp_5 = away_data['team_last_5']
        team_b2b = home_data['team_b2b']
        opp_b2b = away_data['team_b2b']
        data = {'g':[g],'spread':[spread],'team_last_5':[team_5],'opp_last_5':[opp_5],'team_b2b':[team_b2b],'opp_b2b':[opp_b2b]}
        df = pd.DataFrame(data=data)
        return pd.concat([df,diff],axis=1)
    

    
    