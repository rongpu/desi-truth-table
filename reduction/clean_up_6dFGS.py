from __future__ import print_function, division
import numpy as np
import sys, os
from astropy.table import Table
import fitsio

cat = Table.read('/Users/roz18/Downloads/6dFGS_vizier.fits')
cat.rename_column('_RAJ2000', 'RAJ2000')
cat.rename_column('_DEJ2000', 'DEJ2000')
cat.rename_column('_6dFGS', '6dFGS')
cat.write('/Users/roz18/Downloads/6dFGS.fits')