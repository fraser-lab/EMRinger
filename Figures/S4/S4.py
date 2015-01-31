#! /usr/bin/env python

import matplotlib.pyplot as plt

x = [3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0]
y = [2.968677, 3.143741, 2.906839, 2.510553, 1.684038, 1.373736, 1.357269, 1.721942, 1.803851, 1.256614, 0.353246, -0.075401, -0.199493, -0.207986, -0.628273, -0.100759, 0.056998, -0.003313, 0.403037, 0.871305]
fig,ax = plt.subplots()
ax.axhspan(-0.015,0.015,color='0.1',alpha=0.3, linewidth=0)
ax.plot(x,y, linewidth=3.0, alpha=0.7, color="#5DA5DA")
ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
ax.xaxis.set_ticks_position('bottom')
ax.set_ylim(-1,4)
ax.set_xlabel("Filtered Resolution ($\AA$)", labelpad=10)
ax.set_ylabel("EMRinger Score", labelpad=10)
fig.savefig('S4.png')