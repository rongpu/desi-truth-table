# Trim (remove unmatched objects of) single-survey matched catalogs

from __future__ import division, print_function
import numpy as np
from astropy.io import fits
import os

dr='5.0'
# top_dir = '/project/projectdirs/desi/target/analysis/truth'
top_dir = '/global/project/projectdirs/desi/users/rongpu/truth'

parent_dir = os.path.join(top_dir, 'parent/')
# input_dir = os.path.join(top_dir, 'dr'+dr+'/allmatches/')
input_dir = os.path.join(top_dir, 'dr'+dr+'/mystuff/')
output_dir = os.path.join(top_dir, 'dr'+dr+'/trimmed/')

def get_decals_filename(filename):
    if filename[-3:]=='.gz':
        filename = filename[:-3]
    return 'decals-dr'+dr+'-'+filename

filelist = [
    'saga_spectra_june2017.fits'
]


for index in range(len(filelist)):

    print(filelist[index])

    spec_filename = filelist[index]
    decals_filename = get_decals_filename(spec_filename)

    decals_path = os.path.join(input_dir, decals_filename)
    spec_path = os.path.join(parent_dir, spec_filename)
    decals_output_path = os.path.join(output_dir, decals_filename[:-5]+'-trim.fits')
    spec_output_filename = spec_filename[:spec_filename.find('.fits')]+'-trim.fits'
    spec_output_path = os.path.join(output_dir, spec_output_filename)

    if not os.path.exists(decals_path):
        print('No match')
    elif os.path.isfile(spec_output_path):
        print('Trimmed files already exist')
    else:
        cat1 = fits.getdata(decals_path)
        cat2 = fits.getdata(spec_path)

        notmask = (cat1['RA']==0) & (cat1['DEC']==0)
        mask = ~notmask
        print('fraction of matched objects: {}/{} = {}'.format(np.sum(mask), len(cat1), np.sum(mask)/len(cat1)))
        cat1 = cat1[mask]
        cat2 = cat2[mask]

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        fits.writeto(decals_output_path, cat1)
        fits.writeto(spec_output_path, cat2)
