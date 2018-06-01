########################################################################
# The code uses the filenames of sweep files as input for RA and Dec   #
# range. Thus changes of the filenames would render the code unusable. #
########################################################################

# Matching between two catalogs
# Use cat1 data to create a catalog that is line-matched to cat2

# Creating line-matched catalogs (all objects in cat2 are kept):
# 1. Find matched objects
# 2. Flag duplicates (objects in cat1 that have more than one match to cat2)
# 3. Rearrange cat1 so that it is line-matched to cat2 and there's no duplicate
# 4. Save the new cat1
# Note:
# - Objects with no match are assigned '' for string and 0 for numbers

# cat1 - multiple catalog files - DECaLS
# cat2 - single or multiple catalog files - the "truth" catalog

# astropy.fits cannot be used because it does not allow this:
# cat_stack[mask2full] = cat1[mask2full]

# To run this script, e.g. match Legacy Survey DR6 to DEEP2:
# python decals_matching 6.0 deep2

from __future__ import division, print_function
import matplotlib
matplotlib.use( "Agg" )
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy.coordinates import SkyCoord
import sys, os, time, argparse, glob
import fitsio
from catalog_info import catalog_info
from catalog_matching_scatter_plot import scatter_plot

time_start = time.clock()

top_dir = '/project/projectdirs/desi/target/analysis/truth'
# top_dir = '/global/project/projectdirs/desi/users/rongpu/truth'

save_q = True # save catalog
region_q = True # match only overlapping regions to reduce computation time
correct_offset_q = True
plot_q = True

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr')
parser.add_argument('catalog')
parser.add_argument("--test", action="store_true")
args = parser.parse_args()
if len(args.ls_dr)!=3:
    raise ValueError('ls_dr not in the correct format!')

sweep_dir = os.path.join('/global/project/projectdirs/cosmo/data/legacysurvey/', 
    'dr'+args.ls_dr[0], 'sweep', args.ls_dr)

# Only 1/10 of the cat2 ojects are used if testing is enabled
testing_q = args.test

cat_info = catalog_info(args.catalog, args.ls_dr)
ra_col, dec_col, search_radius, cat2_fns, cat1_output_fns, plot_path, ext, unique_q = cat_info
plot_path = os.path.join(top_dir, plot_path)

parent_dir = os.path.join(top_dir, 'parent/')
output_dir_allmatches = os.path.join(top_dir, 'dr'+args.ls_dr+'/allmatches/')
output_dir_trimmed = os.path.join(top_dir, 'dr'+args.ls_dr+'/trimmed/')

cat1_paths = sorted(glob.glob(os.path.join(sweep_dir, '*.fits')))

