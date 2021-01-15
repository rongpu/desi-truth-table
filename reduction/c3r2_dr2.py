# Add RA and DEC in degrees
# Remove duplicates

from __future__ import division, print_function
import sys, os, glob, time, warnings, gc
import numpy as np
from astropy.table import Table, vstack, hstack
import fitsio
import match_coord

cat = Table.read('/Users/rongpu/Downloads/c3r2_DR1+DR2_2019april11.txt', format='ascii')
print(len(cat))

# Add RA and DEC in degrees
cat['ra'] = np.array(cat['RAh']*15 + cat['RAm']/4. + cat['RAs']/240.)
cat['dec'] = np.array(cat['DEd'] + cat['DEm']/60. + cat['DEs']/3600.)
cat['dec'][cat['DE-']=='-'] *= -1

# Remove duplicates
ra_col = 'ra'
dec_col = 'dec'
quality_col = 'Qual'

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

cat.remove_columns(['dec_perturb'])
print(len(cat))

cat.write('/Users/rongpu/Downloads/c3r2_DR1+DR2_2019april11-reduced.fits')