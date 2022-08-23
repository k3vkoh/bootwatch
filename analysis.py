import pandas as pd 
from sqlalchemy import create_engine

import matplotlib
import matplotlib.pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FuncAnimation

import seaborn as sns

import os 

import numpy as np

engine = create_engine('sqlite:////Users/kevinkoh/Desktop/bootwatch/bootwatch.db')

cwd = os.getcwd()

directory = os.path.join(cwd, 'data')

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

brands_gif = os.path.join(cwd, 'brand_movement.gif')
brands_png = os.path.join(cwd, 'brand_movement.png')

fig = plt.figure(figsize=(7,5))
plt.style.use('seaborn-deep')

df = None

sql = """ 
		SELECT * FROM players
	"""

df = pd.read_sql(sql, engine)

brand_array = np.array(df['brand'])
brand_unique = np.unique(brand_array)

palette = list(reversed(sns.color_palette("Spectral", 100).as_hex()))

brands = {}

def init():
	plt.clf()

def animate(i):

	plt.clf()

	plt.ylabel('# of players')
	plt.ylabel('year')
	plt.title('Boot Brands Used by Top 100 Players (2015-2021)')

	for x in range(len(brand_unique)):
		if brand_unique[x] == 'None':
			continue
		temp = brands[brand_unique[x]][:i+1]
		plt.plot(range(len(temp)), temp, color = palette[x*10])
		plt.annotate(brand_unique[x], (len(temp)-1, temp[-1]))

	plt.xticks(np.arange(i+1), years[:i+1])

def get_data_brand(brand, year):

	sql = """ 
			SELECT * FROM players
			WHERE brand == '{}' and year == '{}'
		""".format(brand, year)

	return pd.read_sql(sql, engine)

def brand_comparison():

	global brands

	for x in years:
		year = str(x)
		for y in brand_unique:
			temp = get_data_brand(y, year)
			count = temp.shape[0]
			if y not in brands:
				brands[y] = [count]
			else:
				brands[y].append(count)

	ani = FuncAnimation(fig, animate, frames = len(years), interval = 1000, init_func = init, repeat = True)

	with open(brands_gif, 'wb') as gif:
		writergif = animation.PillowWriter(fps = 1)
		ani.save(gif, writer = writergif)

	plt.savefig(brands_png)

def analyze():
	brand_comparison()

if __name__ == '__main__':
	analyze()


