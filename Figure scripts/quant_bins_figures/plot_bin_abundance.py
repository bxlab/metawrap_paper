#!/usr/bin/env python


import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# load in library sizes:
libs={}
for line in open(sys.argv[1]):
	if line.startswith("#"): continue
	lib=line.strip().split("\t")[0]
	reads=int(line.strip().split("\t")[1])
	libs[lib] = reads
	

# load in abundannce table as pandas dataframe
z=pd.read_csv(sys.argv[2], sep='\t', index_col=0)
z.columns.name

# remove all 0 rows
z = z[(z.T != 0).any()]

# standardize abundance values by total number of reads in each sample
for column in z: z[column]=100000000*z[column]/libs[column]


# standardize rows by maximum value in each row
#z = z.div(z.max(axis=1), axis=0)

# log standardize:
z=z+0.0001
z = np.log(z)

# make heat map
sns.set(font_scale=1)
g = sns.clustermap(z, figsize=(10,10), col_cluster=True, cmap="RdBu_r")
plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, color='w')
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, color='w')


# add labels
plt.text(15, -5.6, "Samples", fontsize=26, ha="center", rotation='horizontal', verticalalignment='center')
plt.text(0, -2.75, "Bins", fontsize=26, ha="center", rotation='vertical', verticalalignment='center')
plt.text(15, 1.4, sys.argv[1].split("_")[0]+" bin abundances", fontsize=36, ha="center", rotation='horizontal', verticalalignment='center')
plt.text(3, 0.5, "-log10\nbin abund.", fontsize=16, ha="center", rotation='vertical', verticalalignment='center')
plt.subplots_adjust(left=0.05, right=0.98, bottom=0.10, top=0.90)


plt.savefig(sys.argv[3], format='eps', dpi=600)






