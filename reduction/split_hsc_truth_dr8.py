from __future__ import division, print_function
import os, sys
import numpy as np
from astropy.table import Table
import fitsio

dr = '8.0'

regions = ['south_2h', 'south_9h', 'south_12h', 'south_14h', 'south_22h', 'north_14h', 'north_16h']
ra_range = [[0, 50], [100, 150], [150, 200], [200, 250], [300, 350], [200, 225], [225, 250]]

for field in ['north', 'south']:

    print('\n------------------------------------------------------')
    print('------------------------------------------------------\n')
    print('DR'+dr+' '+field)
    print('-----------\n')

    matched_dir = os.path.join('/project/projectdirs/desi/target/analysis/truth/dr'+dr, field, 'matched')

    hsc = fitsio.read(os.path.join(matched_dir, 'hsc_pdr1_wide.forced.reduced-match.fits'))
    ls = fitsio.read(os.path.join(matched_dir, 'ls-dr'+dr+'-hsc_pdr1_wide.forced.reduced-match.fits'))
    print(len(hsc))
    print(len(ls))

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
            ls1 = ls[mask]

            if not os.path.exists(os.path.join(matched_dir, 'hsc_pdr1_wide')):
                os.makedirs(os.path.join(matched_dir, 'hsc_pdr1_wide'))

            fitsio.write(os.path.join(matched_dir, 'hsc_pdr1_wide/hsc_pdr1_wide.forced.reduced-match-{}.fits'.format(region_name)), hsc1)
            fitsio.write(os.path.join(matched_dir, 'hsc_pdr1_wide/ls-dr'+dr+'-hsc_pdr1_wide.forced.reduced-match-{}.fits'.format(region_name)), ls1)

        if np.sum(mask_all & mask)!=0:
            print('There is overlap!!!')

        mask_all |= mask

    print()
    print(np.sum(mask_all))
    print(len(hsc))
