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

fig = plt.figure(figsize=(7,5))
ax = plt.subplot(111)

plt.style.use('seaborn-deep')

df = None

sql = """ 
		SELECT * FROM players
	"""

df = pd.read_sql(sql, engine)

brand_array = np.array(df['brand'])
brand_unique = np.unique(brand_array)

palette = list(reversed(sns.color_palette("Spectral", len(brand_unique)).as_hex()))

brands = {}

def init():
	ax.clear()
	box = ax.get_position()
	ax.set_position([box.x0 + .04, box.y0, box.width, box.height])

def animate(i):

	y0 = brands['Nike'][i]
	y1 = brands['Adidas'][i]
	y2 = brands['Puma'][i]
	y3 = brands['New Balance'][i]
	y4 = brands['Mizuno'][i]
	y5 = brands['Under Armour'][i]
	y6 = brands['Umbro'][i]
	y7 = brands['Asics'][i]
	y8 = brands['None'][i]

	ax.set_title('Top 100 Players Endorsements {}'.format(years[i]))

	ax.barh(range(9), sorted([y0,y1,y2,y3,y4,y5,y6,y7,y8]), color=palette)

	sorted_brands = sorted(brands.items(), key = lambda x: x[1])
	tcks = [i[0] for i in sorted_brands]

	plt.yticks(range(9), tcks)

	plt.savefig(os.path.join(cwd, 'brands_{}.png'.format(years[i])))

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
		writergif = animation.PillowWriter(fps = 3)
		ani.save(gif, writer = writergif)

def analyze():
	brand_comparison()

if __name__ == '__main__':
	analyze()


