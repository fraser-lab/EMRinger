import json
import pymol
from pymol.cgo import *

# This is a heavily modified version of the cgoCircle script found on the pymol wiki)
# This tool has been developed to support the EMRinger software, but is useful for all dihedral-sampling visualization.
def ringerRing(jsonfile, cr=1, cg=0.4, cb=0.8, width=28):
  with open(jsonfile, 'r') as file:
    vertices = json.load(file)
  obj=[BEGIN, LINES, COLOR, float(cr), float(cg), float(cb)]
  for i in range(len(vertices)):
    obj.append( VERTEX )
    obj.append(vertices[i][0])
    obj.append(vertices[i][1])
    obj.append(vertices[i][2])
    obj.append( VERTEX )
    obj.append(vertices[(i+1)%len(vertices)][0])
    obj.append(vertices[(i+1)%len(vertices)][1])
    obj.append(vertices[(i+1)%len(vertices)][2])  
  obj.append(END)

  cName=str(jsonfile)
  cmd.load_cgo(obj, cName)
  cmd.set("cgo_line_width", width)
  return obj


cmd.extend("ringerRing", ringerRing)