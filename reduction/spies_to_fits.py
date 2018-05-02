# SpIES first data release
# Convert the ascii tables to FITS format

from __future__ import division, print_function
import numpy as np
from astropy.table import Table

t = Table.read('/project/projectdirs/desi/target/analysis/truth/parent/original/SpIES_ch1_only.tbl.gz', format='ipac')

FLAGS_ch1 = np.zeros((len(t), 2))
COV_ch1 = np.zeros((len(t), 2))

for index in range(len(t)):
    FLAGS_ch1[index] = np.array(t['FLAGS_ch1'][index][1:-1].split(','), dtype=float)
    COV_ch1[index] = np.array(t['COV_ch1'][index][1:-1].split(','), dtype=float)
    
t['FLAGS_ch1'] = FLAGS_ch1
t['COV_ch1'] = COV_ch1

t.write('/project/projectdirs/desi/target/analysis/truth/parent/SpIES_ch1_only.fits')

####################################################################################################

t = Table.read('/project/projectdirs/desi/target/analysis/truth/parent/original/SpIES_ch1andch2.tbl.gz', format='ipac')

FLAGS_ch1 = np.zeros((len(t), 2))
COV_ch1 = np.zeros((len(t), 2))
FLAGS_ch2 = np.zeros((len(t), 2))
COV_ch2 = np.zeros((len(t), 2))

for index in range(len(t)):
    FLAGS_ch1[index] = np.array(t['FLAGS_ch1'][index][1:-1].split(','), dtype=float)
    COV_ch1[index] = np.array(t['COV_ch1'][index][1:-1].split(','), dtype=float)
    FLAGS_ch2[index] = np.array(t['FLAGS_ch2'][index][1:-1].split(','), dtype=float)
    COV_ch2[index] = np.array(t['COV_ch2'][index][1:-1].split(','), dtype=float)
    
t['FLAGS_ch1'] = FLAGS_ch1
t['COV_ch1'] = COV_ch1
t['FLAGS_ch2'] = FLAGS_ch2
t['COV_ch2'] = COV_ch2

t.write('/project/projectdirs/desi/target/analysis/truth/parent/SpIES_ch1andch2.fits')

