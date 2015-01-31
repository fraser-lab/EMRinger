import matplotlib.pyplot as plt
from libtbx import easy_pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", dest="folder_a", help='Folder name for unrefined')
parser.add_argument("-b", dest="folder_b", help='Folder name for refined (Transmembrane)')
parser.add_argument("-c", dest="folder_c", help='Folder name for refined')
args = parser.parse_args()

y_a = easy_pickle.load('%s/emringer_scores.pkl' % args.folder_a)
y_b = easy_pickle.load('%s/emringer_scores.pkl' % args.folder_b)
y_c = easy_pickle.load('%s/emringer_scores.pkl' % args.folder_c)

x_a = easy_pickle.load('%s/thresholds.pkl' % args.folder_a)
x_b = easy_pickle.load('%s/thresholds.pkl' % args.folder_b)
x_c = easy_pickle.load('%s/thresholds.pkl' % args.folder_c)


# for i in range(len(y_a)):
#   if y_b[i] > 0:
#     x_a=x_a[i:]
#     x_b=x_b[i:]
#     y_a=y_a[i:]
#     y_b=y_b[i:]
#     break




fig, ax = plt.subplots(figsize=(6,4.5))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_ylim(-1,4)
ax.set_xlabel('Map Value Threshold', labelpad=10)
ax.set_ylabel('EMRinger Score', labelpad=10)
ax.axhspan(-0.015,0.015,color='0.1',alpha=0.3, linewidth=0)
ax.plot(x_a,y_a,label="Unrefined", linewidth=3.0)
ax.plot(x_b,y_b,label="Unrefined (Transmembrane)", linewidth=3.0)
ax.plot(x_c,y_c,label="Refined (Transmembrane)", linewidth=3.0)
plt.legend(loc='upper right', fontsize="x-small")
fig.savefig('3B.png')