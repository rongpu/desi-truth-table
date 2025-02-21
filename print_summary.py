# Print the number of matched objects in truth catalogs

# Example: print summary of all DR9.0 truth catalogs:
# python print_summary.py 9.0

# Example: checking a specific DR9.0 truth catalog:
# python print_summary.py 9.0 --catalog deep2

from __future__ import division, print_function
import sys, os, time, argparse, glob
import numpy as np
import fitsio
from astropy.io import fits

from catalog_info import catalog_info

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr')
parser.add_argument('--catalog', required=False, help='(optional) name of truth catalog')
args = parser.parse_args()
ls_dr = args.ls_dr

top_dir = '/global/cfs/cdirs/desi/target/analysis/truth'
# top_dir = '/global/cfs/cdirs/desi/users/rongpu/truth'
parent_dir = os.path.join(top_dir, 'parent/')

end_string = '-match.fits'

if args.catalog is None:
    # catalogs = ["hsc-dr3.yaml"]
    catalog_fns = sorted(glob.glob('truth_catalogs/*.yaml'))
else:
    catalog_fns = ['truth_catalogs/'+args.catalog+'.yaml']

for field in ['north', 'south']:

    print('\n------------------------------------------------------')
    print('------------------------------------------------------\n')
    print('DR'+ls_dr+' '+field)
    print('-----------\n')

    output_dir_matched = os.path.join(top_dir, 'dr'+ls_dr, field, 'matched')

    for index in range(len(catalog_fns)):

        catalog_fn = catalog_fns[index]
        catalog = os.path.basename(catalog_fn).rstrip('.yaml')
        print(catalog)

        cat_info = catalog_info(catalog_fn, ls_dr, field=field)
        ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext = cat_info

        for cat2_index in range(len(cat2_fns)):

            cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)
            cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)

            cat2_fn = cat2_fns[cat2_index]
            cat2_path = os.path.join(parent_dir, cat2_fn)

            if os.path.isfile(cat1_output_path_trim):
                cat2 = fitsio.read(cat2_path, ext=ext, columns=[ra_col])
                t = fits.getdata(cat1_output_path_trim)
                print('{}  {} ({:.2f}%)'.format(cat2_fn, len(t), 100*len(t)/len(cat2)))
            else:
                print(cat2_fn, ' No match')
                continue

        print('\n------------------------------------------------------\n')

