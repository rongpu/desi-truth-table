from __future__ import print_function, division
import numpy as np
import sys, os
from astropy.table import Table
import fitsio

cat = fitsio.read('/Users/roz18/Downloads/2dFGRS_vizier.fits')
cat = Table(cat)
t = Table.read('/Users/roz18/Downloads/2dFGRS_vizier_RA_DEC_deg.fit')
cat['RAJ2000_deg'] = np.array(t['_RAJ2000'])
cat['DEJ2000_deg'] = np.array(t['_DEJ2000'])

cat.write('/Users/roz18/Downloads/2dFGRS.fits')