for cat2_index in range(len(cat2_fns)):

    cat2_fn = cat2_fns[cat2_index]
    print(cat2_fn)

    cat2_path = os.path.join(parent_dir, cat2_fn)
    cat1_output_fn = cat1_output_fns[cat2_index]
    cat1_output_path_allmatches = os.path.join(output_dir_allmatches, cat1_output_fn)

    cat1_output_path_trim = os.path.join(output_dir_trimmed, cat1_output_fn[:-5]+'-trim.fits')
    cat2_output_fn = cat2_fn[:cat2_fn.find('.fits')]+'-trim.fits'
    cat2_output_path_trim = os.path.join(output_dir_trimmed, cat2_output_fn)

    if os.path.isfile(cat1_output_path_allmatches):
        print(cat1_output_path_allmatches+' already exist!!!!!!!!!!!!!!')
        exit()
    if os.path.isfile(cat1_output_path_trim):
        print(cat1_output_path_trim+' already exist!!!!!!!!!!!!!!')
        exit()
    if os.path.isfile(cat2_output_path_trim):
        print(cat2_output_path_trim+' already exist!!!!!!!!!!!!!!')
        exit()

    # -----------------------------------------------------------------------------------------

    cat2 = fitsio.read(cat2_path, ext=ext)

    if testing_q:
        cat2 = cat2[::10]

    # Case sensitive if fitsio is used
    ra2full = np.array(cat2[ra_col])
    dec2full = np.array(cat2[dec_col])

        
    file_count = 0
    total_duplicates = 0
    match_count = 0

    for fileindex in range(len(cat1_paths)):

        cat1_path = cat1_paths[fileindex]
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
            # bar keeps track of cat2 original index
            bar = np.arange(len(cat2))
            # keep only cat2 objects in the overlapping region
            ra2 = ra2full[mask]
            dec2 = dec2full[mask]
            bar = bar[mask]
            print('%d - '%fileindex + filename)
            print('%d out of %d objects in cat2 are in the overlapping region'%(np.sum(mask), len(mask)))
        
        cat1 = fitsio.read(cat1_path, ext=1)

        if testing_q:
            cat1 = cat1[::10]

        ra1 = np.array(cat1['RA'])
        dec1 = np.array(cat1['DEC'])

        # Matching catalogs
        print("Matching...")
        skycat1 = SkyCoord(ra1*u.degree,dec1*u.degree, frame='icrs')
        skycat2 = SkyCoord(ra2*u.degree,dec2*u.degree, frame='icrs')
        idx, d2d, _ = skycat2.match_to_catalog_sky(skycat1)
        # For each object in cat2, a closest match to cat1 is found. Thus not all cat1 objects are included. 
        # idx is the cat1 index for cat2 -- idx[0] is the cat1 index that the first cat2 object matched.
        # Similarly d2d is the distance between the matches. 

        mask2 = d2d<(search_radius*u.arcsec)
        if np.sum(mask2)==0:
            print('0 matches')
            continue
        count1 = np.sum(mask2)
        print('Number of initial matches = %d'%count1)

        # Correct for systematic offsets
        ra_offset, dec_offset = 0., 0.
        # Require at least 100 matches for computing the offsets
        if (correct_offset_q) and (np.sum(mask2)>100):
            d_ra = ra2[mask2] - ra1[idx[mask2]]
            d_dec = dec2[mask2] - dec1[idx[mask2]]

            # Deal with pairs that cross RA=0
            mask = d_ra > 180
            d_ra[mask] = d_ra[mask] - 360.
            mask = d_ra < -180
            d_ra[mask] = d_ra[mask] + 360.

            ra_offset = np.mean(d_ra)
            dec_offset = np.mean(d_dec)
            ra1 = ra1 + ra_offset
            dec1 = dec1 + dec_offset

            print('RA  offset = %f arcsec'%(ra_offset*3600))
            print('Dec offset = %f arcsec'%(dec_offset*3600))
            skycat1 = SkyCoord(ra1*u.degree,dec1*u.degree, frame='icrs')
            idx, d2d, _ = skycat2.match_to_catalog_sky(skycat1)
            mask2 = d2d<(search_radius*u.arcsec)
            count1 = np.sum(mask2)
            print('Number of matches after offset correction = %d'%count1)

        notmask2 = ~mask2
        idx[notmask2] = -99

        # foo keeps track of cat2 (reduced) index for idx and d2d
        foo = np.arange(len(idx))

        #---- Only remove doubly matched objects if cat2 is unique (no duplicates) ------------
        if unique_q:
            
            # Sort by idx to find doubly matched objects
            sort_index = idx.argsort()
            idx.sort()
            d2d = d2d[sort_index]
            foo = foo[sort_index]

            # Find the first non-zero idx
            i = np.argmax(idx>=0)
            # Find doubly matched objects, keep only the nearest match
            while i<=len(idx)-2:
                if idx[i]>=0 and idx[i]==idx[i+1]:
                    end = i+1
                    while end+1<=len(idx)-1 and idx[i]==idx[end+1]:
                        end = end+1
                    findmin = np.argmin(d2d[i:end+1])
                    for j in range(i,end+1):
                        if j!=i+findmin:
                            idx[j]=-99
                    i = end+1
                else:
                    i = i+1
            count2 = np.sum(idx>=0)

            print('Number of doubly matched objects = %d'%(count1 - count2))
            print('Number of final matches = %d'%count2)

            # Restore idx and d2d to original order
            sort_index = foo.argsort()
            foo.sort()
            idx = idx[sort_index]
            d2d = d2d[sort_index]

        #--------------------------- create line-matched catalog -----------------------------
        # See Evernote for explanation

        mask2 = idx>=0
        if region_q:
            mask2full = np.zeros(len(cat2), dtype=bool)
            mask2full[bar[mask2]] = True
            notmask2full = ~mask2full
        else:
            mask2full = mask2.copy()
            notmask2full = ~mask2full

        # cat1_matchid is the cat2 (original) index for cat1 objects
        cat1_matchid = -99.*np.ones(len(cat1))
        if region_q:
            cat1_matchid[idx[mask2]] = bar[mask2]
        else:
            cat1_matchid[idx[mask2]] = foo[mask2]
        mask1 = cat1_matchid>=0
        cat1_index = np.arange(len(cat1))
        cat1_matchid = cat1_matchid[mask1]
        cat1_index = cat1_index[mask1]

        sort_index = cat1_matchid.argsort()
        cat1_index = cat1_index[sort_index]
        index_list = np.zeros(len(cat2), dtype=int)
        index_list[mask2full] = cat1_index

        if file_count==0:
            cat_stack = cat1[index_list]
            mask_stack = mask2full.copy()
        else:
            cat_stack[mask2full] = cat1[index_list[mask2full]]
            duplicates = np.sum(mask_stack&mask2full)
            if duplicates>=1:
                print('%d overlapping duplicates'%duplicates)
                total_duplicates = total_duplicates + duplicates
            mask_stack = mask_stack | mask2full

        file_count = file_count+1
        match_count = match_count + np.sum(mask2full)

        if plot_q & (np.sum(mask2full)>1):

            d_ra = (cat2[ra_col][mask2full]-cat_stack['RA'][mask2full])*3600    # in arcsec
            d_dec = (cat2[dec_col][mask2full]-cat_stack['DEC'][mask2full])*3600 # in arcsec
            
            # Deal with pairs that cross RA=0
            mask = d_ra > 180*3600
            d_ra[mask] = d_ra[mask] - 360.*3600
            mask = d_ra < -180*3600
            d_ra[mask] = d_ra[mask] + 360.*3600

            # Convert to actual degrees:
            d_ra = d_ra * np.cos(cat_stack['DEC'][mask2full]/180*np.pi)

            markersize = np.max([0.005, np.min([10, 0.2*100000/np.sum(mask2full)])])
            ax = scatter_plot(d_ra, d_dec, markersize=markersize, alpha=0.4)
            if correct_offset_q and (ra_offset!=0) and (dec_offset!=0):
                ax.plot(ra_offset*3600, dec_offset*3600, 'r.', markersize=9)
            
            if not os.path.exists(plot_path):
                os.makedirs(plot_path)
            plt.savefig(os.path.join(plot_path, '{}_{}.png'.format(cat2_index, brick)))
            plt.close()

    # -----------------------------------------------------------------------------------------

    if match_count==0:
        print('No match with entire DECaLS!')
    else:
        notmask_stack = ~mask_stack
        # For objects with no match, assign '' to strings and 0 to numbers
        for index in range(len(cat_stack.dtype.names)):
            colformat = cat_stack.dtype[index].char
            colname = cat_stack.dtype.names[index]        
            if (colformat.find('S')>=0) or (colformat.find('a')>=0):
                cat_stack[colname][notmask_stack] = ''
            else:
                cat_stack[colname][notmask_stack] = 0

        print('\n%d total matches'%np.sum(mask_stack))
        if total_duplicates>0:
            print('%d total overlapping duplicates'%total_duplicates)

        if save_q:

            # save the full line-matched catalog
            if not os.path.exists(output_dir_allmatches):
                os.makedirs(output_dir_allmatches)

            fitsio.write(cat1_output_path_allmatches, cat_stack, clobber=True)

            # save trimmed catalog: only keeping matched objects
            mask = ~((cat_stack['RA']==0) & (cat_stack['DEC']==0))
            print('fraction of matched objects: {}/{} = {}'
                .format(np.sum(mask), len(cat_stack), np.sum(mask)/len(cat_stack)))
            print()
            cat1_trim = cat_stack[mask]
            cat2_trim = cat2[mask]
            if not os.path.exists(output_dir_trimmed):
                os.makedirs(output_dir_trimmed)
            fitsio.write(cat1_output_path_trim, cat1_trim, clobber=True)
            fitsio.write(cat2_output_path_trim, cat2_trim, clobber=True)

        time_end = time.clock()
        print('%f seconds'%(time_end-time_start))
        time_start = time_end-time_start

    print('\n------------------------------------------------------\n')