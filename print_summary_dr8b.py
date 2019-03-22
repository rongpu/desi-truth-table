# Special version for internal release DR8b

# Print the number of matched objects in truth catalogs
# Example: DR8b North truth catalogs:
# python print_summary.py 8b north

from __future__ import division, print_function
import sys, os, time, argparse, glob
import numpy as np
import fitsio
from astropy.io import fits

from catalog_info import catalog_info

top_dir = '/project/projectdirs/desi/target/analysis/truth'
# output_dir = '/project/projectdirs/desi/target/analysis/truth'
output_dir = '/global/cscratch1/sd/rongpu/truth'

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr')
parser.add_argument('field')
args = parser.parse_args()

if args.field=='north':
    field_dir = '90prime-mosaic'
elif args.field=='south':
    field_dir = 'decam'
else:
    raise ValueError('field can only be \"north\" or \"south\"!')

parent_dir = os.path.join(top_dir, 'parent/')

output_dir_matched = os.path.join(output_dir, 'dr'+args.ls_dr, field_dir, 'matched')
end_string = '-match.fits'

catalogs = sorted(glob.glob('truth_catalogs/*.yaml'))
catalogs = [string[15:-5] for string in catalogs]

for index in range(len(catalogs)):

    print(catalogs[index])
    
    cat_info = catalog_info(catalogs[index], args.ls_dr)
    ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext = cat_info

    for cat2_index in range(len(cat2_fns)):
        
        cat2_fn = cat2_fns[cat2_index]
        cat2_path = os.path.join(parent_dir, cat2_fn)
        cat2 = fitsio.read(cat2_path, ext=ext, columns=[ra_col])

        cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)
        cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)

        if os.path.isfile(cat1_output_path_trim):
            t = fits.getdata(cat1_output_path_trim)
            print('{}  {}  {:.2f}%'.format(cat2_fn, len(t), 100*len(t)/len(cat2)))
        else:
            print(cat2_fn, ' No match')
    print('\n------------------------------------------------------\n')

