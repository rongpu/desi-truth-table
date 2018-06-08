from __future__ import division, print_function
import numpy as np
from astropy.table import Table
import fitsio


hsc = fitsio.read('/project/projectdirs/desi/target/analysis/truth/dr5.0/trimmed/hsc_pdr1_wide.forced.reduced-trim.fits')
decals = fitsio.read('/project/projectdirs/desi/target/analysis/truth/dr5.0/trimmed/decals-dr5.0-hsc_pdr1_wide.forced.reduced-trim.fits')
print(len(hsc))
print(len(decals))

regions = ['south_2h', 'south_9h', 'south_12h', 'south_14h', 'south_22h', 'north_14h', 'north_16h']
ra_range = [[0, 50], [100, 150], [150, 200], [200, 250], [300, 350], [200, 225], [225, 250]]

mask_all = np.zeros(len(hsc), dtype=bool)
for index in range(len(regions)):
    region_name = regions[index]
    if region_name.startswith('south'):
        mask = hsc['dec']<30
    else:
        mask = hsc['dec']>30
    mask &= (hsc['ra']>ra_range[index][0]) & (hsc['ra']<ra_range[index][1])
    print(np.sum(mask))

    if np.sum(mask)>0:
        hsc1 = hsc[mask]
        decals1 = decals[mask]
        fitsio.write('/project/projectdirs/desi/target/analysis/truth/dr5.0/trimmed/hsc_pdr1_wide/hsc_pdr1_wide.forced.reduced-trim-{}.fits'.format(region_name), hsc1)
        fitsio.write('/project/projectdirs/desi/target/analysis/truth/dr5.0/trimmed/hsc_pdr1_wide/decals-dr5.0-hsc_pdr1_wide.forced.reduced-trim-{}.fits'.format(region_name), decals1)

    if np.sum(mask_all & mask)!=0:
        print('There is overlap!!!')

    mask_all |= mask

print()
print(np.sum(mask_all))
print(len(hsc))
