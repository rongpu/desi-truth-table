from __future__ import division, print_function
import sys, os, glob, time, warnings, gc
import numpy as np
# import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.table import Table, vstack, hstack, join
import fitsio
# from astropy.io import fits


cat = Table.read('/global/cfs/cdirs/desi/target/analysis/truth/parent/original/cesam_zcosbrightspec20k_dr3_catalog.csv')
cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/cesam_zcosbrightspec20k_dr3_catalog.fits')
