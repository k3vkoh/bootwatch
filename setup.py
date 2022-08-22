import pandas as pd 
from sqlalchemy import create_engine

import os

engine = create_engine('sqlite:////Users/kevinkoh/Desktop/bootwatch/bootwatch.db')

cwd = os.getcwd()

directory = os.path.join(cwd, 'data')

def import_files():

	players_df = pd.DataFrame()

	for filename in os.scandir(directory):
		if filename.is_file() and '.DS_Store' not in filename.path:
			temp = pd.read_excel(filename.path)
			df = temp.copy()
			df = df[:100]
			table_name = filename.name.split('.')[0]
			year = '20' + table_name.split('_')[1]
			df['year'] = year
			players_df = pd.concat([players_df, df])
	
	players_df.to_sql('players', engine, if_exists = 'replace', index = False)

if __name__ == '__main__':
	import_files()