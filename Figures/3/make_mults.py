import subprocess
# Make doubles
for i in range(1,24):
    input_string = "overlapmap MAPIN1 run1_ravg7_ct21_data_shiny_ravg7_frame%03d_half1_class001_unfil.mrc MAPIN2 run1_ravg7_ct21_data_shiny_ravg7_frame%03d_half1_class001_unfil.mrc MAPOUT %d+%d.ccp4 << END\n MAP ADD\n END" % (i, i+1, i, i+1) 
    print input_string
    subprocess.call(input_string, shell=True)

import subprocess
# Make triples
for i in range(1,23):
    input_string = "overlapmap MAPIN1 3Dvol_%03d.ccp4 MAPIN2 %d+%d.ccp4 MAPOUT %d_three_window.ccp4 << END\n MAP ADD\n END" % (i, i+1, i+2, i+1) 
    subprocess.call(input_string, shell=True)

import subprocess
# Make quints
for i in range(1,21):
    input_string = "overlapmap MAPIN1 %d_three_window.ccp4 MAPIN2 %d+%d.ccp4 MAPOUT %d_five_window.ccp4 << END\n MAP ADD\n END" % (i+1, i+3, i+4, i+2) 
    subprocess.call(input_string, shell=True)
