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
def make_predictions(data, order=(0,1,1), start=82, factor=1.0):
    results = []
    start_idx = len(data) - start
    for i in range(start):
        model = ARIMA(data[:start_idx + i],order=order).fit()
        #houston_model.summary()
        results.append(model.forecast()[0] + factor * 0.68 * model.predict()[-1])
        #results.append((data[start_idx + i - 1] + model.predict()[-1]))
        #print(model.predict()[start_idx])
        #print(model.predict(dynamic=True)[0])
        #print (model.forecast())
    return results

#this should really be for 1 instance, this functions returns value of next prediction
#as a combination of forecast which is the avg of all instances
def make_single_prediction(data,order=(0,1,1)):
    model = ARIMA(data,order).fit()
    return model.forecast()[0] + model.predict()[-1]