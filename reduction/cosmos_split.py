from __future__ import division, print_function
import numpy as np
import sys
from astropy.table import Table

cat = Table.read('/Users/roz18/Documents/Temp/desi-truth-table/3dhst.v4.1.5.master.fits.gz')
fields = np.unique(cat['field'])

for field in fields:
    mask = cat['field']==field
    cat1 = cat[mask].copy()
    cat1.write('/Users/roz18/Documents/Temp/desi-truth-table/3dhst.v4.1.5.master.'+field+'.fits')