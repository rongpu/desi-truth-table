# Convert WiggleZ final data release dataset to FITS

from __future__ import print_function, division
import numpy as np
import sys, os
from astropy.table import Table

colnames = ['WiggleZ_Name', 'RA', 'Dec', 'redshift', 'Dredshift', 'Q', 'FUV', 'NUV', 'u', 'g', 'r', 'i', 'z', 'DFUV', 'DNUV', 'Du', 'Dg', 'Dr', 'Di', 'Dz', 'E(B-V)', 'class', 'UTdate', 'MFUV', 'Mass', 'DMass', 'SpecFile', 'comments']

cat = Table.read('wigglez.dat', format='ascii')

for index in range(28):
    colname_old = 'col'+str(index+1)
    colname_new = colnames[index]
    cat.rename_column(colname_old, colname_new)

cat1 = cat.copy()

# Convert 'null' to numpy nan
for index in range(28):
    colname = colnames[index]
    mask = cat1[colname]=='null'
    if np.sum(mask)>0:
        print(colname)
        d = cat1[colname]
        d[mask] = 'nan'
        d = np.array(d, dtype=float)
        cat1[colname] = d

cat1.write('wigglez.final.fits')
