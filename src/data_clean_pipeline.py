import pandas as pd 
import numpy as np 
import pickle
import copy
import time
import requests
from bs4 import BeautifulSoup

'''
This pipeline at it's completion should take an input of just teams as a list of strings and years as a list of strings
and transform the data to a working usable for modeling
'''

class Pipeline():
    
    def __init__(self):
