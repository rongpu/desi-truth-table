from __future__ import division, print_function

def get_filenames(cat2_filelist, dr):
    with open(cat2_filelist, 'r') as f:
        cat2_filenames = list(map(str.rstrip, f.readlines()))
    output_filenames = []
    for filename in cat2_filenames:
        if filename[-3:]=='.gz':
            filename = filename[:-3]
        output_filenames.append('decals-dr'+dr+'-'+filename)
    return cat2_filenames, output_filenames

def catalog_info(catalog, dr):
    '''
    Return the catalog information necessary for reading the catalog.
    '''

    # Read from the first HDU by default
    ext = 0

    if catalog.lower()=='ages':
        # RA and Dec columns in cat2
        ra_col = 'RAJ2000'
        dec_col = 'DEJ2000'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['ages_reduced.fits']
        output_filenames = ['decals-dr'+dr+'-ages_reduced.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_ages/'
    elif catalog.lower()=='sdss':
        # RA and Dec columns in cat2
        ra_col = 'PLUG_RA'
        dec_col = 'PLUG_DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['sdss-specObj-dr14-unique-trimmed.fits']
        output_filenames = ['decals-dr'+dr+'-sdss-specObj-dr14-unique-trimmed.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_sdss_dr14/'
        ext = 1
    elif catalog.lower()=='eboss':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['eBOSS-DR14-redmonsterAll-v5_10_0-radec-added.fits']
        output_filenames = ['decals-dr'+dr+'-eBOSS-DR14-redmonsterAll-v5_10_0-radec-added.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_eboss_dr14/'
    elif catalog.lower()=='cosmos_zphot':
        # RA and Dec columns in cat2
        ra_col = 'ALPHA_J2000'
        dec_col = 'DELTA_J2000'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['COSMOS2015_Laigle+_v1.1.fits']
        output_filenames = ['decals-dr'+dr+'-cosmos-zphot.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_cosmos_zphot/'
    elif catalog.lower()=='cosmos_acs':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['cosmos-acs.fits.gz']
        output_filenames = ['decals-dr'+dr+'-cosmos-acs.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_cosmos_acs/'
    elif catalog.lower()=='spies':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 3.
        cat2_filenames = ['spies.fits.gz']
        output_filenames = ['decals-dr'+dr+'-spies.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_spies/'
    elif catalog.lower()=='deep2':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-truth-table/misc/deep2_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = 'qaplots/dr'+dr+'/decals_match_deep2/'
    elif catalog.lower()=='vipers':
        # RA and Dec columns in cat2
        ra_col = 'alpha'
        dec_col = 'delta'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-truth-table/misc/vipers_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = 'qaplots/dr'+dr+'/decals_match_vipers/'
    elif catalog.lower()=='cfhtls':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-truth-table/misc/cfhtls_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = 'qaplots/dr'+dr+'/decals_match_cfhtls/'
    elif catalog.lower()=='vvds':
        # RA and Dec columns in cat2
        ra_col = 'ALPHA'
        dec_col = 'DELTA'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-truth-table/misc/vvds_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = 'qaplots/dr'+dr+'/decals_match_vvds/'
    elif catalog.lower()=='shela':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 3.
        cat2_filenames = ['shela_irac_v1.3_flux_cat.fits']
        output_filenames = ['decals-dr'+dr+'-shela-irac-v1.3-flux-cat.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_shela/'
    elif catalog.lower()=='deep3':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['alldeep.egs.uniq.2012jun13.fits.gz']
        output_filenames = ['decals-dr'+dr+'-alldeep.egs.uniq.2012jun13.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_deep3/'
    elif catalog.lower()=='3d-hst':
        # RA and Dec columns in cat2
        ra_col = 'ra'
        dec_col = 'dec'
        # Search radius in arcsec
        search_radius = 0.4
        filelist_path = '/global/homes/r/rongpu/git/desi-truth-table/misc/3d-hst_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = 'qaplots/dr'+dr+'/decals_match_3d-hst/'
    elif catalog.lower()=='fmost-cosmos':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['FMOS_COSMOS_v1.0.fits']
        output_filenames = ['decals-dr'+dr+'-FMOS_COSMOS_v1.0.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_fmost-cosmos/'
    elif catalog.lower()=='mosdef':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['mosdef_zcat.16aug2016.fits']
        output_filenames = ['decals-dr'+dr+'-mosdef_zcat.16aug2016.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_mosdef/'
    elif catalog.lower()=='gama':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['GAMA-DR2-SpecObj.fits']
        output_filenames = ['decals-dr'+dr+'-GAMA-DR2-SpecObj.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_gama/'
        ext = 1
    elif catalog.lower()=='wigglez':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['wigglez_dr1_unique.fits']
        output_filenames = ['decals-dr'+dr+'-wigglez_dr1_unique.fits']
        plot_path = 'qaplots/dr'+dr+'/decals_match_wigglez/'
        ext = 1
    else:
        raise ValueError('ERROR: '+catalog+' not found!')

    return ra_col, dec_col, search_radius, cat2_filenames, output_filenames, plot_path, ext
