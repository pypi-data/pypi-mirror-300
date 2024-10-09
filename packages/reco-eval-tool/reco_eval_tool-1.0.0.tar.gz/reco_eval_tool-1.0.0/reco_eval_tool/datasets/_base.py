import os
from os import environ, listdir
from os.path import join

import pandas as pd


def load_file(file_path, sep=None):
	if sep is None:
		with open(file_path, 'r', encoding="utf8") as f:
			first_line = f.readline()
			if '\t' in first_line:
				sep = '\t'
			elif ',' in first_line:
				sep = ','
			else:
				raise ValueError('The file does not contain the valid separator')
	df = pd.read_csv(file_path, sep=sep)
	return df


def load_dir(dir_path, sep=None):
	file_paths = [join(dir_path, f) for f in listdir(dir_path)]
	df = pd.DataFrame()
	for file_path in file_paths:
		df = df.append(_load_file(file_path, sep))
	return df


def load_df(df):
	return df
