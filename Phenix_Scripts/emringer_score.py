#! /usr/bin/env phenix.python

# Rotamer distribution analysis tool for validation of models generated from cryoEM data.
# Written by Benjamin Barad

# Written for use with EMRinger pkl output.
# 
# Reference:
#
# Barad BA, Echols N, Wang RYR, Cheng YC, DiMaio F, Adams PD, Fraser JS. 
# Side-chain-directed model and map validation for 3D Electron Cryomicroscopy. 
# Manuscript in preparation.

########################################################################
# Package imports
import math
import numpy as np
import os
from libtbx import easy_pickle, adopt_init_args
from emringer import *
import matplotlib.pyplot as plt
import argparse
from collections import OrderedDict
from matplotlib import rcParams
rcParams['figure.autolayout'] = True
# rcParams['xtick.labelsize'] = 16
# rcParams['ytick.labelsize'] = 16
# rcParams['axes.labelsize'] = 24
# rcParams['axes.titlesize'] = 24



########################################################################
# Argument Parsing  
def Parse_stuff():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--files", dest="filenames", help='Filenames (including path if not in current directory) of pkl', nargs='*', default=['/5623_emringer.pkl'])
  parser.add_argument("-s", "--Sampling_Angle", dest="sampling_angle", help="Don't mess with this unless you've also made the corresponding change in emringer. By default it is 5, which is identical to the default in ringer.", nargs='?', default=5)  
  args = parser.parse_args()
  return args


########################################################################
# Classes and Statics- these may eventually want to be moved to ringer.

class Peak:
	# The peak object, should eventually get moved into ringer I suspect.
	def __init__(self, resname, resid, chain_id, n_chi, chi_value, rho_value):
		adopt_init_args(self, locals())
		self.chi_value=chi_value%360

	def __repr__(self):
		return "\n%s\t%s\t%s\t%s\t%d\t%f" % (self.resname,self.resid,self.chain_id,self.n_chi,self.chi_value*5,self.rho_value)

class Peaklist:
	# Right now this is just a slightly specialized list. I may add functionality later, however.
	def __init__(self):
		self.peaks=[]

	def sorted(self, *key):
		return sorted(self.peaks,*key)

	def append_lists(self,other_peaklist):
		self.peaks = self.peaks+ other_peaklist.peaks

	def add_new(self,resname, resid, chain_id, n_chi, chi_value, rho_value):
		self.peaks.append(Peak(resname, resid, chain_id, n_chi, chi_value, rho_value))

	def get_peaks(self):
		return self.peaks

	def __len__(self):
		return len(self.peaks)

	def __repr__(self):
		return str(sorted(self.peaks,key=lambda peak: peak.chi_value))

# Residue_codes = ["PHE","TYR","TRP"]
Residue_codes = ["ARG","ASN","ASP","CYS","GLU","GLN","HIS",
"LEU","LYS","MET","PHE","SER","TRP","TYR","SEC","PYL"]
Ignored_codes = ["ALA","GLY","PRO","THR","ILE","VAL"]

########################################################################
# Child Functions

def statistic(binned_peaks):
	# this is the main pair of statistics used for my plots.
	# Normal approximation to the binomial theorem.
	rotamer_count = sum(binned_peaks[0::2])
	total_count = sum(binned_peaks)
	stdev = math.sqrt(39.0/72*33.0/72*total_count)
	mean= total_count*39.0/72
	# Hacky way to avoid zero division
	rotamer_ratio=rotamer_count/(total_count+0.000000000000000000001)
	zscore=(rotamer_count-mean)/(stdev+0.000000000000000000001)
	# print "\t Rotamer ratio: %.3f" % rotamer_ratio
	# print "\t Z-score = %.3f" % zscore
	# if (zscore>0):
	# 	pscore_approx1=0.5-0.5*(math.erf(zscore/math.sqrt(2)))
	# 	pscore_approx2=1.0/12*math.exp(-zscore*zscore/2)+1.0/4*math.exp(-zscore*zscore*2/3)
	# 	# print "\t One approximation of the p-value is %g" % pscore_approx1
		# print "\t Another approximation of the p-value is %g" % pscore_approx2
	# else:
		# print "\t pscore greater than 0.5"

	return zscore, rotamer_ratio

