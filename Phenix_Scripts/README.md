#Scripts to Run EMRinger

These scripts can all be run with phenix.python. 

`emringer_score.py` and `emringer_residue.py` and `emringer_rolling.py` each import from `emringer.py`, so all scripts must be kept in the same folder to run.

## Calculating an EMRinger Score for your structure
*EMRinger reports very sensitively on model-to-map agreement, and therefore precise fit is very important. Even slight misalignments can cause dramatically lower scores. For getting a precise fit if you don't have one coming out of refinement, the best result that I have come up with is to superimpose your model onto a fitted model. If such a model is not available, I have had great success using `phenix.real_space_refine` without any special parameters.*

The "standard" EMRinger Score calculation requires `emringer.py` and `emringer_score.py`. The first performs the EMRinger scan, and the second performs the threshold scan and calculates Z-scores at each threshold. It requires a model in pdb format, and a map in CCP4 format, with a file extension of `.map` or `.ccp4`. MRC files typically work as well, but the file extension needs to be changed and occasionally problems arise as a result of origin shifts. 

`emringer.py` spits out a pickle (`.pkl`) file that is used by all of the downstream scripts I have written, including `emringer_score.py`. Thus, to calculate an EMRinger score, you should perform the following pairs of commands (Here PDB.pdb is the pdb file and MAP.map is the map file. PDB_emringer.pkl is the automatically generated pkl file):
```bash
phenix.python emringer.py PDB.pdb MAP.map
phenix.python emringer_score.py -i PDB_emringer.pkl
```
 `emringer_score.py` will generate a series of histogram plots at each threshold, a plot of EMRinger scores and enrichment across thresholds, and a series `.pkl` files that contain the various data calculated in the scan. All of these plots will be saved to a folder that is named `PDB_emringer.pkl.output/`. These plots, and particularly the histograms, can be very useful for troubleshooting poor EMRinger scores. The scripts look best when used in combination with my [`matplotlibrc` file](https://github.com/bbarad/matplotlibrc), which will be used automatically by phenix.python if the file is in the same folder as the script is being run. A copy of the matplotlibrc is in the figures folder of this repository. 

#### Actually getting the score
The `emringer_score.py` script will also print a series of statistics, culminating in the EMRinger score. **This is the value that should be used in "table 1" or the equivalent for any structure papers using EMRinger score as a validation statistic.**

#### My score is near 0 (or negative); what now?
The histograms plotted by the `emringer_score.py` script can come in handy for troubleshooting.

If the results look like relatively flat noise, and you are confident in the quality of your map, it is likely that the position of the model does not line up with the map. Try loading your structure into pymol and seeing whether they overlap. You can do the same in Chimera, but it can detect and correct for some problems so that improperly aligned models might appear aligned. Position your model in the map well as described above; in a worst case scenario, `phenix.real_space_refine` should be able to correct the fit, but it may change your model somewhat in the process. Your model may need further improvement if it continues to score poorly after fitting, and it is also possible that your map is too low in resolution to resolve side chains.

If there is a significant number of peaks in the 0-20º range, or around 120º, you may be sampling into the backbone density during the EMRinger scan. This can happen in low resolution maps, but has been seen in a few cases in higher resolution maps. The solution we have found is to apply a small amount of B-factor sharpening. In general, B-factor sharpening decreases EMRinger scores in our experience, so we recommend using as small a degree of sharpening as possible to eliminate the sampling into the backbone. Large amounts of sharpening broadens the peaks in the EMRinger scan, making the assigned peak angle less accurate and more likely to be non-rotameric. It also may be necessary to perform further refinement, as slightly misplaced backbone positions can exacerbate the problem.



## Doing other things with EMRinger
To run other scripts used in the EMRinger manuscript, the following usage patterns are advised.

To calculate residue-specific EMRinger scores (such as those used for radiation damage analysis):
`phenix.python emringer_residue.py -i PDB_emringer.pkl -r ASP,GLU`

To calculate rolling window EMRinger analysis:
`phenix.python emringer_rolling.py -i PDB_emringer.pkl`

To calculate per-residue RSCC:
`phenix.python em_rscc PDB.pdb MAP.map d_min=3.27` #  d_min should be the resolution of the map.
