# Cross-matching with BRICKID and BRICK_OBJID/OBJID, and obtain pz and stellar mass values
# cat1 - sweep catalogs
# cat2 - a single catalog file with unique objects and BRICKID and BRICK_OBJID

# Example:
# python legacy_surveys_matching.py 8.0 /global/cfs/cdirs/desi/target/analysis/truth/dr8.0/south/matched/ls-dr8.0-deep2-field2-match.fits --field north

from __future__ import division, print_function
# import matplotlib
# matplotlib.use( "Agg" )
import sys, os, glob, time, warnings, gc
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack, hstack
import fitsio
import argparse

time_start = time.clock()

parser = argparse.ArgumentParser()
parser.add_argument('ls_dr', help='DR number of Legacy Surveys')
parser.add_argument('catalog', help='file path of truth catalog')
parser.add_argument('--field', help='choose field: north or south?')
args = parser.parse_args()

if float(args.ls_dr)>=8:
    if (args.field!='north') and (args.field!='south'):
        raise ValueError('field can only be \"north\" or \"south\"!')
    sweep_dir = os.path.join('/global/project/projectdirs/cosmo/data/legacysurvey/', 
        'dr'+args.ls_dr[0], args.field, 'sweep', args.ls_dr)
    # pz_dir = os.path.join('/global/project/projectdirs/cosmo/data/legacysurvey/', 
    #     'dr'+args.ls_dr[0], args.field, 'sweep', args.ls_dr+'-photo-z')
    pz_dir = os.path.join('/global/cfs/cdirs/desi/users/rongpu/ls_dr{}_photoz'.format(args.ls_dr), 'sweep_'+args.field)
else:
    raise ValueError('only DR8+ is supported')

print(sweep_dir)
print(pz_dir)
print(args.catalog)
print()

cat2_path = args.catalog
cat1_paths = sorted(glob.glob(os.path.join(sweep_dir, '*.fits')))

output_path = cat2_path.replace('.fits', '-pz.fits')

if os.path.isfile(output_path):
    print(output_path+' already exist!!!!!!!!!!!!!!')
    sys.exit()

# BRICK_OBJID is the column in the target catalog
cat2 = Table(fitsio.read(cat2_path, columns=['BRICKID', 'BRICK_OBJID']))
if cat2['BRICK_OBJID'].max()>=1000000:
    raise ValueError('BRICK_OBJID too large!!!')
# Force int64 to avoid integer overflow
cat2['id'] = np.array(cat2['BRICKID'], dtype='int64')*1000000+np.array(cat2['BRICK_OBJID'], dtype='int64')
if not len(cat2)==len(np.unique(cat2['id'])):
    raise ValueError('id not unique!!!')
cat2.sort('id')

cat1_stack = []
for cat1_index in range(len(cat1_paths)):

    # Load sweep catalog

    cat1_path = cat1_paths[cat1_index]
    print(cat1_index, len(cat1_paths), cat1_path)

    cat1 = Table(fitsio.read(cat1_path, columns=['BRICKID', 'OBJID']))
    if cat1['OBJID'].max()>=1000000:
        raise ValueError('OBJID too large!!!')
    cat1['id'] = np.array(cat1['BRICKID'], dtype='int64')*1000000+np.array(cat1['OBJID'], dtype='int64')
    if not len(cat1)==len(np.unique(cat1['id'])):
        raise ValueError('id not unique!!!')
    cat1.remove_columns(['BRICKID', 'OBJID'])

    cat1_fn = os.path.basename(cat1_path)
    
    # Add photo-z's
    cat1_pz_path = os.path.join(pz_dir, cat1_fn.replace('.fits', '-pz.fits'))
    cat1_pz = Table.read(cat1_pz_path)
    cat1 = hstack([cat1, cat1_pz])

    # Add stellar masses
    cat1_steller_mass_path = os.path.join(pz_dir, cat1_fn.replace('.fits', '_stellar_mass.npy'))
    stellar_mass = np.load(cat1_steller_mass_path)
    cat1['MASS_OPT'] = stellar_mass

    mask = np.in1d(cat1['id'], cat2['id'])
    cat1 = cat1[mask]
    cat1_stack.append(cat1)

cat1_stack = vstack(cat1_stack)
cat1_stack.sort('id')

if len(cat2)!=len(cat1_stack):
    raise ValueError('Length does not match!!!')
if not np.all(cat2['id']==cat1_stack['id']):
    raise ValueError('ids do not match!!!')

cat1_stack.remove_column('id')

cat2 = hstack([cat2, cat1_stack])
cat2.write(output_path)

time_end = time.clock()
print('%.1f seconds'%(time_end-time_start))
time_start = time_end-time_start

print('\n------------------------------------------------------\n')


