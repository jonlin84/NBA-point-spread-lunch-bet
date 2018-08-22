from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

#need pickled spread_df, team_avg
#integrate a model selector as an input choice
#include optimizer??
def prediction_calculator_with_build(X_train,y_train,X_test,y_test,spread_df,team_avg):
    X_train_copy = copy.deepcopy(X_train)
    y_train_copy = copy.deepcopy(y_train)
    X_test_copy = copy.deepcopy(X_test)
    y_test_copy = copy.deepcopy(y_test)
    
    rf = RandomForestClassifier(n_estimators=500,n_jobs=-1,verbose=3)
    rf.fit(X_train_copy,y_train_copy)
    X_test_copy.index = range(len(X_test_copy))
    first_predictions = rf.predict(X_test_copy)
    first_score = rf.score(X_test_copy,y_test_copy)
    #first prediction should be the same
    update_model_pred = []
    for i in range(len(X_test_copy)):
        rf.fit(X_train_copy,y_train_copy)
        X_X = pd.DataFrame(X_test_copy.iloc[i]).T
        X_pred = rf.predict(X_X)
        update_model_pred.append(float(X_pred))
        y_train_copy = np.insert(np.array(y_train_copy),len(y_train_copy),y_test_copy[i])
        X_train_copy = pd.concat([X_train_copy,X_X],axis=0)

    final_pred = np.array(update_model_pred)
    final_score = accuracy_score(y_test,final_pred)
    
    return update_model_pred, first_predictions, first_score, final_score


def create_season_test_set(teams,year,team_avg,spread_df):
    x_df = pd.DataFrame()
    y_df = pd.DataFrame()
    for team in teams:
        x,y = spread_prediction_creator(team,year,team_avg,spread_df)
        x_df = pd.concat([x_df,x],axis=0)
        y_df = pd.concat([y_df,pd.DataFrame(y)],axis=0)
    X_test = x_df
    y_test = y_df.values.reshape(-1)
    X_test.index = (range(len(X_test)))
    return X_test, y_test

    def create_season_training_set(teams,year,team_avg,spread_df):
    x_df = pd.DataFrame()
    y_df = pd.DataFrame()
    for team in teams:
        x,y = box_score_grabber(box_2014,team,year,spread_df)
        x_df = pd.concat([x_df,x],axis=0)
        y_df = pd.concat([y_df,pd.DataFrame(y)],axis=0)
    X_train = x_df
    y_train = y_df.values.reshape(-1)
    X_train.index = (range(len(X_train)))
    return X_train, y_train