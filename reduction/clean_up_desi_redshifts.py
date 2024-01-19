from __future__ import division, print_function
import sys, os, glob, time, warnings, gc
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack, hstack, join
import fitsio

############################################################ SV1 BGS ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv1_cumulative_bgs.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']
cat['EFFTIME_BGS'] = 0.1400 * cat['TSNR2_BGS']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply MEDIUM masks
maskbits = [1, 11, 13]
mask_clean = np.ones(len(cat), dtype=bool)
for bit in maskbits:
    mask_clean &= (cat['MASKBITS'] & 2**bit)==0
print('BGS', np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]
print(len(cat))

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_BGS', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_BGS']>540)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Redshift quality cut
mask_quality = cat['ZWARN']==0
mask_quality &= cat['Z']<0.8
mask_quality &= cat['DELTACHI2']>80
print(np.sum(~mask_quality)/len(mask_quality))
cat = cat[mask_quality]
print(len(cat))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

columns_to_keep = ['TARGETID', 'Z', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV1-BGS'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv1_bgs.fits')

############################################################ SV1 ELG ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv1_cumulative_elg.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']
cat['EFFTIME_BGS'] = 0.1400 * cat['TSNR2_BGS']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply ELG mask
mask_clean = cat['elg_mask']==0
print('ELG mask', np.sum(mask_clean), np.sum(~mask_clean), np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_LRG', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_LRG']>3000)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Redshift quality cut
mask_quality = cat['ZWARN']==0
mask_quality &= cat['DELTACHI2']>45
mask_quality &= (cat['OII_FLUX']>0) & (cat['OII_FLUX_IVAR']>0)
mask_quality &= np.log10(cat['OII_FLUX'] * np.sqrt(cat['OII_FLUX_IVAR'])) > 0.9 - 0.2 * np.log10(cat['DELTACHI2'])
print(np.sum(~mask_quality)/len(mask_quality))
cat = cat[mask_quality]
print(len(cat))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

columns_to_keep = ['TARGETID', 'Z', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV1-ELG'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv1_elg.fits')

############################################################ SV1 LRG ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv1_cumulative_lrg.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']
cat['EFFTIME_BGS'] = 0.1400 * cat['TSNR2_BGS']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply LRG mask
mask_clean = cat['lrg_mask']==0
print('LRG mask', np.sum(mask_clean), np.sum(~mask_clean), np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_LRG', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_LRG']>3000)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Redshift quality cut
mask_quality = cat['ZWARN']==0
mask_quality &= cat['Z']<1.45
mask_quality &= cat['DELTACHI2']>45
print(np.sum(~mask_quality)/len(mask_quality))
cat = cat[mask_quality]
print(len(cat))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

columns_to_keep = ['TARGETID', 'Z', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV1-LRG'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv1_lrg.fits')

############################################################ SV1 QSO ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv1_cumulative_qso.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply DR9 bitmasks
maskbits = [1, 8, 9, 11, 12, 13]
mask_clean = np.ones(len(cat), dtype=bool)
for bit in maskbits:
    mask_clean &= (cat['MASKBITS'] & 2**bit)==0
print('Masking', np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_LRG', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_LRG']>3000)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

