
# Use python3.6+

# Author: RA, 2019-06-08
# License: CC0 -- No rights reserved


import pandas as pd
import numpy as np
import os

from itertools import groupby

PARAM = {
	# Template table
	'template': "INPUT/20190608_tls_MFA_ALL_STATES.csv",

	# Fake table
	'fake': "OUTPUT/fakes/{name}-{n}.csv",

	# CSV file format
	'csv': {
		'sep': '\t',
		'decimal': ',',
	},

	# How many fakes to make
	'repeat': 10,

	# Same set of tables every time (preferred)
	'seed': 42,
}


# A discrete distribution on n outcomes
def random_distribution(n):
	v = np.random.rand(n)
	v = v / v.sum()
	return v


def fake_table1():
	# Template table
	df0 = pd.read_csv(PARAM['template'], **PARAM['csv'])

	# Groups of column names
	groups = [list(group) for (prefix, group) in groupby(df0.columns, key=(lambda x: x.split("_")[0]))]

	# Retain only groups of >= 2
	groups = [group for group in groups if (len(group) >= 2)]

	# print("Identified {n} groups.".format(n=len(groups)))
	# print("\n".join(str(group) for group in groups.values()))

	# Create a copy
	df = df0.copy()

	# Fill the copy with fake data
	def fake_row(row):
		for group in groups:
			row[group] = random_distribution(len(group))
		return row

	df = df.apply(fake_row, axis=1)

	return df


def fake_tables():
	# Seed for "random"
	if PARAM.get('seed') is not None:
		np.random.seed(PARAM['seed'])


	# The name of the template file without path and extension
	name = os.path.splitext(os.path.basename(PARAM['template']))[0]
	# Make output directories
	os.makedirs(os.path.dirname(PARAM['fake']), exist_ok=True)

	for n in range(PARAM['repeat']):
		# Output filename
		filename = PARAM['fake'].format(name=name, n=(1 + n))

		print("Making", filename)

		# Make another fake table
		df = fake_table1()
		df: pd.DataFrame

		# Save fake table
		df.to_csv(filename, **PARAM['csv'])


if __name__ == "__main__":
	fake_tables()
