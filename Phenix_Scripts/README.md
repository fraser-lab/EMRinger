#Scripts to Run EMRinger

These scripts can all be run with phenix.python. 

`emringer_score.py` and `emringer_residue.py` and `emringer_rolling.py` each import from `emringer.py`, so all scripts must be kept in the same folder to run.

To run each script:

`phenix.python emringer.py PDB.pdb MAP.map`

`phenix.python emringer_score.py -i PDB_ringer.pkl`

`phenix.python emringer_residue.py -i PDB_ringer.pkl -r ASP,GLU`

`phenix.python emringer_rolling.py -i PDB_ringer.pkl`

`phenix.python em_rscc PDB.pdb MAP.map d_min=3.27` #  d_min should be the resolution of the map.