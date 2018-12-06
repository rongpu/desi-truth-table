# Convert the Stripe 82 massive galaxy catalog from Alexie Leauthaud (private communication) to FITS format

from __future__ import division, print_function
import os, sys
import numpy as np
from astropy.table import Table

# Stripe 82 massive galaxy catalog
cat_path = os.path.join(os.getenv('DATA_PATH'), 'desi_lrg_selection/misc/bundy2015_stripe82_massivegalaxy_catalog.txt')
cat = Table.read(cat_path, format='ascii.no_header')
print(len(cat))

cat.rename_column('col1', 'RA')
cat.rename_column('col2', 'DEC')
cat.rename_column('col3', 'zbest')
cat.rename_column('col4', 'mstar')

cat.write(os.path.join(os.getenv('DATA_PATH'), 'desi_lrg_selection/misc/bundy2015_stripe82_massivegalaxy_catalog.fits'))