#Figure 3

Figure 3 performs emringer analysis on dose-fractionated maps of the T20S proteasome using a single static model to understand the effects of radiation damage on individual side-chains.

I attached the script I used to generate the frame-averaged maps, but for space reasons I am not distributing them. Instead, I am including pkl files containing the EMRinger scores for each residue subset and each averaged structure.

## Usage

```bash
phenix.python 3A.py

phenix.python emringer_rings.py 3J9I.pdb emd_5778.map 
phenix.python emringer_pkl_to_json.py 3J9I_ringer_rings.pkl

pymol 3B.pml 

phenix.python 3C_E.py D 99 3C.png

pymol 3D.pml

phenix.python 3C_E.py 1 36
``` 




*I am not including the raw dose-fractionated data here for the sake of data management (it spans several gigabytes). If you need to recapitulate the exact data, please email [Ben Barad](mailto:benjamin.barad@gmail.com) to coordinate a data transfer.*
