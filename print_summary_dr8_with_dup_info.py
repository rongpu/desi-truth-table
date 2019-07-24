# Print the number of matched objects in truth catalogs
# Example: DR8.0 truth catalogs:
# python print_summary.py 8.0

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
parent_dir = os.path.join(top_dir, 'parent/')

end_string = '-match.fits'

catalogs = sorted(glob.glob('truth_catalogs/*.yaml'))
catalogs = [string[15:-5] for string in catalogs]

for field in ['north', 'south']:

    print('\n------------------------------------------------------')
    print('------------------------------------------------------\n')
    print('DR'+args.ls_dr+' '+field)
    print('-----------\n')

    output_dir_matched = os.path.join(top_dir, 'dr'+args.ls_dr, field, 'matched')

    for index in range(len(catalogs)):

        print(catalogs[index])
        
        cat_info = catalog_info(catalogs[index], args.ls_dr, field=field)
        ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext = cat_info

        for cat2_index in range(len(cat2_fns)):
            
            cat2_fn = cat2_fns[cat2_index]
            cat2_path = os.path.join(parent_dir, cat2_fn)
            cat2 = fitsio.read(cat2_path, ext=ext, columns=[ra_col])

            cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)
            cat1_output_path_trim = os.path.join(output_dir_matched, cat1_output_fns[cat2_index][:-5]+end_string)

            if os.path.isfile(cat1_output_path_trim):
                t = fitsio.read(cat1_output_path_trim)
                print('{}  {}  {:.2f}%'.format(cat2_fn, len(t), 100*len(t)/len(cat2)))
                mask = (t['TYPE']==b'DUP') | (t['TYPE']==b'DUP ') | (t['TYPE']=='DUP') | (t['TYPE']=='DUP ')
                print('{} DUP {}  {:.2f}%'.format(cat2_fn, np.sum(mask), 100*np.sum(mask)/len(t)))
            else:
                print(cat2_fn, ' No match')
        print('\n------------------------------------------------------\n')

