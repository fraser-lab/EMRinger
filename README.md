# DEPRECATED: EMRinger
## The current up to date version of EMRinger is packaged with CCTBX (https://github.com/cctbx/cctbx_project/blob/master/mmtbx/command_line/emringer.py). This version will not support new features or bugfixes.The code here remains for recapitulating exact results from the EMRinger paper (citation below). The up to date version can be run with `cctbx.emringer` or `phenix.emringer`, or in the Phenix GUI.

**This is the set of scripts used for the EMRinger paper (citation below). For the most up-to-date version of EMRinger, please use phenix.emringer or the integrated GUI version of EMRinger in the latest phenix nightly.**


*All of the scripts used in the EMRinger paper were based on [Phenix](www.phenix-online.org), [python](www.python.org), and [pymol](www.pymol.org)*

### Calculating EMRinger Scores
If you would like to calculate EMRinger scores, check out the `Phenix_Scripts` folder for more detailed instructions. Feel free to [email the authors](mailto:ben.barad@ucsf.edu) if you would like help running the scripts or want to troubleshoot any issues.

### Recapitulating the Figures
Ultimately, every figure used in the EMRinger paper should be recalculable by a user interested in investigating the tool. Currently, only some of the figure generation scripts have been packaged nicely, but feel free to check out the `Figures` folder to see my progress on that front. If there is a figure in the manuscript that you really want to try to generate with your own data, [email the authors](mailto:ben.barad@ucsf.edu) and we'll be more than happy to share the not-as-cleaned-up scripts we used.

## Requirements
*These were the software versions used to make the figures*
```
Phenix 1.9 official or any nightly after that.
Pymol Incentive 1.7.4 
Python 2.7.8
```
Within Python, the following extensions were used:
```
pandas
matplotlib
numpy
multiprocessing
```

## Citation:
Barad B.A., Echols N., Wang R. Y-R., Cheng Y.C., Dimaio F., Adams P.D., Fraser J.S. EMRinger: side-chain-directed model and map validation for 3D Electron Cryomicroscopy. *Nature Methods* published online 17 August 2015; doi: 10.1038/nmeth.3541
