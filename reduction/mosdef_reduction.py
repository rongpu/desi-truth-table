from __future__ import print_function, division
import numpy as np
import sys, os
from astropy.table import Table

cat = Table.read('mosdef_zcat.final.fits')

print(len(cat))
mask = cat['TARGET']==1
cat = cat[mask]
print(len(cat))
mask = (cat['Z_MOSFIRE']>0)
cat = cat[mask]
print(len(cat))
mask = cat['Z_MOSFIRE_ZQUAL']==7
cat = cat[mask]
print(len(cat))

cat.write('mosdef_zcat.final.reduced.fits')