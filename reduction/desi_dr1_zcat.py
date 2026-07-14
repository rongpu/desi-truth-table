import sys, os, glob, time, warnings
import numpy as np
from astropy.table import Table, vstack, hstack, join
import fitsio

cat = Table(fitsio.read('/pscratch/sd/r/rongpu/tmp/iron/zcatalog/v2/zall/zall-tilecumulative-iron.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

mask = cat['ZCAT_PRIMARY'].copy()
cat = cat[mask]
print(len(cat), len(np.unique(cat['TARGETID'])))

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/zall-tilecumulative-iron-unique.fits')
