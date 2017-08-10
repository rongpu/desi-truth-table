from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
import fitsio
from astropy.table import Table
import sys

columns = ['PLATE', 'MJD', 'FIBERID', 'PLUG_RA', 'PLUG_DEC']
print('Loading...')
cat1 = fitsio.read('/project/projectdirs/desi/users/rongpu/truth/parent/spAll-v5_10_0.fits', columns=columns)
cat2 = Table.read('/project/projectdirs/desi/users/rongpu/truth/parent/eBOSS-DR14-redmonsterAll-v5_10_0.fits')
print('Loading complete')

ra2 = np.zeros(len(cat2))
dec2 = np.zeros(len(cat2))

plate1 = cat1['PLATE']
mjd1 = cat1['MJD']
fiberid1 = cat1['FIBERID']
ra1 = cat1['PLUG_RA']
dec1 = cat1['PLUG_DEC']
plate2 = cat2['PLATE']
mjd2 = cat2['MJD']
fiberid2 = cat2['FIBERID']+1

progress = 0.
l2 = len(cat2)

mask_nomatch = np.zeros(l2, dtype=bool)

for index in range(l2):
    # match_index = np.intersect1d(np.intersect1d(np.where(plate2[index]==plate1), np.where(mjd2[index]==mjd1)), np.where(fiberid2[index]==fiberid1))
    mjd_match = np.where(mjd2[index]==mjd1)[0]
    match_index = np.intersect1d(np.where(plate2[index]==plate1[mjd_match]), np.where(fiberid2[index]==fiberid1[mjd_match]))
    if len(match_index)!=1:
        print('Error: %d matches for object %d'%(len(match_index), index))
        mask_nomatch[index] = True
        ra2[index] = 0.
        dec2[index] = 0.
        # sys.exit()
    else:
        match_index = match_index[0]
        ra2[index] = ra1[mjd_match[match_index]]
        dec2[index] = dec1[mjd_match[match_index]]

    if index/l2>=(progress/100):
        print('%2.1f percent done'%progress)
        progress = progress+0.1
    
cat2['RA'] = ra2
cat2['DEC'] = dec2

print(np.sum(mask_nomatch), 'objects without RA/Dec')
cat2 = cat2[~mask_nomatch]

cat2.write('/project/projectdirs/desi/users/rongpu/truth/parent/eBOSS-DR14-redmonsterAll-v5_10_0-radec-added.fits')

