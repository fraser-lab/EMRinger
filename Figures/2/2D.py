#! /usr/bin/env python

import pandas
import matplotlib.pyplot as plt
import numpy as np

table = pandas.read_csv("EMDB_table.csv")

resolutions = table['Resolution']
scores = table['EMRinger Score']
# ids = table['EMDB ID']
# colors = table['Color']

z = np.polyfit(resolutions,scores,1)
fn = np.poly1d(z)

fig, ax = plt.subplots(figsize=(6,4.5))
ax.set_xlabel("Resolution ($\AA$)", labelpad=10)
ax.set_ylabel("EMRinger score", labelpad=10)
ax.set_xlim(3.0,5.2)
ax.set_ylim(-1,4)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
x=np.arange(3,5.5,0.1)
ax.axhspan(-0.015,0.015,color='0.1',alpha=0.3, linewidth=0)
ax.plot(x, fn(x), '--', color="#5DA5DA", alpha=0.7)
for _,row in table.iterrows():
	# This is just the annotations I am moving around!
	ax.plot(row['Resolution'],row['EMRinger Score'],marker='.', color=row['Color'])
	if row['EMDB ID'] not in [5160,5995,2787,2364, 5778, 5645]:
		ax.annotate(row['EMDB ID'], xy=(row['Resolution'],row['EMRinger Score']), size="xx-small", xytext=(4,0), textcoords='offset points')
	elif row['EMDB ID'] in [5160, 5995,5778]:
		ax.annotate(row['EMDB ID'], xy=(row['Resolution'],row['EMRinger Score']), size="xx-small", xytext=(-4,0), ha="right", textcoords='offset points')
	elif row['EMDB ID'] in [2364, 2787, 5645]:
		ax.annotate(row['EMDB ID'], xy=(row['Resolution'],row['EMRinger Score']), size="xx-small", xytext=(4,-6), textcoords='offset points')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
ax.xaxis.set_ticks_position('bottom')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
fig.savefig('2D.png')