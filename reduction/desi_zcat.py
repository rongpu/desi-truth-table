import sys, os, glob, time, warnings
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack, hstack, join
import fitsio

sys.path.append(os.path.expanduser('~/git/Python/user_modules/'))
from match_coord import match_self


for specprod in ['iron', 'loa', 'matterhorn']:

    cat = Table(fitsio.read('/pscratch/sd/r/rongpu/tmp/{}/zcatalog/v2_20260805/zall/zall-pix-{}.fits'.format(specprod, specprod)))
    print(len(cat), len(np.unique(cat['TARGETID'])))

    mask = cat['ZCAT_PRIMARY'].copy()
    cat = cat[mask]
    print(len(cat), len(np.unique(cat['TARGETID'])))

    # Use the score to select which duplicated object to keep
    score = cat['EFFTIME_SPEC'].copy()

    # Booast the score of confident redshifts
    mask = cat['Z_CONF']==3
    print(np.sum(mask), np.sum(mask)/len(mask))
    score[mask] *= 10
    print()

    # Reduce the score of non-main, non-SV, stuck and non-target (mostly stuck and sky) fibers
    mask = ~np.in1d(cat['SURVEY'], ['main', 'sv1', 'sv2', 'sv3'])
    print(np.sum(mask), np.sum(mask)/len(mask))
    mask |= cat['TARGETID'] < 0
    print(np.sum(mask), np.sum(mask)/len(mask))
    mask |= cat['OBJTYPE']!='TGT'
    print(np.sum(mask), np.sum(mask)/len(mask))
    score[mask] /= 10

    n_duplicates = 1

    while n_duplicates>0:
        n_duplicates, idx1, idx2 = match_self(cat['TARGET_RA'], cat['TARGET_DEC'], search_radius=0.5, return_indices=True, plot_q=False)
        if len(idx1)==0:
            continue
        mask_remove1 = (score[idx1] < score[idx2]) | (score[idx1]==0)
        mask_remove2 = (score[idx2] < score[idx1]) | (score[idx2]==0)
        idx_remove = np.unique(np.concatenate([idx1[mask_remove1], idx2[mask_remove2]]))
        print(len(idx_remove), len(idx_remove)/len(idx1))
        mask = np.full(len(cat), True)
        mask[idx_remove] = False
        print(np.sum(mask), np.sum(mask)/len(mask))
        cat = cat[mask]
        score = score[mask]

    cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/zall-pix-{}-unique.fits'.format(specprod))