def RMSD_statistic(peak_list):
	# Still not clear how useful RMSD is but angular deviations tend to be heavily dependent on sample size (as outliers are overweighted).
	squared_deviations=[]
	for peak in peak_list:
		squared_deviations.append(min((i-peak.chi_value)**2 for i in [60,180,300]))
	RMSD = (sum(squared_deviations)/len(squared_deviations))**0.5
	return RMSD

def calculate_peaks(ringer,threshold, args):
	## Checks if something is greater than either of its neighbors (including wrapping) and returns if true and if above a threshold)
	new_peaks=Peaklist()
	list = ringer._angles[1].densities
	for i in range(len(list)):
		if (list[i]==max(list) and list[i]>threshold):
			new_peaks.add_new(ringer.resname, ringer.resid, ringer.chain_id, 1, i, list[i])
	return new_peaks



def parse_pickle(filename, args):
	# All processes that require reading the pickle. Involves reading out the angles and calculating the thresholds.
	print "===== Loading Pickle: %s =====" % filename
	chi = 1
	waves=[]
	averages=[]
	maxima=[]
	ringer_things = easy_pickle.load(filename)
	for i in ringer_things:
		if chi in i._angles.keys() and i.resname in Residue_codes:
			waves.append(i)
			maxima.append(max(i._angles[chi].densities))
			averages.append(np.average(i._angles[chi].densities))
	max_max = max(maxima)
	avg_avg = np.average(averages)
	thresholds = [avg_avg+i*(max_max-avg_avg)/20 for i in range(20)]
	print "Threshold list: %s" % thresholds
	print "===== Pickle Parsed ====="
	return waves, thresholds

def calculate_binned_counts(peak_count, first=60, binsize=12,n_angles=72): 
	# Bin peaks by rotamer regions for statistics.
	first_loc = int(first/5)
	bins = int(n_angles/binsize)
	binned_output=[0]*bins
	for i in range(bins):
		for j in range(binsize):
			binned_output[i] += peak_count[int(first_loc+i*binsize-binsize/2+j)%72]
	return binned_output

def calc_ratio(count_list, args):
	# Calculate the same statistics as the "statistic" call, but do it without ifrst binning the peaks.
	total_angles=360/args.sampling_angle
	binsize=int(total_angles/6)
	first_loc=60/args.sampling_angle
	
	binned_list=[0]*6
	for i in range(6):
		for j in range(binsize):
			binned_list[i] += count_list[int(first_loc+i*binsize-binsize/2+j)%72]
	rotamer_count = sum(binned_list[0::2])
	total_count = sum(binned_list)
	stdev = 0.5*math.sqrt(total_count)
	mean= total_count/2
	rotamer_ratio=rotamer_count/(total_count+0.000000000000000000001)
	zscore=(rotamer_count-mean)/(stdev+0.000000000000000000001)
	return rotamer_ratio, zscore


def make_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

########################################################################
# Main Run

