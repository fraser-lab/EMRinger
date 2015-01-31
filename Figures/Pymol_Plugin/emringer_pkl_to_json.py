from emringer_rings import *
from libtbx import easy_pickle
import json
import os, sys


def make_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

filename = sys.argv[1]
make_dir("%s_rings" % filename)

file = easy_pickle.load(sys.argv[1])
for i in file:
  json.dump(i._angles[1].densities, open("%s_rings/%s_%d.json" % (filename, i.chain_id, int(i.resid)), 'w'))
