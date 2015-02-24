# Rolling rotamericity metric

########################################################################
# Package imports
import numpy as np
import math
from emringer import ringer_chi, ringer_residue
from libtbx import easy_pickle
import matplotlib.pyplot as plt
import argparse
# from matplotlib import rcParams
from itertools import count, groupby

# rcParams['figure.autolayout'] = True
# rcParams['xtick.labelsize'] = 16
# rcParams['ytick.labelsize'] = 16
# rcParams['axes.labelsize'] = 24
# rcParams['axes.titlesize'] = 24


Residue_codes = ["ARG","ASN","ASP","CYS","GLU","GLN","HIS",
"LEU","LYS","MET","PHE","SER","TRP","TYR","SEC","PYL"]
Branched_residues = ["THR","VAL","ILE"]
No_c_gamma = ["ALA", "GLY"]
Weird = ["PRO"]


########################################################################
# Argument Parsing  
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--file_a", dest="filename_a", 
  help='Filename of pkl file', 
  default='/Users/benjaminbarad/Dropbox/Ringer_Project/Ringer_Output/5778.ent_ringer.pkl')
parser.add_argument("-o", dest="offset", type=int, default=0)
parser.add_argument("-t", "--threshold", dest="threshold", 
  help='Threshold cutoff for rho density', 
  nargs='?', type = float, default=0)
parser.add_argument("-w", "--extension_around_center", dest = "extension",
  help='Number of amino acids to extend around the center in both directions. \
  The total window will therefore be twice this number plus one for the center.'
  , nargs="?", type=int, default=10)
parser.add_argument("--percent_passing_cutoff", dest = "thresholded_cutoff",
  help='Minimum %% passing threshold to flag as a bad region...'
  , nargs="?", type=float, default=0.8)
parser.add_argument("--rotamericity_cutoff", dest = "rotamer_cutoff",
  help='Maximum rotamericity to be flagged.'
  , nargs="?", type=float, default=0.5)
parser.add_argument("--graph", dest = "graph", action='store_true')
parser.add_argument("--save", dest = "save", action='store_true', default=True)
parser.add_argument("-r", "--rel", dest = "rel", action='store_true')
parser.set_defaults(rel=False, graph=False, save=True)
args = parser.parse_args()

class RingerDict(object):
  '''Ringerdict: A dictionary accessible form of the output of ringer'''
  def __init__(self, resultlist, offset):
    self.dict = {}
    for residue in resultlist:
      if residue.resname in Residue_codes:
        residue.resid = int(residue.resid)+offset
        self.add_residue(residue)

  def add_residue(self, residue):
    if residue.chain_id not in self.dict.keys():
      self.dict[residue.chain_id] = {}
    if 1 in residue._angles.keys():
      self.dict[residue.chain_id][residue.resid] = residue._angles[1]

  def get_peak(self, chain_id, residue_id):
    if (chain_id in self.dict.keys() and residue_id in self.dict[chain_id].keys()):
      return self.dict[chain_id][residue_id]
    else:
      return None

  def get_chains(self):
    return self.dict.keys()

  def get_residues(self, chain_id):
    return sorted(self.dict[chain_id].keys())

def ranges(p):
    q = sorted(p)
    i = 0
    for j in xrange(1,len(q)):
        if q[j] > 1+q[j-1]:
            yield (q[i],q[j-1])
            i = j
    yield (q[i], q[-1])

def identify_regions(results):
  for chain, chain_out in results.iteritems():
    outliers = []
    print "For Chain %s:" % chain
    for k in chain_out:
      if (np.divide(k[2],k[1]) > args.thresholded_cutoff) and (np.divide(k[3],k[2]) < args.rotamer_cutoff):
        for i in range(k[0]-args.extension, k[0]+args.extension):
          outliers.append(i) 
    if len(outliers) > 0:
      print list(ranges(outliers))
      print ""
    else:
      print "No outliers at this threshold \n"





def main():
  ringer_results = easy_pickle.load(args.filename_a)
  hierarchy = RingerDict(ringer_results, 0)
  results_a = {}
  for chain in hierarchy.get_chains():
    results_a[chain] = []
    # Results will be a list of tuples of the form residue number, 
    # number checked in window, number passing threshold in window, 
    # number deviating in window.
    for i in hierarchy.get_residues(chain):
      total_n = 0.0
      threshold_n = 0.0
      # threshold_deviation = 0
      n_deviate = 0.0
      for j in range(-args.extension, args.extension+1):
        chi = hierarchy.get_peak(chain, int(i)+j)
        if chi:
          total_n += 1
          if args.rel:
            if chi.relrho > args.threshold:
              threshold_n += 1
              if chi.deviation <= 30:
                n_deviate += 1
          else:
            if chi.peakrho > args.threshold:
              threshold_n += 1
              if chi.deviation <= 30:
                n_deviate += 1
      results_a[chain].append((i, total_n, threshold_n, n_deviate))
  # identify_regions(results)
  if args.graph or args.save:
    plot_results(results_a)




def plot_results(results_a):
  for chain in results_a.keys():
    fig, ax = plt.subplots()
    plt.title("Rolling window - Chain %s" % chain)
    x_a = [k[0] for k in results_a[chain]]
    y_a = [np.divide(k[3],k[2]) for k in results_a[chain]]
    plt.plot(x_a, y_a, linewidth=3.0, alpha=0.9)
    # plt.xlim(381,695)
    plt.xlabel("Center Residue of %d-Residue Window" % (2*args.extension+1), labelpad=10)
    plt.ylabel("Fraction Rotameric Residues", labelpad=10)
    plt.ylim(0,1)
    # plt.legend(loc=4)
    # ax.axvspan(380,382,color='0.1',alpha=0.3, linewidth=0)
    # ax.axvspan(694,696,color='0.1',alpha=0.3, linewidth=0)
    ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
    ax.xaxis.set_ticks_position('bottom')
    if args.graph:
      fig.show()
    if args.save:
      output = args.filename_a[:-4] + "_" + chain + "_rolling.png"
      fig.savefig(output)


if __name__ == "__main__":
  main()

