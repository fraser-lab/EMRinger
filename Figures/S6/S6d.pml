reinit
viewport 1000,1000
bg white
set sphere_scale, 0.2

set normalize_ccp4_maps, off
set ray_shadow, off

load emd_5778.map, mymap, format=ccp4
load final_300.pdb, refined
load deposited.pdb, unrefined

set_view (\
    -0.067859709,   -0.281320244,   -0.957210422,\
    -0.172237784,    0.948321700,   -0.266495556,\
     0.982717156,    0.146789506,   -0.112809010,\
    -0.000074932,    0.000000206,  -46.434886932,\
   -36.917549133,   -4.189402580,   -5.308875084,\
    29.610561371,   63.237155914,  -20.000000000 )

hide everything
sele ref_sele, refined and chain B and resi 47-58
sele unref_sele, unrefined and chain B and resi 427-438
show sticks, ref_sele
show sticks, unref_sele
isomesh mesh, mymap, 10, chain B and resi 45-60, carve=2
color gray, mesh
hide (hydro)
show cartoon, ref_sele and bb.
cartoon tube, ref_sele and bb.
show cartoon, unref_sele and bb.
cartoon tube, unref_sele and bb.
set cartoon_tube_radius, .25
set cartoon_side_chain_helper, on

set_color new_red, [.848, .129, .125]
set_color new_purple, [.691, .469, .649]

color new_red, unrefined
color new_purple, refined
util.cnc()

ray #1000,1000
png refinement_comparison_pymol.png