def main(args):
	for file in args.filenames:
		make_dir(file+'.output')
		Weird_residues=OrderedDict()
		peak_count={}
		residue_peak_count={}
		rotamer_ratios_residues={}
		zscores_residues={}
		for i in Residue_codes:
			residue_peak_count[i]={}
			rotamer_ratios_residues[i]=[]
			zscores_residues[i]=[]
		binned_peaks={}
		zscores=[]
		rotamer_ratios=[]

		non_zero_thresholds=[]
		waves, thresholds = parse_pickle(file, args)
		length = len(waves)
		peaks=OrderedDict()
				# calculate peaks and histogram
		for threshold in thresholds:
			print ""
			print "===== Calculating Statistics for Threshold %.3f =====" % threshold
			peaks[threshold]=Peaklist()
			Weird_residues[threshold]=Peaklist()
			peak_count[threshold] = [0]*72
			for i in Residue_codes:
				residue_peak_count[i][threshold]=[0]*72
			for i in waves:
				peaks[threshold].append_lists(calculate_peaks(i, threshold, args))
			for peak in peaks[threshold].get_peaks():
				peak_count[threshold][peak.chi_value]+=1
				residue_peak_count[peak.resname][threshold][peak.chi_value]+=1
				if ((peak.chi_value<6) or (peak.chi_value>18 and peak.chi_value<30) or (peak.chi_value>42 and peak.chi_value<54) or (peak.chi_value>66)):
					Weird_residues[threshold].peaks.append(peak)
			# Calculate the binned peaks and ratios
			binned_peaks[threshold] = calculate_binned_counts(peak_count[threshold], 60)
			# print "For threshold %.3f" % threshold
			# print "Sample size = %d" % sum(binned_peaks[threshold])
			zscore_n, rotamer_ratio_n = statistic(binned_peaks[threshold])
			if rotamer_ratio_n==0: 
				break
			for i in Residue_codes:
				rotamer_ratios_residues_n, zscores_n = calc_ratio(residue_peak_count[i][threshold], args)
				rotamer_ratios_residues[i].append(rotamer_ratios_residues_n)
				zscores_residues[i].append(zscores_n)
			non_zero_thresholds.append(threshold)
			zscores.append(zscore_n)
			rotamer_ratios.append(rotamer_ratio_n)
			print "===== Plotting Histogram for Threshold %.3f =====" % threshold
			plot_peaks(peak_count[threshold], file, threshold, 60, RMSD_statistic(peaks[threshold].peaks))
			# plot_rotamers(binned_peaks[threshold], file, threshold, 60)
		# 	print "Outliers at threshold %.2f: %s" % (threshold, str(Weird_residues[threshold]))
		print ""
		print "===== Plotting Statistics Across Thresholds ====="
		plot_progression(non_zero_thresholds, rotamer_ratios, file, [10*i/math.sqrt(length) for i in zscores])
		# for i in Residue_codes:
		# 	plot_progression(non_zero_thresholds, rotamer_ratios_residues[i], file, zscores_residues[i], i)
		print ""
		print "===== Writing Pickles Out ====="
		easy_pickle.dump(file+'.output/Outliers.pkl',Weird_residues)
		print 'Wrote ' + file+'.output/Outliers.pkl'
		easy_pickle.dump(file+'.output/rotamer_ratios.pkl', rotamer_ratios)
		print 'Wrote ' + file+'.output/rotamer_ratios.pkl'
		easy_pickle.dump(file+'.output/zscores.pkl', zscores)
		print 'Wrote ' + file+'.output/zscores.pkl'
		easy_pickle.dump(file+'.output/emringer_scores.pkl', [10*i/math.sqrt(length) for i in zscores])
		print 'Wrote ' + file+'.output/emringer_scores.pkl'
		easy_pickle.dump(file+'.output/thresholds.pkl', thresholds)
		print 'Wrote ' + file+'.output/thresholds.pkl'
		easy_pickle.dump(file+'.output/peak_counts.pkl', peak_count)
		print 'Wrote ' + file+'.output/peak_counts.pkl'
		for index, value in enumerate(zscores):
			if value == max(zscores):
				print ""
				print "=====Final Statistics for Model/Map Pair====="
				print "Optimal Threshold: %.3f" % non_zero_thresholds[index]
				print "Rotamer-Ratio: %.3f" % rotamer_ratios[index]
				print "Max Zscore: %.3f" % float(value)
				print "Total Residues Scanned: %d" % length
				# print "Z-score/(length): %.8f" % (value/length)
				print "EMRinger Score: %8f" % (10*value/math.sqrt(length))
				break
		return float(10*max(zscores)/math.sqrt(length))





########################################################################
# GUI and Output

