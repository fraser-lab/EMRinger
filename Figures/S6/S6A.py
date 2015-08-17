#! /usr/bin/env python

import matplotlib.pyplot as plt


folders = [84, 131, 300, 422, 651, 857, 1381, 1438, 1444, 1607]
trajectories = {}

for i in folders:
	trajectories[i] = [0.62]+[float(j) for j in open("3A/%d/scores.txt" % i).readlines()]

fig,ax = plt.subplots(figsize=(6,4.5))
ax.axhspan(-0.015,0.015,color='0.1',alpha=0.3, linewidth=0)
ax.set_ylim(-1,4)
ax.set_xticklabels(["Initial","1","2","3","4","5","Final"], range(7))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xlabel("Stage of Refinement", labelpad=10)
ax.set_ylabel("EMRinger Score", labelpad=10)
for key, value in trajectories.iteritems():
	if key == 300:
		ax.plot(range(7), value, color="#60BD68", linewidth=3.0)
	else:
		ax.plot(range(7), value, color="#60BD68", linewidth=3.0, alpha=0.3)
fig.savefig("3A.png")