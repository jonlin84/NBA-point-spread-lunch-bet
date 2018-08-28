import pickle
import copy
%matplotlib inline

import os
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats

import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.statespace.sarimax import SARIMAX

#load organized labelled boxscore dataframe
box = pd.read_pickle('../CapstoneProject/final_clean_boxscores_2009_2018.pkl')

#load transformed sp dataframe (does not include recently modified features)
sp = pd.read_pickle('../CapstoneProject/spread_transformed.pkl')

def team_series(team,box_df):
    return copy.deepcopy(box_df[box.team==team])

def to_time_series(series):
    df = copy.deepcopy(series)
    df.index = pd.DatetimeIndex(freq='D',start=0,periods=len(df))
    return df

#takes timeseries dataset and returns forecast prediction
def make_predictions(data, order=(0,1,1), start=82):
    results = []
    start_idx = len(data) - start
    for i in range(start):
        model = ARIMA(data[:start_idx + i],order=order).fit()
        #houston_model.summary()
        results.append(model.forecast()[0] +  0.68 * model.predict()[-1])
        #results.append((data[start_idx + i - 1] + model.predict()[-1]))
        #print(model.predict()[start_idx])
        #print(model.predict(dynamic=True)[0])
        #print (model.forecast())
    return results

#this should really be for 1 instance, this functions returns value of next prediction
#as a combination of forecast which is the avg of all instances
def make_single_prediction(data,order=(0,1,1)):
    model = ARIMA(data,order).fit()
    return model.forecast()[0] + 0.68 * model.predict()[-1]

# take predicted columns FG, FG3, FGA
# avg with opp_fg of opponent at the indexed game for opponent (dataframe where team == opp, return index)
# take index of the rolling avg dataframe
# use FG, FG3, FGA averages to construct average points (find standard deviation to use as variance)
# for now use the sum of 3 variables (FG3*2, FG3,FT) for variance
#stats.normal.sf(total_diff - spread, total_avg, variance)
#that number is my prediction
#the machine learning is using time series to 'forecast' scores minimizing some of the error by taking the mean of the
#predicted score and the rollling 5 game average of the opponent


#RMSE was ~17, goal is ~10

def team_sampler(team,year,boxscore_df):
    fg_fg3_ft =  ['avg_fg_last_5','avg_fg3_last_5','avg_ft_last_5',
                    'avg_opp_fg_last_5','avg_opp_fg3_last_5','avg_opp_ft_last_5']
    
    d = defaultdict(int)
    for team in teams:
        box_team = copy.deepcopy(boxscore_df[(boxscore_df.team==team)&(boxscore_df.year==year)])
        box_team.index = range(len(box_team))
        roll_avg = copy.deepcopy(box_team[avg_list_no_pct].rolling(5, min_periods=1).mean())
        roll_avg.columns = avg_5_no_pct
        insertion = pd.DataFrame(np.zeros(len(avg_list_no_pct))).T
        insertion.columns = avg_5_no_pct
        roll_avg = pd.concat([insertion,roll_avg[:-1]],axis=0)
        roll_avg.index = range(len(roll_avg))
        combined_df = pd.concat([sp,roll_avg],axis=1)
        d[team] = combined_df
        
    return d

#team sampler work
def team_sampler(team,opp,year,df):
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
    return pd.concat([s_team,roll_avg],axis=1)

#I have combined dataframes spread and boxscore into a single pickled file called 
#THEBIGDATAFRAME (had to score boxscores and values by team then year)
        