# Select QSOs and apply redshift quality cuts
res = Table()
res['IS_QSO_QN'] = np.max(np.array([cat[name] for name in ['C_LYA', 'C_CIV', 'C_CIII', 'C_MgII', 'C_Hbeta', 'C_Halpha']]), axis=0) > 0.95
res['IS_QSO_QN_NEW_RR'] = cat['IS_QSO_QN_NEW_RR'] & res['IS_QSO_QN']
res['GOOD_QSO'] = (cat['SPECTYPE']=='QSO') | cat['IS_QSO_MGII'] | res['IS_QSO_QN']
res['Z_QSO'] = cat['Z'].copy()
res['Z_QSO'][res['IS_QSO_QN_NEW_RR']] = cat['Z_NEW'][res['IS_QSO_QN_NEW_RR']].copy()
res['ZERR'] = cat['ZERR'].copy()
res['ZERR'][res['IS_QSO_QN_NEW_RR']] = cat['ZERR_NEW'][res['IS_QSO_QN_NEW_RR']].copy()
# Correct bump at z~3.7
sel_pb_redshift = (((res['Z_QSO'] > 3.65) & (res['Z_QSO'] < 3.9)) | ((res['Z_QSO'] > 5.15) & (res['Z_QSO'] < 5.35))) & ((cat['C_LYA'] < 0.95) | (cat['C_CIV'] < 0.95))
print(np.sum(sel_pb_redshift), np.sum(sel_pb_redshift)/len(sel_pb_redshift))
res['GOOD_QSO'][sel_pb_redshift] = False
print(np.sum(res['GOOD_QSO'])/len(res))
cat['GOOD_QSO'] = res['GOOD_QSO'].copy()
cat['Z_QSO'] = res['Z_QSO'].copy()
cat['ZERR_QSO'] = res['ZERR'].copy()
mask = cat['GOOD_QSO'].copy()
print('Good QSO', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Require the same redshift from RR and QN
zdiff_threshold = 0.01
mask_fail = np.abs((cat['Z'] - cat['Z_QSO'])/(1 + cat['Z'])) > zdiff_threshold
mask = ~mask_fail
print('Same redshift', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# DELTACHI2 cut
mask = cat['DELTACHI2']>45
print('DELTACHI2', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

columns_to_keep = ['TARGETID', 'Z', 'Z_QSO', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV1-QSO'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv1_qso.fits')

############################################################ SV3 BGS ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv3_cumulative_bgs.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']
cat['EFFTIME_BGS'] = 0.1400 * cat['TSNR2_BGS']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply MEDIUM masks
maskbits = [1, 11, 13]
mask_clean = np.ones(len(cat), dtype=bool)
for bit in maskbits:
    mask_clean &= (cat['MASKBITS'] & 2**bit)==0
print('BGS', np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]
print(len(cat))

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_BGS', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_BGS']>160)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Redshift quality cut
mask_quality = cat['ZWARN']==0
mask_quality &= cat['Z']<0.8
mask_quality &= cat['DELTACHI2']>40
print(np.sum(~mask_quality)/len(mask_quality))
cat = cat[mask_quality]
print(len(cat))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

columns_to_keep = ['TARGETID', 'Z', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV3-BGS'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv3_bgs.fits')

############################################################ SV3 LRG ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv3_cumulative_lrg.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']
cat['EFFTIME_BGS'] = 0.1400 * cat['TSNR2_BGS']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply LRG mask
mask_clean = cat['lrg_mask']==0
print('LRG mask', np.sum(mask_clean), np.sum(~mask_clean), np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_LRG', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_LRG']>1000)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Redshift quality cut
mask_quality = cat['ZWARN']==0
mask_quality &= cat['Z']<1.45
mask_quality &= cat['DELTACHI2']>30
print(np.sum(~mask_quality)/len(mask_quality))
cat = cat[mask_quality]
print(len(cat))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

columns_to_keep = ['TARGETID', 'Z', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV3-LRG'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv3_lrg.fits')

############################################################ SV3 QSO ############################################################

cat = Table(fitsio.read('/global/cfs/cdirs/desi/users/rongpu/spectro/fugu/sv3_cumulative_qso.fits'))
print(len(cat), len(np.unique(cat['TARGETID'])))

cat['EFFTIME_LRG'] = 12.15 * cat['TSNR2_LRG']

