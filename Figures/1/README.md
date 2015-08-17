# Figure 1
*emringer.py is required for 1B\_D\_F.py to work. Move it to the folder you are working in. 1A\_C\_E.pml require the ringer pymol plugin.*

## Source Data
EMDB 5778 must be downloaded to use.  
1a.pdb is chain C of the deposited PDB TODO.  
1a_sphere.pdb is a water  placed at the peak value of the emringer plot for residue 519.

1c.pdb is chain C of the deposited PDB TODO, but with the dihedral angle of residue 519 set to 130 in pymol. 
1c_sphere.pdb is a water  placed at the peak value of the emringer plot for residue 519.

1e.pdb is chain C of the new deposited PDB 3J9J (refined by Ray Wang!).
1e_sphere.pdb is a water  placed at the peak value of the emringer plot for residue 519.

## Usage
```bash
phenix.python emringer_rings.py 1a.pdb emd_5778.map
phenix.python emringer_pkl_to_json.py 1a_emringer_rings.pkl

phenix.python emringer_rings.py 1c.pdb emd_5778.map
phenix.python emringer_pkl_to_json.py 1c_emringer_rings.pkl

phenix.python emringer_rings.py 1e.pdb emd_5778.map
phenix.python emringer_pkl_to_json.py 1e_emringer_rings.pkl

pymol 1A_C_E.pml

phenix.python emringer.py 1a.pdb emd_5778.map
phenix.python 1B_D_F.py -i 1a_emringer.pkl -p C,519 -o 1b.png

phenix.python emringer.py 1c.pdb emd_5778.map
phenix.python 1B_D_F.py -i 1c_emringer.pkl -p C,519 -o 1d.png

phenix.python emringer.py 1e.pdb emd_5778.map
phenix.python 1B_D_F.py -i 1e_emringer.pkl -p C,139 -o 1f.png
```