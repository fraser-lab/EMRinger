# Last tested on incentive pymol 1.7.6.0

reinit
viewport 1000,1000
bg white
set sphere_scale, 0.2

set normalize_ccp4_maps, off
set ray_shadow, off

run pymoL_ringer.py
set_color sphere_color = (1.,0.4, 0.8)
load emd_5778.map, emmap, format=ccp4



# 1A
load 1a.pdb, 1a
hide everything, 1a
show sticks, 1a and resi 518-520
isomesh mesh, emmap, 10, 1a and resi 517-522, carve=2.8
color gray, mesh
ringerRing 1a_ringer_rings.pkl_rings/C_519.json, width=35
load 1a_peak.pdb, 1a_peak
show sphere, 1a_peak
color sphere_color, 1a_peak

set_view (\
     0.575205505,   -0.465316206,    0.672765613,\
     0.336578012,    0.884230018,    0.323804051,\
    -0.745553434,    0.040184479,    0.665231764,\
    -0.000101128,    0.000070696,  -15.356035233,\
    29.777294159,  -10.306631088,  -20.545518875,\
    -8.448255539,   39.157485962,  -20.000000000 )

ray
png 1a.png

delete 1a
delete 1a_peak
delete mesh
delete 1a_ringer_rings.pkl_rings_C_519.json

#1C
load 1c.pdb, 1c
hide everything, 1c
show sticks, 1c and resi 518-520
color green, 1c
util.cnc
isomesh mesh, emmap, 10, 1c and resi 517-522, carve=2.8
color gray, mesh
ringerRing 1c_ringer_rings.pkl_rings/C_519.json, width=35
load 1c_peak.pdb, 1c_peak
show sphere, 1c_peak
color sphere_color, 1c_peak

set_view (\
     0.575205505,   -0.465316206,    0.672765613,\
     0.336578012,    0.884230018,    0.323804051,\
    -0.745553434,    0.040184479,    0.665231764,\
    -0.000101128,    0.000070696,  -15.356035233,\
    29.777294159,  -10.306631088,  -20.545518875,\
    -8.448255539,   39.157485962,  -20.000000000 )

ray
png 1c.png

delete 1c
delete 1c_peak
delete mesh
delete 1c_ringer_rings.pkl_rings_C_519.json

#1E
load 1e.pdb, 1e

hide everything, 1e
show sticks, 1e and resi 138-140
color tv_orange, 1e
util.cnc
hide (hydro)
isomesh mesh, emmap, 10, 1e and resi 137-140, carve=2.35
color gray, mesh
ringerRing 1e_ringer_rings.pkl_rings/C_139.json, width=35
load 1e_peak.pdb, 1e_peak
show sphere, 1e_peak
color sphere_color, 1e_peak

set_view (\
     0.575205505,   -0.465316206,    0.672765613,\
     0.336578012,    0.884230018,    0.323804051,\
    -0.745553434,    0.040184479,    0.665231764,\
    -0.000101128,    0.000070696,  -15.356035233,\
    29.777294159,  -10.306631088,  -20.545518875,\
    -8.448255539,   39.157485962,  -20.000000000 )

ray
png 1e.png