# Remove FIBERSTATUS!=0 fibers
mask = cat['COADD_FIBERSTATUS']==0
print('FIBERSTATUS', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Remove "no data" fibers
mask = cat['ZWARN'] & 2**9==0
print('No data', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Apply DR9 bitmasks
maskbits = [1, 8, 9, 11, 12, 13]
mask_clean = np.ones(len(cat), dtype=bool)
for bit in maskbits:
    mask_clean &= (cat['MASKBITS'] & 2**bit)==0
print('Masking', np.sum(~mask_clean)/len(mask_clean))
cat = cat[mask_clean]

# Remove duplidates keeping the higher EFFTIME objects
cat.sort('EFFTIME_LRG', reverse=True)
_, idx_keep = np.unique(cat['TARGETID'], return_index=True)
cat = cat[idx_keep]
print(len(cat), len(np.unique(cat['TARGETID'])))

mask_good = (cat['EFFTIME_LRG']>1000)
cat = cat[mask_good]
print(len(cat), len(np.unique(cat['TARGETID'])))

# Remove stars
mask_star = (cat['SPECTYPE']=='STAR') | (cat['Z']<0.0003)
print(np.sum(mask_star)/len(mask_star))
cat = cat[~mask_star]
print(len(cat))

# Select QSOs and apply redshift quality cuts
res = Table()
res['IS_QSO_QN'] = np.max(np.array([cat[name] for name in ['C_LYA', 'C_CIV', 'C_CIII', 'C_MgII', 'C_Hbeta', 'C_Halpha']]), axis=0) > 0.95
res['IS_QSO_QN_NEW_RR'] = cat['IS_QSO_QN_NEW_RR'] & res['IS_QSO_QN']
res['GOOD_QSO'] = (cat['SPECTYPE']=='QSO') | cat['IS_QSO_MGII'] | res['IS_QSO_QN']
res['Z_QSO'] = cat['Z'].copy()
res['Z_QSO'][res['IS_QSO_QN_NEW_RR']] = cat['Z_NEW'][res['IS_QSO_QN_NEW_RR']].copy()
res['ZERR'] = cat['ZERR'].copy()
res['ZERR'][res['IS_QSO_QN_NEW_RR']] = cat['ZERR_NEW'][res['IS_QSO_QN_NEW_RR']].copy()
# Correct bump at z~3.7
sel_pb_redshift = (((res['Z_QSO'] > 3.65) & (res['Z_QSO'] < 3.9)) | ((res['Z_QSO'] > 5.15) & (res['Z_QSO'] < 5.35))) & ((cat['C_LYA'] < 0.95) | (cat['C_CIV'] < 0.95))
print(np.sum(sel_pb_redshift), np.sum(sel_pb_redshift)/len(sel_pb_redshift))
res['GOOD_QSO'][sel_pb_redshift] = False
print(np.sum(res['GOOD_QSO'])/len(res))
cat['GOOD_QSO'] = res['GOOD_QSO'].copy()
cat['Z_QSO'] = res['Z_QSO'].copy()
cat['ZERR_QSO'] = res['ZERR'].copy()
mask = cat['GOOD_QSO'].copy()
print('Good QSO', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# Require the same redshift from RR and QN
zdiff_threshold = 0.01
mask_fail = np.abs((cat['Z'] - cat['Z_QSO'])/(1 + cat['Z'])) > zdiff_threshold
mask = ~mask_fail
print('Same redshift', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

# DELTACHI2 cut
mask = cat['DELTACHI2']>30
print('DELTACHI2', np.sum(mask), np.sum(~mask), np.sum(~mask)/len(mask))
cat = cat[mask]

columns_to_keep = ['TARGETID', 'Z', 'Z_QSO', 'ZERR', 'ZWARN', 'CHI2', 'SPECTYPE', 'DELTACHI2', 'COADD_FIBERSTATUS', 'TARGET_RA', 'TARGET_DEC', 'COADD_NUMEXP', 'COADD_EXPTIME', 'COADD_NUMNIGHT', 'COADD_NUMTILE', 'TSNR2_ELG', 'TSNR2_BGS', 'TSNR2_QSO', 'TSNR2_LRG', 'OII_FLUX', 'OII_FLUX_IVAR', 'HDELTA_FLUX', 'HDELTA_FLUX_IVAR', 'HGAMMA_FLUX', 'HGAMMA_FLUX_IVAR', 'HBETA_FLUX', 'HBETA_FLUX_IVAR', 'OIII_FLUX', 'OIII_FLUX_IVAR', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR', 'fn']
cat = cat[columns_to_keep]

cat['SURVEY'] = 'DESI-SV3-QSO'

cat.write('/global/cfs/cdirs/desi/target/analysis/truth/parent/desi_sv3_qso.fits')

