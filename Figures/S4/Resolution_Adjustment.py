import subprocess

resolutions = [3.2+i*0.2 for i in range(20)]
print "=====Generating MTZ====="
subprocess.call("phenix.map_to_structure_factors emd_5623.map box=true d_min=3.2", shell=True)
for i in resolutions:
  print "=====Running %f=====" % i
  subprocess.call("phenix.mtz2map emd_5623.mtz scale=volume output.prefix=%f d_min=%f grid_resolution_factor=1.2156/%f" % (i,i,i), shell=True) #grid_resolution_factor=0.2
  subprocess.call("phenix.python ../../Phenix_scripts/emringer.py %f_1.ccp4 5623.pdb output_base=%f" % (i,i), shell=True)
  subprocess.call("phenix.python emringer_resscan.py -i %f.pkl >> res_scan.txt" % i, shell=True)

