# Remove duplicates

from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy.coordinates import SkyCoord
from matplotlib.ticker import NullFormatter
import fitsio
import sys
from catalog_matching_scatter_plot import scatter_plot

# search radius in arcsec
search_radius = 1.

data_path = '/project/projectdirs/desi/users/rongpu/dr3_truth/'
cat_path = data_path+'ages_original.fits'

ra_col = 'RAJ2000'
dec_col = 'DEJ2000'
z_col = 'z1'
# Signal-to-noise
sn = 'S_N1'

cat = fits.getdata(cat_path)

len0 = len(cat)
print('%d objects in the original catalog'%(len0))

ra = np.array(cat[ra_col])
dec = np.array(cat[dec_col])
z = np.array(cat[z_col])
sn = np.array(cat[sn])

skycat = SkyCoord(ra*u.degree,dec*u.degree, frame='icrs')
idx, d2d, _ = skycat.match_to_catalog_sky(skycat, nthneighbor=2)

mask_duplicates = d2d<(search_radius*u.arcsec)
print('%d duplicates'%np.sum(mask_duplicates))

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---

# Assign a random number to resolve conflict if sn is the same
random = np.random.rand(len(cat))

cat_index = np.arange(len(cat))
# Repeatedly remove duplicates until no more duplicates
continue_loop = True
loop = 0
while continue_loop:

    print('Loop %d'%loop)
    loop = loop+1

    skycat = SkyCoord(ra*u.degree,dec*u.degree, frame='icrs')
    idx, d2d, _ = skycat.match_to_catalog_sky(skycat, nthneighbor=2)

    mask_duplicates = d2d<(search_radius*u.arcsec)
    print('%d duplicates'%np.sum(mask_duplicates))

    mask_remove = mask_duplicates & ((sn<sn[idx]) | ((sn==sn[idx]) & (random>random[idx])))
    mask_keep = ~mask_remove
    ra = ra[mask_keep]
    dec = dec[mask_keep]
    sn = sn[mask_keep]
    random = random[mask_keep]
    cat_index = cat_index[mask_keep]
    print('%d objects removed'%np.sum(mask_remove))

    if np.sum(mask_remove)==0:
        continue_loop = False

print('Total of %d duplicates removed'%(len(cat)-len(cat_index)))
print('%d objects remaining'%len(cat))
cat = cat[cat_index]
fits.writeto(data_path+'ages_reduced.fits', cat, clobber=False)
