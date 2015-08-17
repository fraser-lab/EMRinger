from libtbx import easy_pickle
import argparse
from emringer import *
import matplotlib
from matplotlib import pyplot as plt

########################################################################
# Argument Parsing  
def Parse_stuff():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--files", dest="filename", help='Filename (including path if not in current directory) of pkl')
  parser.add_argument("-p", "--pairs", dest="pairs", help="Chain, Resid pairs", nargs='*', default=[(0,0)])
  parser.add_argument("-o", "--output", dest="output", help="output filename", nargs='?', default='emringer_plot.png')  
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
          plot_ringer(i._angles[1].densities, int(i.resid),i.resname, i.chain_id, folder, args.output)
          # pair_densities[(i.chain_id,i.resname,i.resid)] = i._angles[1].densities
    # multiplot_ringer(pair_densities, folder)

def plot_ringer(densities, resid, resname, chain_id, folder, output="plot.png"):
  x = range(0,365,5)
  # Add the 360 point, = the 0 point
  densities.append(densities[0])
  fig, ax = plt.subplots(figsize=(5,4))
  plt.axvspan(30, 90, color='0.5', alpha=0.5, linewidth=0)
  plt.axvspan(150, 210, color='0.5', alpha=0.5, linewidth=0)
  ax.set_ylim(0,13)
  plt.axvspan(270, 330, color='0.5', alpha=0.5, linewidth=0)
  ax.set_xticks(range(0,390,60))
  ax.plot(x,densities, linewidth=3.0, color = "#5DA5DA")
  # ax.legend(loc=2)
  ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
  ax.xaxis.set_ticks_position('bottom')
  # ax.set_title("EMRinger Chi-1 Density Scan", y=1.05)
  ax.set_ylabel("Map value", labelpad=10)
  ax.set_xlabel("$\chi$1 angle ($\degree$)", labelpad=5)
  # ax.set_xlabel("Chi1 angle ($\degree$)", labelpad=5)
  # ax.spines['top'].set_visible(False)
  # ax.spines['right'].set_visible(False)
  ax.get_xaxis().tick_bottom()
  ax.get_yaxis().tick_left()
  ax.grid()
  # ax.get_xaxis().set_major_formatter(
  #   matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
  # ax.get_yaxis().set_major_formatter(
  #   matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
  # ax.set_ylim(0,13)
  ax.set_xlim(0,360)
  fig.savefig("%s" % (output))

# def multiplot_ringer(pair_densities, folder):
#   fig, ax = plt.subplots()
#   plt.axvspan(30, 90, color='0.5', alpha=0.5)
#   plt.axvspan(150, 210, color='0.5', alpha=0.5)
#   plt.axvspan(270, 330, color='0.5', alpha=0.5)
#   x = range(0,365,5)
#   ax.set_xlim(0,360)
#   ax.set_xticks(range(0,390,60))
#   ax.set_ylim(0,13)
#   ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
#   ax.xaxis.set_ticks_position('bottom')
#   # ax.set_title("Ringer Plot", y=1.05)
#   ax.set_ylabel("Electron Potential Density", labelpad=5)
#   ax.set_xlabel("Chi-1 Angle", labelpad=5)
#   for key, value in pair_densities.iteritems():
#     y = value + value[0:0]
#     print y
#     print x
#     ax.plot(x,value, label="Residue %s %d of Chain %s" % (key[1],int(key[2]),key[0]))
#   # ax.legend(loc=2)
#   fig.savefig("%s/multiplot.png" % folder)

if __name__=='__main__':
  args=Parse_stuff()
  run(args)




