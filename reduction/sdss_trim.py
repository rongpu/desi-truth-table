# Remove duplicates - keeping objects with SPECPRIMARY==1
# Keep only columns that are relevant

from __future__ import division, print_function
import numpy as np
# from astropy.io import fits
import fitsio
from astropy.table import Table

data_path = '/global/projecta/projectdirs/desi/target/analysis/truth/parent/original/'
cat_path = data_path+'sdss-specObj-dr16.fits'

columns = ['SURVEY', 'INSTRUMENT', 'PROGRAMNAME', 'SPECPRIMARY', 'SPECOBJID', 'FLUXOBJID', 'BESTOBJID', 'PLATE', 'MJD', 'FIBERID', 'OBJID', 'PLUG_RA', 'PLUG_DEC', 'CLASS', 'SUBCLASS', 'Z', 'Z_ERR', 'RCHI2', 'DOF', 'RCHI2DIFF', 'ZWARNING', 'SN_MEDIAN_ALL']
cat = fitsio.read(cat_path, columns=columns)

mask = cat['SPECPRIMARY']==1
print(np.sum(mask), np.sum(mask)/len(mask))
cat = cat[mask]

fitsio.write('/global/projecta/projectdirs/desi/target/analysis/truth/parent/sdss-specObj-dr16-unique-trimmed.fits', cat)