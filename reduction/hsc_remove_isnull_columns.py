# Remove "_isnull" columns

from __future__ import division, print_function
import numpy as np
from astropy.table import Table
import fitsio

######################################################################

cat = fitsio.read('/project/projectdirs/desi/target/analysis/truth/parent/original/hsc_pdr1_udeep.forced.fits')
cat = Table(cat)
print(len(cat))

colnames = cat.colnames
for colname in colnames:
    if colname.endswith('_isnull'):
        cat.remove_column(colname)

cat.write('/project/projectdirs/desi/target/analysis/truth/parent/hsc_pdr1_udeep.forced.reduced.fits')

######################################################################

cat = fitsio.read('/project/projectdirs/desi/target/analysis/truth/parent/original/hsc_pdr1_deep.forced.fits')
cat = Table(cat)
print(len(cat))

colnames = cat.colnames
for colname in colnames:
    if colname.endswith('_isnull'):
        cat.remove_column(colname)

cat.write('/project/projectdirs/desi/target/analysis/truth/parent/hsc_pdr1_deep.forced.reduced.fits')

######################################################################

cat = fitsio.read('/project/projectdirs/desi/target/analysis/truth/parent/original/hsc_pdr1_wide.forced.fits')
cat = Table(cat)
print(len(cat))

colnames = cat.colnames
for colname in colnames:
    if colname.endswith('_isnull'):
        cat.remove_column(colname)

cat.write('/project/projectdirs/desi/target/analysis/truth/parent/hsc_pdr1_wide.forced.reduced.fits')

