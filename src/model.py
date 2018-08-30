import pandas as pd
import numpy as np
import pickle
import copy
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier


class SpreadPredict():
    '''
    builds regression model and returns prediction
    '''
    def __init__(self,model='logistic'):
        if model in ['logistic','randomforest','gradientboosting']:
            if model == 'logistic':
                self.model = LogisticRegression()
            if model == 'randomforst':
                self.model = RandomForestClassifier(n_estimators=500)
            if model == 'gradientboosting':
                self.model = GradientBoostingClassifier(n_estimators=500,learning_rate=.001)
        else:
            print('invalid model selected...Logistic Regression initialized')
            self.model = LogisticRegression()

