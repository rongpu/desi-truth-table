# remove "_isnull" columns;
# hstack the catalogs (originally separated to circumvent the SQL size limit)

from __future__ import division, print_function
import sys, os, time, argparse, glob, gc
import numpy as np
from astropy.table import Table, hstack
import fitsio

cat_dir = '/global/cscratch1/sd/rongpu/temp/parent'

hsc_list = ['hsc-pdr2-dud-cosmos',
            'hsc-pdr2-dud-deep2_3',
            'hsc-pdr2-dud-elais_n1',
            'hsc-pdr2-dud-sxds',
            'hsc-pdr2-dud-xmm_lss',
            'hsc-pdr2-wide-w01',
            'hsc-pdr2-wide-w02',
            'hsc-pdr2-wide-w03',
            'hsc-pdr2-wide-w04',
            'hsc-pdr2-wide-w05',
            'hsc-pdr2-wide-w06',
            'hsc-pdr2-wide-w07',]
suffix_list = ['1', '2']

for index1 in range(len(hsc_list)):
    cat_hstack = []
    for index2 in range(len(suffix_list)):

        fn = hsc_list[index1]+'-'+suffix_list[index2]+'.fits'
        print(fn)

        cat = fitsio.read(os.path.join(cat_dir, 'original', fn))
        cat = Table(cat)
        print(len(cat))

        for colname in cat.colnames:
            if colname.endswith('_isnull'):
                cat.remove_column(colname)

        if index2!=0:
            if not np.all(cat_hstack[0]['object_id']==cat['object_id']):
                raise ValueError('object_id do not match for '+fn)
            cat.remove_column('object_id')

        cat_hstack.append(cat)

    cat_hstack = hstack(cat_hstack)
    cat_hstack.write(os.path.join(cat_dir, hsc_list[index1]+'-reduced.fits'))

    gc.collect()
