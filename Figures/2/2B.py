#! /usr/bin/env phenix.python

from libtbx import easy_pickle
import matplotlib.pyplot as plt
import matplotlib
from sys import argv

thresholds = easy_pickle.load("%s/thresholds.pkl" % argv[1])
print thresholds
peak_counts = easy_pickle.load("%s/peak_counts.pkl" % argv[1])
print sum(peak_counts[thresholds[0]])
sample_sizes = [sum(peak_counts[i]) for i in thresholds]
rotamer_ratios = easy_pickle.load("%s/rotamer_ratios.pkl" % argv[1])

fig,ax1=plt.subplots(figsize=(6.7,4.5))
ax1.set_xlabel("Map value cutoff", labelpad=10)
ax1.set_ylabel("Peaks above cutoff", labelpad=10)
# ln1 = ax1.plot(thresholds, sample_sizes, label="Peaks above threshold", color="#4683C1", alpha=0.7)
ln1 = ax1.plot(thresholds, sample_sizes, label="Peaks above cutoff", color="#781C81", alpha=0.7)
# for tl in ax1.get_yticklabels():
# 	tl.set_color('b')
ax2 = ax1.twinx()
ax2.set_ylabel("Fraction rotameric", labelpad=10)
ax2.set_ylim(0,1)
ln2 = ax2.plot(thresholds, rotamer_ratios, label="Fraction rotameric",color="#D92120", alpha=0.7)
# for tl in ax2.get_yticklabels():
# 	tl.set_color('r')
# ax1.yaxis.grid()
ax1.xaxis.set_ticks_position('bottom')
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax1.get_xaxis().tick_bottom()
# ax.get_yaxis().tick_left()
# ax1.get_xaxis().set_major_formatter(
#   matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax1.get_yaxis().set_major_formatter(
  matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

lns = ln1+ln2
labs = [l.get_label() for l in lns]
leg = ax1.legend(lns, labs, loc='lower left', fontsize=13, borderpad=0)
leg.get_frame().set_linewidth(0.0)
fig.savefig("2B.png")



# for tl in ax2.get_yticklabels():
# 	tl.set_color('r')