from __future__ import division, print_function
import numpy as np
from astropy.io import fits
import os

dr='4.0'
top_dir = '/project/projectdirs/desi/target/analysis/truth'
# top_dir = '/global/project/projectdirs/desi/users/rongpu/truth'

parent_dir = os.path.join(top_dir, 'parent/')
input_dir = os.path.join(top_dir, 'dr'+dr+'/allmatches/')
output_dir = os.path.join(top_dir, 'dr'+dr+'/trimmed/')

def get_decals_filename(filename):
    if filename[-3:]=='.gz':
        filename = filename[:-3]
    return 'decals-dr'+dr+'-'+filename

filelist = [
    'ages_reduced.fits',
    'COSMOS2015_Laigle+_v1.1.fits',
    'deep2-field1.fits.gz',
    'deep2-field2.fits.gz',
    'deep2-field3.fits.gz',
    'deep2-field4.fits.gz',
    'VIPERS_W1_SPECTRO_PDR2.fits',
    'VIPERS_W4_SPECTRO_PDR2.fits',
    'stripe82-dr12-specz.fits.gz',
    'stripe82-dr12-stars.fits.gz',
    'spies.fits.gz',
    'cfhtls-d2-i.fits.gz',
    'cfhtls-d2-r.fits.gz',
    'cfhtls-d3-i.fits.gz',
    'cfhtls-d3-r.fits.gz',
    'cosmos-acs.fits.gz',
    'AllQSO.DECaLS.dr2.fits',
    'Stars_str82_355_4.DECaLS.dr2.fits',
    'cesam_vvds_spCDFS_DEEP_Full.fits',
    'cesam_vvds_spF02_DEEP_Full.fits',
    'cesam_vvds_spF02_UDEEP_Full.fits',
    'cesam_vvds_spF10_WIDE_Full.fits',
    'cesam_vvds_spF14_WIDE_Full.fits',
    'cesam_vvds_spF22_WIDE_Full.fits',
    'shela_irac_v1.3_flux_cat.fits',
    'alldeep.egs.uniq.2012jun13.fits.gz',
    '3dhst.v4.1.5.master.aegis.fits',
    '3dhst.v4.1.5.master.cosmos.fits',
    '3dhst.v4.1.5.master.goodsn.fits',
    '3dhst.v4.1.5.master.goodss.fits',
    '3dhst.v4.1.5.master.uds.fits',
    'FMOS_COSMOS_v1.0.fits',
    'mosdef_zcat.16aug2016.fits',
    'GAMA-DR2-SpecObj.fits', 
    'wigglez_dr1_unique.fits', 
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
