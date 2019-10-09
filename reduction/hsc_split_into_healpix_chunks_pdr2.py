from __future__ import division, print_function
import sys, os, warnings, gc
import numpy as np
from astropy.table import Table, vstack, hstack
import fitsio
import healpy as hp

hsc_list = [
'hsc-pdr2-wide-w01',
'hsc-pdr2-wide-w02',
'hsc-pdr2-wide-w03',
'hsc-pdr2-wide-w04',
'hsc-pdr2-wide-w05',
'hsc-pdr2-wide-w06',
'hsc-pdr2-wide-w07',
]

for field in ['north', 'south']:
    
    cat_dir = '/project/projectdirs/desi/target/analysis/truth/dr8.0/{}/matched/'.format(field)
    
    for index in range(len(hsc_list)):
        hsc_fn = hsc_list[index]

        if os.path.isfile(os.path.join(cat_dir, 'ls-dr8.0-'+hsc_fn+'-reduced-match.fits')):

            print(hsc_fn)

            cat1 = fitsio.read(os.path.join(cat_dir, 'ls-dr8.0-'+hsc_fn+'-reduced-match.fits'))
            cat2 = fitsio.read(os.path.join(cat_dir, hsc_fn+'-reduced-match.fits'))

            ra, dec = cat1['RA'], cat1['DEC']
            
            nside = 16
            pix = hp.ang2pix(nside, ra, dec, lonlat=True, nest=True)
            pix_unique = np.unique(pix)

            output_dir = os.path.join(cat_dir, 'hsc-pdr2-wide', hsc_fn)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for pix_i in pix_unique:
                mask = pix==pix_i
                fitsio.write(os.path.join(output_dir, 'ls-dr8.0-'+hsc_fn+'-reduced-match-hp-{}.fits'.format(pix_i)), cat1[mask])
                fitsio.write(os.path.join(output_dir, hsc_fn+'-reduced-match-hp-{}.fits'.format(pix_i)), cat2[mask])

            gc.collect()