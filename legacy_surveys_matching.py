#!/usr/bin/env python

# Example:
# ./legacy_surveys_matching.py --ls-dr 10.1 --catalog deep2 --field south --output-dir $SCRATCH/truth/ --add-pz --plot-qa

# Match the truth catalogs to Legacy Surveys sweep catalogs;
# Save the following results:
# 1. Boolean arrays (.npy) with the same length as the truth catalogs indicating whether each
#    object has a match;
# 2. Catalogs containing matched objects in FITS format.

# cat1 - multiple catalog files - DECaLS/BASS/MzLS
# cat2 - single or multiple catalog files - the "truth" catalog

# To run this script, e.g. match Legacy Survey DR9.0 North to DEEP2:
# python legacy_surveys_matching.py 9.0 deep2 --field north

from __future__ import division, print_function
# import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sys, os, time, argparse, glob
import fitsio
import argparse, gc
from astropy.table import Table, hstack

from catalog_info import catalog_info
# sys.path.append(os.path.expanduser('~/git/Python/user_modules/'))
from match_coord import match_coord, scatter_plot

time_start = time.perf_counter()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Create LS-matched catalogs.")
parser.add_argument('--ls-dr', required=True, help='DR number of Legacy Surveys')
parser.add_argument('--catalog', required=True, help='truth catalog')
parser.add_argument('--field', required=True, help='choose field: north or south?')
parser.add_argument('--parent-dir', type=str, default='/dvs_ro/cfs/cdirs/desi/target/analysis/truth/parent', help='path to parent/truth catalog directory')
parser.add_argument('--output-dir', type=str, default='/global/cfs/cdirs/desi/target/analysis/truth', help='path to output directory')
parser.add_argument('--yaml-path', type=str, default=None, help='path to YAML file containing truth catalog information and cross-matching parameters')
parser.add_argument('--add-pz', action='store_true', help='add photo-z columns')
parser.add_argument('--plot-qa', action='store_true', help='make QA plots')
args = parser.parse_args()
args.parent_dir = os.path.expandvars(args.parent_dir)
args.output_dir = os.path.expandvars(args.output_dir)
args.yaml_path = os.path.expandvars(args.yaml_path)

region_q = True  # match only overlapping regions to reduce computation time
correct_offset_q = True  # correct for the mean RA/DEC offsets in each sweep brick

if args.yaml_path is None:
    args.yaml_path = os.path.join('truth_catalogs', args.catalog+'.yaml')
cat_info = catalog_info(args.yaml_path, args.ls_dr, args.field)
ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext = cat_info
plot_path = os.path.join(args.output_dir, plot_path)

if args.field!='north' and args.field!='south':
    raise ValueError('field can only be \"north\" or \"south\"!')
sweep_dir = os.path.join('/dvs_ro/cfs/cdirs/cosmo/data/legacysurvey/', 'dr'+args.ls_dr.split('.')[0], args.field, 'sweep', args.ls_dr)
pz_dir = os.path.join('/dvs_ro/cfs/cdirs/cosmo/data/legacysurvey/', 'dr'+args.ls_dr.split('.')[0], args.field, 'sweep', args.ls_dr+'-photo-z')

output_dir_allobjects = os.path.join(args.output_dir, 'dr'+args.ls_dr, args.field, 'allobjects')
output_dir_matched = os.path.join(args.output_dir, 'dr'+args.ls_dr, args.field, 'matched')

if not os.path.exists(output_dir_allobjects):
    os.makedirs(output_dir_allobjects)
if not os.path.exists(output_dir_matched):
    os.makedirs(output_dir_matched)
if not os.path.exists(plot_path):
    os.makedirs(plot_path)

cat1_paths = sorted(glob.glob(os.path.join(sweep_dir, '*.fits')))

