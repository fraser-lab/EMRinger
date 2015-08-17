# Pymol plugin
This plugin generates the actual ring of dihedral space scanned by a ringer plot.

## Usage:
Using phenix:
```bash
phenix.python emringer_rings.py a.pdb b.map
phenix.python emringer_pkl_to_json.py a_ringer_rings.pkl
```

In pymol:
```pymol
run pymol_ringer.py
ringerRing A_1.json, cr, cg, cb, width
```