# remove "_isnull" columns;
# match the ordering of hsc-pdr3-dud-no_mag_limit.fits

from __future__ import division, print_function
import sys, os, time, argparse, glob, gc
import numpy as np
from astropy.table import Table, vstack
import fitsio

cat = Table(fitsio.read('/global/cfs/cdirs/desi/target/analysis/truth/parent/original/hsc-pdr3-dud-no_mag_limit_apflux_and_masks.fits'))
print(len(cat))

for colname in cat.colnames:
    if colname.endswith('_isnull'):
        cat.remove_column(colname)

tt = Table(fitsio.read('/global/cfs/cdirs/desi/target/analysis/truth/parent/original/hsc-pdr3-dud-no_mag_limit.fits', columns=['object_id']))
print(len(tt))

assert len(cat['object_id'])==len(np.unique(cat['object_id']))
assert len(cat)==len(tt) and np.all(np.unique(cat['object_id'])==np.unique(tt['object_id']))

# Matching cat to tt
if len(tt)!=len(cat) or not np.all(np.unique(tt['object_id'])==np.unique(cat['object_id'])):
    raise ValueError('tt and cat have different object_id list')
t1_reverse_sort = np.array(tt['object_id']).argsort().argsort()
cat = cat[np.argsort(cat['object_id'])[t1_reverse_sort]]

print(len(cat))
assert np.all(np.all(cat['object_id']==tt['object_id']))

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/hsc-pdr3-dud-no_mag_limit_apflux_and_masks-reduced.fits')
