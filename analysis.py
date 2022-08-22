import pandas as pd 
from sqlalchemy import create_engine

import matplotlib
import matplotlib.pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FuncAnimation

import seaborn as sns

import os 

engine = create_engine('sqlite:////Users/kevinkoh/Desktop/bootwatch/bootwatch.db')

cwd = os.getcwd()

directory = os.path.join(cwd, 'data')

def get_data():

	years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

	sql = """ 
			SELECT * FROM players
		"""

	df = pd.read_sql(sql, engine)

	return df

