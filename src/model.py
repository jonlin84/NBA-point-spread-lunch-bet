import pandas as pd
import numpy as np
import pickle
import copy
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from finalized import create_team_avg_with_rolling
from finalized import season_df_compiler
from finalized import transform_test

drop_columns= [ 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
    'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
    'pf', 'pts', 'opp_mp', 'opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg3',
    'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_orb',
    'opp_drb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk', 'opp_tov','opp_pf',
    'opp_pts', 't', 'y', 'g', 'date', 'opp', 'result', 'score', 'ou', 'total', 
    'home', 'score_diff', 'spread_diff']


class SpreadPredict():
    '''
    builds regression model and returns prediction
    '''
    self.df = pd.read_pickle('../data/THEBIGDATAFRAME.pkl')
    def __init__(self):
        self.X_train = None
        self.y_train = None
        return self
    

    def _build_season_model(self,teams,year):
        '''
        creates model to make prediction
        '''
        #find optimally tuned learning rate,estimators
        #set large for small training set
        self.gbc = GradientBoostingClassifier(n_estimators=500,learning_rate=.33)

    def _get_team_data(self,teams,year):
        '''
        access dataframe to get team data
        '''

        df = copy.deepcopy(self.df[self.df.year==year])
        df.index = range(len(df))
        return df

    def _make_x_y(self,df,teams,year):
        '''
        return X and y
        '''
        
        data = copy.deepcopy(self._get_team_data(teams,year))
        data.drop(columns=drop_columns,inplace=True)
        X = data.drop(columns=['ats','team','year']).copy()
        y = data.ats
        return X,y

    def _make_X_train_y_train(self,teams,year):
        '''
        creates X_train,y_train
        '''
        self.X_train, self.y_train = self._make_x_y(self.df,teams,year)

    def _predict_probab(self,game):
        return self.gbc.predict_proba(game)
        