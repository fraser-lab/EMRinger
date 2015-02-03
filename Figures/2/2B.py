#! /usr/bin/env phenix.python

from libtbx import easy_pickle
import matplotlib.pyplot as plt
from sys import argv

thresholds = easy_pickle.load("%s/thresholds.pkl" % argv[1])
sample_sizes = easy_pickle.load("%s/sample_sizes.pkl" % argv[1])
rotamer_ratios = easy_pickle.load("%s/rotamer_ratios.pkl" % argv[1])

fig,ax1=plt.subplots(figsize=(6.7,4.5))
ax1.set_xlabel("Map Value Threshold", labelpad=10)
ax1.set_ylabel("Peaks above Threshold", color="b", labelpad=10)
ax1.plot(thresholds, sample_sizes, label="Sample Sizes", color="b", alpha=0.7)
for tl in ax1.get_yticklabels():
	tl.set_color('b')
ax2 = ax1.twinx()
ax2.set_ylabel("Fraction Rotameric", color="r", labelpad=10)
ax2.set_ylim(0,1)
ax2.plot(thresholds, rotamer_ratios, label="Fraction Rotameric", color="r", alpha=0.7)
for tl in ax2.get_yticklabels():
	tl.set_color('r')
ax1.yaxis.grid()
ax1.xaxis.set_ticks_position('bottom')
fig.savefig("2B.png" % argv[1])



# for tl in ax2.get_yticklabels():
# 	tl.set_color('r')