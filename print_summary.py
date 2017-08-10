# Print the number of matched objects in truth catalogs

from __future__ import division, print_function
import argparse
import numpy as np
from astropy.io import fits
import os

parser = argparse.ArgumentParser()
parser.add_argument('dr')
args = parser.parse_args()
dr = args.dr

top_dir = '/project/projectdirs/desi/target/analysis/truth'
# top_dir = '/global/project/projectdirs/desi/users/rongpu/truth'

input_dir = os.path.join(top_dir, 'dr'+dr+'/trimmed/')

def get_trim_filename(filename):
    if filename[-3:]=='.gz':
        filename = filename[:-8]
    else:
        filename = filename[:-5]
    return filename+'-trim.fits'

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

    file_path = os.path.join(input_dir, get_trim_filename(filelist[index]))

    if os.path.exists(file_path):
        t = fits.getdata(file_path)
        print(filelist[index])
        print(len(t))
        print()