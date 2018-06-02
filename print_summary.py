# Print the number of matched objects in truth catalogs

from __future__ import division, print_function
import sys, os, time, argparse, glob
import numpy as np
import fitsio
from astropy.io import fits

from catalog_info import catalog_info

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr')
args = parser.parse_args()

top_dir = '/project/projectdirs/desi/target/analysis/truth'
# top_dir = '/global/project/projectdirs/desi/users/rongpu/truth'

output_dir_trimmed = os.path.join(top_dir, 'dr'+args.ls_dr+'/trimmed/')

catalogs = sorted(glob.glob('truth_catalogs/*.yaml'))
catalogs = [string[15:-5] for string in catalogs]

for index in range(len(catalogs)):

    print(catalogs[index])
    
    cat_info = catalog_info(catalogs[index], args.ls_dr)
    _, _, _, cat2_fns, cat1_output_fns, _, _ = cat_info

    for cat2_index in range(len(cat2_fns)):
        
        cat2_fn = cat2_fns[cat2_index]

        cat1_output_path_trim = os.path.join(output_dir_trimmed, cat1_output_fns[cat2_index][:-5]+'-trim.fits')

        if os.path.isfile(cat1_output_path_trim):
            t = fits.getdata(cat1_output_path_trim)
            print(cat2_fn, len(t))
        else:
            print(cat2_fn, 'No match')
    print('\n------------------------------------------------------\n')