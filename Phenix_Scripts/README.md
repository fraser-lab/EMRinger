#Scripts to Run EMRinger

These scripts can all be run with phenix.python. 

`emringer_score.py` and `emringer_residue.py` and `emringer_rolling.py` each import from `emringer.py`, so all scripts must be kept in the same folder to run.

## Calculating an EMRinger Score for your structure
*EMRinger reports very sensitively on model-to-map agreement, and therefore precise fit is very important. Even slight misalignments can cause dramatically lower scores (try offsetting your structure by 0.1 Å... the score should drop dramatically). For getting a precise fit if you don't have one coming out of refinement, the best result that I have come up with is to superimpose your model onto a fitted model. If such a model is not available, I have had great success using `phenix.real_space_refine` without any special parameters.*

The "standard" EMRinger Score calculation requires `emringer.py` and `emringer_score.py`. The first performs the EMRinger scan, and the second performs the threshold scan and calculates Z-scores at each threshold. It requires a model in pdb format, and a map in CCP4 format, with a file extension of `.map` or `.ccp4`. MRC files typically work as well, but the file extension needs to be changed and occasionally problems arise as a result of origin shifts. 

`emringer.py` spits out a pickle (`.pkl`) file that is used by all of the downstream scripts I have written, including `emringer_score.py`. Thus, to calculate an EMRinger score, you should perform the following pairs of commands (Here PDB.pdb is the pdb file and MAP.map is the map file. PDB_ringer.pkl is the automatically generated pkl file):
```bash
phenix.python emringer.py PDB.pdb MAP.map
phenix.python emringer_score.py -i PDB_ringer.pkl
```
 `emringer_score.py` will generate a series of histogram plots at each threshold, a plot of EMRinger scores and enrichment across thresholds, and a series `.pkl` files that contain the various data calculated in the scan. All of these plots will be saved to a folder that is named `PDB_ringer.pkl.output/`. These plots, and particularly the histograms, can be very useful for troubleshooting poor EMRinger scores. The scripts look best when used in combination with my [`matplotlibrc` file](https://github.com/bbarad/matplotlibrc), which will be used automatically by phenix.python if the file is in the same folder as the script is being run. A copy of the matplotlibrc is in the figures folder of this repository. 

#### Actually getting the score
The `emringer_score.py` script will also print a series of statistics, culminating in the EMRinger score. **This is the value that should be used in "table 1" or the equivalent for any structure papers using EMRinger score as a validation statistic.**


## Doing other things with EMRinger
To run other scripts used in the EMRinger manuscript, the following usage patterns are advised.

To calculate residue-specific EMRinger scores (such as those used for radiation damage analysis):
`phenix.python emringer_residue.py -i PDB_ringer.pkl -r ASP,GLU`

To calculate rolling window EMRinger analysis:
`phenix.python emringer_rolling.py -i PDB_ringer.pkl`

To calculate per-residue RSCC:
`phenix.python em_rscc PDB.pdb MAP.map d_min=3.27` #  d_min should be the resolution of the map.
