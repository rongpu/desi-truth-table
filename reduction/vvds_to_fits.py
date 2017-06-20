from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
import os, sys

filelist = ['cesam_vvds_spCDFS_DEEP_Full.txt',
        'cesam_vvds_spF10_WIDE_Full.txt',
        'cesam_vvds_spF02_DEEP_Full.txt',
        'cesam_vvds_spF14_WIDE_Full.txt',
        'cesam_vvds_spF02_UDEEP_Full.txt',
        'cesam_vvds_spF22_WIDE_Full.txt']

input_dir = '/project/projectdirs/desi/target/analysis/truth/original/'
output_dir = '/project/projectdirs/desi/target/analysis/truth/dr3.1/allmatches'
misc_dir = '/global/u2/r/rongpu/svn/target-truth/trunk/misc/'

for index, filename in enumerate(filelist):
    print(filename)
    
    # Read column names from catalog
    # with open(os.path.join(input_dir, filename), 'r') as f:
    #     line = f.readline()
    #     while line.startswith('# NUM')==False:
    #         line = f.readline()
    # columnss = line.split()[1:]

    # Read the modified column names from file
    with open(os.path.join(misc_dir, filename[:-4]+'_columns.txt'), 'r') as f:
        columns = map(str.rstrip, f.readlines())
    print(len(columns))
    
    cat = Table.read(os.path.join(input_dir, filename), format='ascii')
    if len(cat.colnames)!=len(columns):
        print('ERROR: length of column names list does not match the number of columns in the catalog')
        sys.exis()
        
    for col_index, cat_col in enumerate(cat.colnames):
        cat.rename_column(cat_col, columns[col_index])
    cat.write(os.path.join(output_dir, filename[:-4]+'.fits'))
