#! /usr/bin/env phenix.python

from libtbx import easy_pickle
import argparse
from emringer import *
from matplotlib import pyplot as plt

########################################################################
# Argument Parsing  
def Parse_stuff():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--files", dest="filename", help='Filename (including path if not in current directory) of pkl')
  parser.add_argument("-p", "--pairs", dest="pairs", help="Chain, Resid pairs", nargs='*', default=[(0,0)])
  args = parser.parse_args()
  return args

def make_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

def run(args):
  folder = args.filename+'.ringer_plots'
  make_dir(folder)
  list = easy_pickle.load(args.filename)
  if args.pairs == [(0,0)]:
    for i in list: 
      if 1 in i._angles.keys():
        plot_ringer(i._angles[1].densities, i.resid, i.resname, i.chain_id, folder)
  else:
    pair_densities={}
    finished_pairs = []
    for i in args.pairs:
      finished_pairs.append((i.split(',')[0],i.split(',')[1]))
    for i in list: 
      if 1 in i._angles.keys():
        if (i.chain_id,str(int(i.resid))) in finished_pairs:
          print (i.chain_id,str(int(i.resid)))
          plot_ringer(i._angles[1].densities, int(i.resid),i.resname, i.chain_id, folder)


def plot_ringer(densities, resid, resname, chain_id, folder):
  x = range(0,365,5)
  # Add the 360 point, = the 0 point
  densities.append(densities[0])
  fig, ax = plt.subplots(figsize=(5,4))
  plt.axvspan(30, 90, color='0.5', alpha=0.5, linewidth=0)
  plt.axvspan(150, 210, color='0.5', alpha=0.5, linewidth=0)
  plt.axvspan(270, 330, color='0.5', alpha=0.5, linewidth=0)
  ax.set_xticks(range(0,390,60))
  ax.plot(x,densities, linewidth=3.0, color = "#5DA5DA")
  # ax.legend(loc=2)
  ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
  ax.xaxis.set_ticks_position('bottom')
  # ax.set_title("EMRinger Chi-1 Density Scan", y=1.05)
  ax.set_ylabel("Map Value", labelpad=10)
  ax.set_xlabel("Chi1 Angle ($\degree$)", labelpad=5)
  ax.set_ylim(-0.2,0.6)
  ax.set_xlim(0,360)
  fig.savefig("%s/%s_%d.png" % (folder, chain_id, int(resid)))


if __name__=='__main__':
  args=Parse_stuff()
  run(args)




