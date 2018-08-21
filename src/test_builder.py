from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

#need pickled spread_df, team_avg

def prediction_calculator_with_build(X_train,y_train,X_test,y_test,spread_df,team_avg):
    '''
    Takes X_train,y_train, X_test,y_test data and tests tests initially and refits after each test
    '''
    X_train_copy = copy.deepcopy(X_train)
    y_train_copy = copy.deepcopy(y_train)
    X_test_copy = copy.deepcopy(X_test)
    y_test_copy = copy.deepcopy(y_test)
    
    lr = LogisticRegression()
    lr.fit(X_train_copy,y_train_copy)
    X_test_copy.index = range(len(X_test_copy))
    first_predictions = lr.predict(X_test_copy)
    first_score = lr.score(X_test_copy,y_test_copy)
    #first prediction should be the same
    update_model_pred = []
    for i in range(len(X_test_copy)):
        lr.fit(X_train_copy,y_train_copy)
        X_X = pd.DataFrame(X_test_copy.iloc[i]).T
        X_pred = lr.predict(X_X)
        update_model_pred.append(float(X_pred))
        y_train_copy = np.insert(np.array(y_train_copy),len(y_train_copy),y_test_copy[i])
        X_train_copy = pd.concat([X_train_copy,X_X],axis=0)
    
    final_pred = np.array(update_model_pred)
    final_score = accuracy_score(y_test,final_pred)
    return update_model_pred, first_score, final_score