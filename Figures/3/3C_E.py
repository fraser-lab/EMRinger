from emringer import *
from libtbx import easy_pickle
from matplotlib import pyplot as plt
from sys import argv

numbers = [3,9,15,21] 
extension = "_ringer.pkl"

ringers = {i: easy_pickle.load("%d%s" % (i, extension)) for i in numbers}
x = range(0,365,5)
y ={}
for i in numbers:
	for index, value in enumerate(ringers[i]):
		if (1 in value._angles.keys()):
			if str(argv[1]) == str(value.chain_id):
				if int(argv[2]) == int(value.resid):
					y[i] = value._angles[1].densities + value._angles[1].densities[0:1]










fig, ax = plt.subplots(figsize = (4.8,3.6))
ax.set_xlim(0,360)
ax.set_xticks(range(0,390,60))
ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
ax.xaxis.set_ticks_position('bottom')
ax.set_ylabel("Map Value")
ax.set_xlabel("Chi1 Angle ($\degree$)")
for i in numbers:
	ax.plot(x, y[i], label = "Frames %d to %d" % (i-1, i+3))
fig.savefig("%s%s.png" % (str(argv[1]),str(argv[2])))
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#        	ncol=2, mode="expand", borderaxespad=0., fontsize="small")
# fig.savefig("Figures/%s_%d_legend.png" % (str(argv[1]), int(argv[2])))









