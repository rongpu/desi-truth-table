# Keep only columns that are relevant

from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import sys
import fitsio
from astropy.table import Table

cat = fits.getdata('/project/projectdirs/desi/users/rongpu/specObj-dr13-unique.fits')

columns = ['SURVEY', 'INSTRUMENT', 'SPECOBJID', 'FLUXOBJID', 'BESTOBJID', 'PLATE', 'MJD', 'FIBERID', 'OBJID', 'PLUG_RA', 'PLUG_DEC', 'CLASS', 'SUBCLASS', 'Z', 'Z_ERR', 'RCHI2', 'DOF', 'RCHI2DIFF', 'ZWARNING', 'SN_MEDIAN_ALL']

cat1 = Table()

for index in range(len(columns)):
    col = columns[index]
    print(col)
    cat1[col] = cat[col]

cat1.write('/project/projectdirs/desi/users/rongpu/dr3_truth/specObj-dr13-unique-trimmed.fits')