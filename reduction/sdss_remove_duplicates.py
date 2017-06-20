# Remove duplicates - keeping objects with SPECPRIMARY==1

from __future__ import division, print_function
import numpy as np
from astropy.io import fits
import fitsio
import time


start = time.clock()

data_path = "/project/projectdirs/desi/users/rongpu/dr3_truth/"
cat_path = data_path+'specObj-dr13.fits'

cat = fits.getdata(cat_path)

mask = cat['SPECPRIMARY']==1
cat = cat[mask]

fits.writeto(data_path+'specObj-dr13-unique.fits', cat, clobber=False)

end = time.clock()
print('%f seconds'%(end-start))