def plot_rotamers(binned_output, filename, threshold, first):
	# Binned Histogram
	plt.figure(1)
	plt.clf()
	colors=['blue','red']*3
	angles = range(6)
	bin_angles = [(i*60+first)%360 for i in angles]
	plt.bar(bin_angles, binned_output, align='center', color=colors, width=60)
	plt.savefig('%s.output/%.3f.Phenixed_Histogram.png' % (filename,threshold))
	# print 'Wrote '+filename+'/%.3f.Phenixed_Histogram.png' % threshold
	
def plot_peaks(peak_count, filename, threshold, first, title=0):
	plt.figure(2, figsize=(6,4.5))
	# rcParams.update({'figure.autolayout': True})
	colors = ['#F15854']*6+['#5DA5DA']*13+['#F15854']*11+['#5DA5DA']*13+['#F15854']*11+['#5DA5DA']*13+['#F15854']*5
	plt.clf()
	plt.axvspan((first-30), first+30, color='0.5', alpha=0.5, linewidth=0)
	plt.axvspan(first+90, first+150, color='0.5', alpha=0.5, linewidth=0)
	plt.axvspan(first+210, (first+270), color='0.5', alpha=0.5, linewidth=0)
	plt.tick_params(axis='x',which='both',top='off')
	plt.tick_params(axis='y',which='both',right='off')
	peak_count_extra = peak_count+[peak_count[0]]
	angles = [i*5 for i in range(0,73)]
	plt.bar(angles,peak_count_extra, width=5, align='center', color=colors)
	# plt.title('Peak Counts', y=1.05) #  - Threshold %.3f' % (threshold)
	plt.xticks([i*60 for i in range(7)])
	plt.xlim(0,360)
	plt.xlabel(r'Chi1 Angle ($\degree$)', labelpad=10)
	plt.ylabel("Peak Count", labelpad=10)
	plt.savefig('%s.output/%.3f.threshold_histogram.png' % (filename,threshold))
	print 'Saved plot to %s.output/%.3f.threshold_histogram.png' % (filename,threshold)
	# print 'RMSD at threshold %.3f is %.1f' % (threshold,title)
	# print 'Wrote '+filename+'/%.3f.Phenix_allpeaks.png' % threshold
	plt.clf()

def plot_progression(non_zero_thresholds, rotamer_ratios, file, zscores, i="Total"):
	for j in range(len(zscores)):
		if zscores[j]>=0:
			non_zero_thresholds = non_zero_thresholds[j:]
			rotamer_ratios= rotamer_ratios[j:]
			zscores=zscores[j:]
			break
	fig = plt.figure(3, figsize=(6,4.5))
	ax1 = plt.subplot()
	ax1.plot(non_zero_thresholds, zscores, 'b-', linewidth=3.0, alpha=0.7)
	ax1.set_xlabel('Map Value Threshold')
	# Make the y-axis label and tick labels match the line color.
	ax1.set_ylabel('EMRinger Score', color='b')
	for tl in ax1.get_yticklabels():
		tl.set_color('b')
	ax1.set_ylim([-1,4])
	ax1.axhspan(-0.015,0.015,color='0.1',alpha=0.3, linewidth=0)
	ax2 = ax1.twinx()
	ax2.grid()
	ax2.plot(non_zero_thresholds, rotamer_ratios, 'r-', label = i, linewidth=3.0, alpha=0.7)
	ax2.set_ylim([0.4,1])
	ax2.set_ylabel(r'Fraction Rotameric', color='r', labelpad=10)
	ax1.xaxis.set_ticks_position('bottom')
	# ax2.set_xlim(2,12)
	# ax2.set_xlim([0.005,0.03])
	for tl in ax2.get_yticklabels():
		tl.set_color('r')
	# if i != "Total":
		# plt.title("Threshold Scan - %s" % i, y=1.05) 
	# else:
	# plt.title("Threshold Scan", y=1.05)
	plt.savefig('%s.output/%s.threshold_scan.png' % (file, i))
	print 'Saved plot to %s.output/%s.threshold_scan.png' % (file, i)
	# print 'Wrote '+file+'/threshold_scan.png'
	plt.clf()
	

if __name__ == "__main__":
	args = Parse_stuff()
	main(args)

