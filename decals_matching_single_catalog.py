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

start = time.clock()

#################################################################################
dr = '5.0'
sweep_dir = '/global/project/projectdirs/cosmo/data/legacysurvey/dr5/sweep/5.0/'

# dr = '4.0'
# sweep_dir = '/global/project/projectdirs/cosmo/data/legacysurvey/dr4/sweep/4.0/'

# dr = '3.1'
# sweep_dir = '/global/project/projectdirs/cosmo/data/legacysurvey/dr3.1/sweep/3.1/'

parent_dir = '/global/project/projectdirs/desi/users/rongpu/truth/parent/'
output_dir = '/global/project/projectdirs/desi/users/rongpu/truth/dr5.0/mystuff/'
plot_path = '/global/project/projectdirs/desi/users/rongpu/truth/qaplots/dr5.0/decals_match_saga/'

ra_col = 'RA'
dec_col = 'DEC'
search_radius = 1.
cat2_filenames = ['saga_spectra_june2017.fits']
output_filenames = ['decals-dr'+dr+'-saga_spectra_june2017.fits']
ext = None

#################################################################################

save_q = True # save catalog
region_q = True # match only overlapping regions to reduce computation time
correct_offset_q = True
plot_q = True


cat1_paths = sorted(glob.glob(os.path.join(sweep_dir, '*.fits')))

for cat2_index in range(len(cat2_filenames)):

    cat2_filename = cat2_filenames[cat2_index]
    output_filename = output_filenames[cat2_index]
    cat2_path = os.path.join(parent_dir, cat2_filename)
    output_path = os.path.join(output_dir, output_filename)
    print(cat2_filename)

    # -----------------------------------------------------------------------------------------

    cat2 = fitsio.read(cat2_path, columns=[ra_col, dec_col], ext=ext)

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
        if correct_offset_q:
            ra_offset = np.mean(ra2[mask2] - ra1[idx[mask2]])
            dec_offset = np.mean(dec2[mask2] - dec1[idx[mask2]])
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

        #------------------------------removing doubly matched objects------------------------------

        # foo keeps track of cat2 (reduced) index for idx and d2d
        foo = np.arange(len(cat2))
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
            cat1_matchid[idx[mask2]] = bar[foo[mask2]]
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

            d_ra_hist=(cat2[ra_col][mask2full]-cat_stack['RA'][mask2full])*3600    # in arcsec
            d_dec_hist=(cat2[dec_col][mask2full]-cat_stack['DEC'][mask2full])*3600 # in arcsec

            ax = scatter_plot(d_ra_hist, d_dec_hist)
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
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            fitsio.write(output_path, cat_stack, clobber=False)

        end = time.clock()
        if match_count==0:
            print('%f seconds'%(end-start))
        start = end-start

    print('\n------------------------------------------------------\n')