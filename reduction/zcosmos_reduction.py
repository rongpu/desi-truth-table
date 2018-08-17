# Convert ASCII file to FITS format

from __future__ import division, print_function
import numpy as np
import sys
from astropy.table import Table

cat = Table.read('/Users/roz18/Downloads/cesam_zcosbrightspec20k_dr3_catalog.txt', format='ascii.commented_header')

cat.write('cesam_zcosbrightspec20k_dr3_catalog.fits')