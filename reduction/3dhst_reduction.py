# Split 3D-HST master catalog into separate catlogs in each field; 

from __future__ import division, print_function
import numpy as np
import sys
from astropy.table import Table

cat = Table.read('/Users/roz18/Documents/Data/desi-truth-table/3dhst.v4.1.5.master.fits.gz')

# print(len(cat))
# mask = cat['z_max_grism']>0
# cat = cat[mask]
# print(len(cat))

fields = np.unique(cat['field'])

for field in fields:
    mask = cat['field']==field
    cat1 = cat[mask].copy()
    cat1.write('/Users/roz18/Documents/Data/desi-truth-table/3dhst.v4.1.5.master.'+field+'.reduced.fits')