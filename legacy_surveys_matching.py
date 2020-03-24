# Match the truth catalogs to Legacy Surveys sweep catalogs;
# Save the following results:
# 1. Boolean arrays (.npy) with the same length as the truth catalogs indicating whether each
#    object has a match;
# 2. Catalogs containing matched objects in FITS format.

# cat1 - multiple catalog files - DECaLS/BASS/MzLS
# cat2 - single or multiple catalog files - the "truth" catalog

# To run this script, e.g. match Legacy Survey DR8.0 North to DEEP2:
# python legacy_surveys_matching.py 8.0 deep2 --field north

from __future__ import division, print_function
import matplotlib
matplotlib.use( "Agg" )
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
import sys, os, time, argparse, glob
import fitsio
import gc

from catalog_info import catalog_info
from match_coord import match_coord, scatter_plot

time_start = time.clock()

parent_dir = '/project/projectdirs/desi/target/analysis/truth/parent'
output_dir = '/project/projectdirs/desi/target/analysis/truth'
# output_dir = '/global/cscratch1/sd/rongpu/truth'

region_q = True # match only overlapping regions to reduce computation time
correct_offset_q = True
plot_q = True
predr8 = False

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr', help='DR number of Legacy Surveys')
parser.add_argument('catalog', help='truth catalog')
parser.add_argument('--field', help='choose field: north or south?')
args = parser.parse_args()

#######################################
# if len(args.ls_dr)!=3:
#     raise ValueError('ls_dr not in the correct format!')
#######################################

cat_info = catalog_info(args.catalog, args.ls_dr, args.field)
ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext = cat_info
plot_path = os.path.join(output_dir, plot_path)
if not os.path.exists(plot_path):
    os.makedirs(plot_path)

if not predr8:
    if args.field=='north':
        field_dir = 'north'
    elif args.field=='south':
        field_dir = 'south'
    else:
        raise ValueError('field can only be \"north\" or \"south\"!')
    sweep_dir = os.path.join('/global/project/projectdirs/cosmo/data/legacysurvey/', 
        'dr'+args.ls_dr[0], field_dir, 'sweep', args.ls_dr)
    output_dir_allobjects = os.path.join(output_dir, 'dr'+args.ls_dr, field_dir, 'allobjects')
    output_dir_matched = os.path.join(output_dir, 'dr'+args.ls_dr, field_dir, 'matched')
else:
    sweep_dir = os.path.join('/global/project/projectdirs/cosmo/data/legacysurvey/', 
        'dr'+args.ls_dr[0], 'sweep', args.ls_dr)
    output_dir_allobjects = os.path.join(output_dir, 'dr'+args.ls_dr+'/allobjects/')
    output_dir_matched = os.path.join(output_dir, 'dr'+args.ls_dr+'/matched/')

if not os.path.exists(output_dir_allobjects):
    os.makedirs(output_dir_allobjects)
if not os.path.exists(output_dir_matched):
    os.makedirs(output_dir_matched)

cat1_paths = sorted(glob.glob(os.path.join(sweep_dir, '*.fits')))

for cat2_index in range(len(cat2_fns)):

    # Load truth catalog

    cat2_fn = cat2_fns[cat2_index]
    print(cat2_fn)

    cat2_path = os.path.join(parent_dir, cat2_fn)
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

    cat2 = fitsio.read(cat2_path, ext=ext)

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
        
        cat1 = fitsio.read(cat1_path, ext=1)

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

        if plot_q & (len(idx1)>1):

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
        fitsio.write(cat1_match_output_path, cat1_match, clobber=True)
        fitsio.write(cat2_match_output_path, cat2_match, clobber=True)

        time_end = time.clock()
        print('%.1f seconds'%(time_end-time_start))
        time_start = time_end-time_start

    print('\n------------------------------------------------------\n')