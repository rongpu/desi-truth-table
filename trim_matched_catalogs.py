from __future__ import division, print_function
import numpy as np
from astropy.io import fits
import os

dr='4.0'
top_dir = '/project/projectdirs/desi/target/analysis/truth'

parent_dir = os.path.join(top_dir, 'parent/')
input_dir = os.path.join(top_dir, 'dr'+dr+'/allmatches/')
output_dir = os.path.join(top_dir, 'dr'+dr+'/trimmed/')

filelist = [
     ['decals-dr'+dr+'-ages.fits', 'ages_reduced.fits'],
     ['decals-dr'+dr+'-cosmos-zphot.fits', 'COSMOS2015_Laigle+_v1.1.fits'],
     ['decals-dr'+dr+'-deep2-field1.fits', 'deep2-field1.fits.gz'],
     ['decals-dr'+dr+'-deep2-field2.fits', 'deep2-field2.fits.gz'],
     ['decals-dr'+dr+'-deep2-field3.fits', 'deep2-field3.fits.gz'],
     ['decals-dr'+dr+'-deep2-field4.fits', 'deep2-field4.fits.gz'],
     ['decals-dr'+dr+'-VIPERS_W1_SPECTRO_PDR2.fits', 'VIPERS_W1_SPECTRO_PDR2.fits'],
     ['decals-dr'+dr+'-VIPERS_W4_SPECTRO_PDR2.fits', 'VIPERS_W4_SPECTRO_PDR2.fits'],
     ['decals-dr'+dr+'-stripe82-specz.fits', 'stripe82-dr12-specz.fits.gz'],
     ['decals-dr'+dr+'-stripe82-stars.fits', 'stripe82-dr12-stars.fits.gz'],
     ['decals-dr'+dr+'-spies.fits', 'spies.fits.gz'],
     ['decals-dr'+dr+'-cfhtls-d2-i.fits', 'cfhtls-d2-i.fits.gz'],
     ['decals-dr'+dr+'-cfhtls-d2-r.fits', 'cfhtls-d2-r.fits.gz'],
     ['decals-dr'+dr+'-cfhtls-d3-i.fits', 'cfhtls-d3-i.fits.gz'],
     ['decals-dr'+dr+'-cfhtls-d3-r.fits', 'cfhtls-d3-r.fits.gz'],
     ['decals-dr'+dr+'-cosmos-acs.fits', 'cosmos-acs.fits.gz'],
     ['decals-dr'+dr+'-AllQSO.DECaLS.dr2.fits', 'AllQSO.DECaLS.dr2.fits'],
     ['decals-dr'+dr+'-Stars-str82-355-4.DECaLS.dr2.fits', 'Stars_str82_355_4.DECaLS.dr2.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spCDFS_DEEP_Full.fits', 'cesam_vvds_spCDFS_DEEP_Full.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spF02_DEEP_Full.fits', 'cesam_vvds_spF02_DEEP_Full.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spF02_UDEEP_Full.fits', 'cesam_vvds_spF02_UDEEP_Full.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spF10_WIDE_Full.fits', 'cesam_vvds_spF10_WIDE_Full.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spF14_WIDE_Full.fits', 'cesam_vvds_spF14_WIDE_Full.fits'],
     ['decals-dr'+dr+'-cesam_vvds_spF22_WIDE_Full.fits', 'cesam_vvds_spF22_WIDE_Full.fits'],
     ['decals-dr'+dr+'-shela-irac-v1.3-flux-cat.fits', 'shela_irac_v1.3_flux_cat.fits'],
     ['decals-dr'+dr+'-alldeep.egs.uniq.2012jun13.fits', 'alldeep.egs.uniq.2012jun13.fits.gz'],
]

for index in range(len(filelist)):

    print(filelist[index][0])

    decals_filename = filelist[index][0]
    spec_filename = filelist[index][1]

    decals_path = os.path.join(input_dir, decals_filename)
    spec_path = os.path.join(parent_dir, spec_filename)

    if not os.path.exists(decals_path):
        print('No match')
    else:
        cat1 = fits.getdata(decals_path)
        cat2 = fits.getdata(spec_path)

        notmask = (cat1['RA']==0) & (cat1['DEC']==0)
        mask = ~notmask
        print('fraction of matched objects: {}/{} = {}'.format(np.sum(mask), len(cat1), np.sum(mask)/len(cat1)))
        cat1 = cat1[mask]
        cat2 = cat2[mask]

        fits.writeto(os.path.join(output_dir, decals_filename[:-5]+'-trim.fits'), cat1)
        spec_output_filename = spec_filename[:spec_filename.find('.fits')]+'-trim.fits'
        fits.writeto(os.path.join(output_dir, spec_output_filename), cat2)
