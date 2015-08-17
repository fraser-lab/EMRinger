reinit
viewport 1000,1000
bg white
set sphere_scale, 0.2
load ../pymol_ringer.py

set normalize_ccp4_maps, off
set ray_shadow, off

load 3J9I.pdb, mymodel
hide everything, mymodel
sele myview, mymodel and chain 1 and resi 35-37
as sticks, myview

#3
load 3_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.32, mymodel and chain 1 and resi 35-39, carve=2.5
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing 1_36.json, cr=0.848, cg=.129, cb=.125, width=28

cd ..

set_color ringColor_3, [.848, .129, .125]


load 1_36_3.pdb, peak_3
as spheres, peak_3
color ringColor_3, peak_3

set_view (\
    -0.520099282,    0.280341119,    0.806787133,\
     0.129185930,   -0.907904387,    0.398760438,\
     0.844276547,    0.311621547,    0.435985923,\
    -0.001054092,    0.000622319,  -20.454679489,\
   174.155899048,  119.923820496,  182.085083008,\
    14.844653130,   25.414520264,  -20.000000000 )

ray

png 3D_1.png

delete mesh_3
delete map_3
delete 1_36.json
delete peak_3


#9
load 9_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.32, mymodel and chain 1 and resi 35-39, carve=2.5
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing 1_36.json, cr=0.902, cg=.453, cb=.184, width=28

cd ..

set_color ringColor_9, [0.902, .453, .184]


load 1_36_9.pdb, peak_3
as spheres, peak_3
color ringColor_9, peak_3

set_view (\
    -0.520099282,    0.280341119,    0.806787133,\
     0.129185930,   -0.907904387,    0.398760438,\
     0.844276547,    0.311621547,    0.435985923,\
    -0.001054092,    0.000622319,  -20.454679489,\
   174.155899048,  119.923820496,  182.085083008,\
    14.844653130,   25.414520264,  -20.000000000 )

ray

png 3D_2.png

delete mesh_3
delete map_3
delete 1_36.json
delete peak_3


#15
load 15_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.32, mymodel and chain 1 and resi 35-40, carve=2.5
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing 1_36.json, cr=0.273, cg=.512, cb=.754, width=28

cd ..

set_color ringColor_15, [.273, .512, .754]


load 1_36_15.pdb, peak_3
as spheres, peak_3
color ringColor_15, peak_3
set_view (\
    -0.520099282,    0.280341119,    0.806787133,\
     0.129185930,   -0.907904387,    0.398760438,\
     0.844276547,    0.311621547,    0.435985923,\
    -0.001054092,    0.000622319,  -20.454679489,\
   174.155899048,  119.923820496,  182.085083008,\
    14.844653130,   25.414520264,  -20.000000000 )


ray

png 3D_3.png

delete mesh_3
delete map_3
delete 1_36.json
delete peak_3


#21
load 21_five_window.ccp4, map_3, format=ccp4
isomesh mesh_3, map_3, 0.32, mymodel and chain 1 and resi 35-39, carve=2.5
color grey, mesh_3



cd 3J9I_ringer_rings.pkl_rings/

ringerRing 1_36.json, cr=0.469, cg=.109, cb=.504, width=28

cd ..

set_color ringColor_21, [.469, .109, .504]


load 1_36_21.pdb, peak_3
as spheres, peak_3
color ringColor_21, peak_3

set_view (\
    -0.520099282,    0.280341119,    0.806787133,\
     0.129185930,   -0.907904387,    0.398760438,\
     0.844276547,    0.311621547,    0.435985923,\
    -0.001054092,    0.000622319,  -20.454679489,\
   174.155899048,  119.923820496,  182.085083008,\
    14.844653130,   25.414520264,  -20.000000000 )


ray

png 3D_4.png
