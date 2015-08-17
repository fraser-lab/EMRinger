reinit
viewport 1000,1000
bg white
set sphere_scale, 0.2
load ../pymol_ringer.py

set normalize_ccp4_maps, off
set ray_shadow, off

load 3J9I.pdb, mymodel
hide everything, mymodel
sele myview, mymodel and chain D and resi 98-100
as sticks, myview

#3
load 3_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.18, mymodel and chain D and resi 99 and (name CA or name CB), 2.3
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing D_99.json, cr=0.848, cg=.129, cb=.125, width=35

cd ..

set_color ringColor_3, [.848, .129, .125]


load D_99_3.pdb, peak_3
as spheres, peak_3
color ringColor_3, peak_3

set_view (\
     0.703835309,    0.087791100,    0.704916298,\
    -0.142429680,   -0.954738021,    0.261117131,\
     0.695935130,   -0.284184426,   -0.659476578,\
     0.000000000,    0.000000000,  -16.006774902,\
   184.469100952,  151.859786987,  117.564544678,\
    11.993782997,   20.019765854,  -20.000000000 )

ray

png 3B_1.png

delete mesh_3
delete map_3
delete D_99.json
delete peak_3


#9
load 9_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.18, mymodel and chain D and resi 99 and (name CA or name CB), 2.3
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing D_99.json, cr=0.902, cg=.453, cb=.184, width=35

cd ..

set_color ringColor_9, [0.902, .453, .184]


load D_99_9.pdb, peak_3
as spheres, peak_3
color ringColor_9, peak_3

set_view (\
     0.703835309,    0.087791100,    0.704916298,\
    -0.142429680,   -0.954738021,    0.261117131,\
     0.695935130,   -0.284184426,   -0.659476578,\
     0.000000000,    0.000000000,  -16.006774902,\
   184.469100952,  151.859786987,  117.564544678,\
    11.993782997,   20.019765854,  -20.000000000 )

ray

png 3B_2.png

delete mesh_3
delete map_3
delete D_99.json
delete peak_3


#15
load 15_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.18, mymodel and chain D and resi 99 and (name CA or name CB), 2.3
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing D_99.json, cr=0.273, cg=.512, cb=.754, width=35

cd ..

set_color ringColor_15, [.273, .512, .754]


load D_99_15.pdb, peak_3
as spheres, peak_3
color ringColor_15, peak_3

set_view (\
     0.703835309,    0.087791100,    0.704916298,\
    -0.142429680,   -0.954738021,    0.261117131,\
     0.695935130,   -0.284184426,   -0.659476578,\
     0.000000000,    0.000000000,  -16.006774902,\
   184.469100952,  151.859786987,  117.564544678,\
    11.993782997,   20.019765854,  -20.000000000 )

ray

png 3B_3.png

delete mesh_3
delete map_3
delete D_99.json
delete peak_3


#21
load 21_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.18, mymodel and chain D and resi 99 and (name CA or name CB), 2.3
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing D_99.json, cr=0.469, cg=.109, cb=.504, width=35

cd ..

set_color ringColor_21, [.469, .109, .504]


load D_99_21.pdb, peak_3
as spheres, peak_3
color ringColor_21, peak_3

set_view (\
     0.703835309,    0.087791100,    0.704916298,\
    -0.142429680,   -0.954738021,    0.261117131,\
     0.695935130,   -0.284184426,   -0.659476578,\
     0.000000000,    0.000000000,  -16.006774902,\
   184.469100952,  151.859786987,  117.564544678,\
    11.993782997,   20.019765854,  -20.000000000 )

ray

png 3B_4.png

delete mesh_3
delete map_3
delete D_99.json
delete peak_3
