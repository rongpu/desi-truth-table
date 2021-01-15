# Fix the data types in SQL-generated FITS catalog
# Remove duplicates

from __future__ import division, print_function
import sys, os, glob, time, warnings, gc
import numpy as np
from astropy.table import Table, vstack, hstack
import fitsio
import match_coord

cat = Table.read('/Users/rongpu/Downloads/OzDES-DR2.fits')
print(len(cat))

# Clean up the FITS table
for col in ['alpha_j2000', 'delta_j2000', 'rmag', 'z']:
    cat[col] = cat[col].astype('float')
cat['qop'] = cat['qop'].astype('int')

# Remove duplicates
ra_col = 'alpha_j2000'
dec_col = 'delta_j2000'

quality_col = 'qop'

# perturb the coordinates so that the 2nd closest match won't be itself
np.random.seed(618)
cat['dec_perturb'] = np.array(cat[dec_col], dtype=np.float64) + np.random.rand(len(cat))*(0.001/3600)

# Assign a random number to break the tie
random = np.random.rand(len(cat))

continue_loop = True
loop = 0
while continue_loop:
    
    print('Loop %d'%loop)
    loop = loop+1

    n_duplicates, idx1, idx2 = match_coord.match_self(cat[ra_col], cat['dec_perturb'], search_radius=1., 
                                                      return_indices=True, plot_q=False)
    
    mask = (cat[quality_col][idx1]<cat[quality_col][idx2]) \
                  | ((cat[quality_col][idx1]==cat[quality_col][idx2]) & (random[idx1]<random[idx2]))
    idx_remove = idx1[mask]    
    cat.remove_rows(idx_remove)
    print('{} objects removed'.format(len(idx_remove)))
    
    if n_duplicates==0:
        continue_loop = False

cat.remove_column('dec_perturb')
print(len(cat))

cat.write('/Users/rongpu/Downloads/OzDES-DR2-reduced.fits')