for cat2_index in range(len(cat2_fns)):

    # Load truth catalog

    cat2_fn = cat2_fns[cat2_index]
    print(cat2_fn)

    cat2_path = os.path.join(args.parent_dir, cat2_fn)
    cat1_output_fn = cat1_output_fns[cat2_index]
    # cat1_output_path_allobjects = os.path.join(output_dir_allobjects, cat1_output_fn)
    cat1_output_path_allobjects = os.path.join(output_dir_allobjects, cat1_output_fn[:-5]+'.npy')

    cat1_match_output_path = os.path.join(output_dir_matched, cat1_output_fn[:-5]+'-match.fits')
    cat2_output_fn = cat2_fn[:cat2_fn.find('.fits')]+'-match.fits'
    cat2_match_output_path = os.path.join(output_dir_matched, cat2_output_fn)

    if os.path.isfile(cat1_output_path_allobjects):
        print(cat1_output_path_allobjects+' already exist!!!!!!!!!!!!!!')
        sys.exit()
    if os.path.isfile(cat1_match_output_path):
        print(cat1_match_output_path+' already exist!!!!!!!!!!!!!!')
        sys.exit()
    if os.path.isfile(cat2_match_output_path):
        print(cat2_match_output_path+' already exist!!!!!!!!!!!!!!')
        sys.exit()

    cat2 = Table(fitsio.read(cat2_path, ext=ext))

    # Case sensitive if fitsio is used
    ra2full = np.array(cat2[ra_col])
    dec2full = np.array(cat2[dec_col])

    file_count = 0
    total_duplicates = 0

    for cat1_index in range(len(cat1_paths)):

        # Load sweep catalog

        cat1_path = cat1_paths[cat1_index]
        filename = cat1_path[-26:-5]

        # Match only overlapping regions to reduce computation time
        if region_q:
            # Area of the brick from the filename
            # # Reduced sweep files:
            # brick = cat1_path[-28:-13]
            # Original sweep files:
            brick = cat1_path[-20:-5]
            ra1min = float(brick[0:3])
            ra1max = float(brick[8:11])
            dec1min = float(brick[4:7])
            if brick[3]=='m':
                dec1min = -dec1min
            dec1max = float(brick[-3:])
            if brick[-4]=='m':
                dec1max = -dec1max
            mask = (ra2full<ra1max+1/60.) & (ra2full>ra1min-1/60.) & (dec2full<dec1max+1/360.) & (dec2full>dec1min-1/360.)
            if np.sum(mask)==0:
                # print('0 matches')
                continue

            # cat2_idx keeps track of cat2 original index
            cat2_idx = np.arange(len(cat2))
            # keep only cat2 objects in the overlapping region
            ra2 = ra2full[mask]
            dec2 = dec2full[mask]
            cat2_idx = cat2_idx[mask]
            print('%d - '%cat1_index + filename)
            print('%d out of %d objects in cat2 are in the overlapping region'%(np.sum(mask), len(mask)))

        cat1 = Table(fitsio.read(cat1_path, ext=1))

        # Add photo-z's
        if args.add_pz:
            cat1_pz_path = os.path.join(pz_dir, filename+'-pz.fits')
            cat1_pz = Table.read(cat1_pz_path)
            if not np.all(cat1['BRICKID']==cat1_pz['BRICKID']) and np.all(cat1['OBJID']==cat1_pz['OBJID']) and np.all(cat1['RELEASE']==cat1_pz['RELEASE']):
                raise ValueError
            cat1_pz.remove_columns(['BRICKID', 'OBJID', 'RELEASE'])
            cat1 = hstack([cat1, cat1_pz])

        # Remove "DUP" objects
        mask = (cat1['TYPE']!='DUP') & (cat1['TYPE']!='DUP ')
        cat1 = cat1[mask]
        if len(cat1)==0:
            continue

        ra1 = np.array(cat1['RA'])
        dec1 = np.array(cat1['DEC'])

        # Matching catalogs
        print("Matching...")

        idx1, idx2, d2d, d_ra, d_dec = match_coord(ra1, dec1, ra2, dec2, search_radius=search_radius, plot_q=False)
        if len(idx1)==0:
            continue

        # Correct for systematic offsets and match again
        ra_offset, dec_offset = 0., 0.
        # Require at least 100 matches for computing the offsets
        if (correct_offset_q) and (len(idx1)>100):
            print("Matching with offsets corrected...")

            ra_offset = np.mean(d_ra)
            dec_offset = np.mean(d_dec)
            ra1 = ra1 + ra_offset/np.cos(np.mean(dec1[idx1])/180*np.pi)/3600.
            dec1 = dec1 + dec_offset/3600.

            print('RA  offset = %.4f arcsec'%(ra_offset))
            print('Dec offset = %.4f arcsec'%(dec_offset))
            idx1, idx2, d2d, d_ra, d_dec = match_coord(ra1, dec1, ra2, dec2, search_radius=search_radius, plot_q=False)

        if region_q:
            idx2_original = cat2_idx[idx2]
        else:
            idx2_original = np.copy(idx2)

        if file_count==0:
            cat1_match = cat1[idx1]
            # the corresponding indices in cat2 for objects in cat1_match:
            cat1_match_idx2 = np.copy(idx2_original)
        else:
            # identify matched objects in cat2 that had already been matched previously
            mask_duplicate = np.in1d(idx2_original, cat1_match_idx2)
            total_duplicates += np.sum(mask_duplicate)

            idx1 = idx1[~mask_duplicate]
            idx2_original = idx2_original[~mask_duplicate]
            cat1_match = np.concatenate((cat1_match, cat1[idx1]))
            cat1_match_idx2 = np.concatenate((cat1_match_idx2, idx2_original))

        file_count += 1

        if args.plot_qa & (len(idx1)>1):

            markersize = np.max([0.01, np.min([5, 0.2*100000/len(d_ra)])])
            axis = [-search_radius*1.05+ra_offset, search_radius*1.05+ra_offset,
                    -search_radius*1.05+dec_offset, search_radius*1.05+dec_offset]
            ax = scatter_plot(d_ra+ra_offset, d_dec+dec_offset, markersize=markersize, alpha=0.4, axis=axis, show=False)
            if correct_offset_q and (ra_offset!=0) and (dec_offset!=0):
                ax.plot(ra_offset, dec_offset, 'r.', markersize=9)
            plt.savefig(os.path.join(plot_path, '{}_{}.png'.format(cat2_index, brick)))
            plt.close()

    # manual garbage collection
    gc.collect()

    # -----------------------------------------------------------------------------------------

    if file_count==0:
        print('No match with entire survey footprint!')
    else:
        cat1_match = cat1_match[np.argsort(cat1_match_idx2)]
        cat1_match_idx2 = np.sort(cat1_match_idx2)
        cat2_match = cat2[cat1_match_idx2]

        ######################################################################
        # For debugging
        if len(np.unique(cat1_match_idx2))!=len(cat1_match_idx2):
            print('Error!!!!')
            sys.exit()
        ######################################################################

        print('\n%d total matches'%len(cat1_match))
        if total_duplicates>0:
            print('%d total overlapping duplicates'%(total_duplicates))

        # save the boolean array of successful/unsuccessful matches
        bool_array = np.zeros(len(cat2), dtype=bool)
        bool_array[cat1_match_idx2] = True
        np.save(cat1_output_path_allobjects, bool_array)

        print('Fraction of matched objects: {}/{} = {:.2f}%'
              .format(len(cat2_match), len(cat2), 100*len(cat2_match)/len(cat2)))
        print()
        
        cat1_match.write(cat1_match_output_path)
        cat2_match.write(cat2_match_output_path)

        time_end = time.perf_counter()
        print('%.1f seconds'%(time_end-time_start))
        time_start = time_end-time_start

    print('\n------------------------------------------------------\n')
