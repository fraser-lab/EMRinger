# Figure 2
* Note: for most of these scripts to work, you must have emringer.py and emringer_score.py in the same folder as the scripts. Move them here before you run the jobs!*



Subpanels a-c of this figure concern the proteasome (PDB 3j9i, EMDB 5623), and emringer must be performed before the rest of the scripts can be run.

Subpanel d uses EMDB_table.csv

## Usage

```bash
phenix.python emringer.py 3j9i.pdb emd_5623.map
phenix.python 2A.py -i 3j9i_emringer.pkl
phenix.python emringer_score.py -i 3J9I_emringer.pkl
phenix.python 2B.py 3J9I_emringer.output/
phenix.python 2C.py -i 3j9i_emringer.pkl
phenix.python 2D.py 
```

* I use my matplotlibrc file to make the plots look good by default. You can put it in this folder or in your `~/.matplotlib` folder. *
