# Remove duplicates

# From the paper: (arxiv.org/abs/1608.02668v1)
# These flag values respectively indicate: unknown redshift (Q = 1), a possible but uncertain 
# redshift (Q = 2), a probably correct redshift derived from noisy data or fewer spectral 
# features (Q = 3), a secure redshift confirmed by multiple spectral features (Q = 4), and a 
# spectrum that is clearly not ex- tragalactic (Q = 6). The science analyses described in this 
# paper use Q = 3 and Q = 4 spectra. The classification Q = 5 is not used.

from __future__ import division, print_function
import numpy as np
from astropy import units as u
from astropy.table import Table
from astropy.coordinates import SkyCoord
import sys


# search radius in arcsec
search_radius = 1.

ra_col = 'R.A.'
dec_col = 'Dec.'
z_col = 'z'
quality_col = 'qual'

cat = Table.read('/Users/roz18/Desktop/test/2dflens_bestredshifts_goodz_withtypesandmags_final.dat', format='ascii')

cat['qual'] = np.array(cat['qual'], dtype='int32')
cat['target'] = np.array(cat['target'], dtype='int32')

len0 = len(cat)
print('%d objects in the original catalog'%(len0))

ra = np.array(cat[ra_col])
dec = np.array(cat[dec_col])
z = np.array(cat[z_col])
quality = np.array(cat[quality_col])

skycat = SkyCoord(ra*u.degree,dec*u.degree, frame='icrs')
idx, d2d, _ = skycat.match_to_catalog_sky(skycat, nthneighbor=2)

mask_duplicates = d2d<(search_radius*u.arcsec)
print('%d duplicates'%np.sum(mask_duplicates))

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---

# Assign a random number to resolve conflict if quality is the same
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

    mask_remove = mask_duplicates & ((quality<quality[idx]) | (quality==6) | ((quality==quality[idx]) & (random>random[idx])))
    mask_keep = ~mask_remove
    ra = ra[mask_keep]
    dec = dec[mask_keep]
    quality = quality[mask_keep]
    random = random[mask_keep]
    cat_index = cat_index[mask_keep]
    print('%d objects removed'%np.sum(mask_remove))

    if np.sum(mask_remove)==0:
        continue_loop = False

print('Total of %d duplicates removed'%(len(cat)-len(cat_index)))
print('%d objects remaining'%len(cat))

cat = cat[cat_index]
cat.write('/Users/roz18/Desktop/test/2dflens.fits')
