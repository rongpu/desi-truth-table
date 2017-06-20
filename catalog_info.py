def get_filenames(cat2_filelist, dr):
    with open(cat2_filelist, 'r') as f:
        cat2_filenames = map(str.rstrip, f.readlines())
    output_filenames = []
    for filename in cat2_filenames:
        if filename[-3:]=='.gz':
            filename = filename[:-3]
        output_filenames.append('decals-dr'+dr+'-'+filename)
    return cat2_filenames, output_filenames

def catalog_info(catalog):
    '''
    Return the catalog information necessary for reading the catalog.
    '''

    # DECaLS version
    dr='4.0'

    if catalog.lower()=='ages':
        # RA and Dec columns in cat2
        ra_col = 'RAJ2000'
        dec_col = 'DEJ2000'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['ages_reduced.fits']
        output_filenames = ['decals-dr'+dr+'-ages.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_ages/'
    elif catalog.lower()=='eboss':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['redmonsterAll-v5_10_0_radec_added.fits']
        output_filenames = ['decals-dr'+dr+'-eboss.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_eboss/'
    elif catalog.lower()=='sdss':
        # RA and Dec columns in cat2
        ra_col = 'PLUG_RA'
        dec_col = 'PLUG_DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['specObj-dr13-unique-trimmed.fits']
        output_filenames = ['decals-dr'+dr+'-sdss.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_sdss/'
    elif catalog.lower()=='cosmos_zphot':
        # RA and Dec columns in cat2
        ra_col = 'ALPHA_J2000'
        dec_col = 'DELTA_J2000'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['COSMOS2015_Laigle+_v1.1.fits']
        output_filenames = ['decals-dr'+dr+'-cosmos-zphot.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_cosmos_zphot/'
    elif catalog.lower()=='cosmos_acs':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['cosmos-acs.fits.gz']
        output_filenames = ['decals-dr'+dr+'-cosmos-acs.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_cosmos_acs/'
    elif catalog.lower()=='spies':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 3.
        cat2_filenames = ['spies.fits.gz']
        output_filenames = ['decals-dr'+dr+'-spies.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_spies/'
    elif catalog.lower()=='stripe82_stars':
        # RA and Dec columns in cat2
        ra_col = 'ra'
        dec_col = 'dec'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['stripe82-dr12-stars.fits.gz']
        output_filenames = ['decals-dr'+dr+'-stripe82-stars.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_stripe82_stars/'
    elif catalog.lower()=='stripe82_specz':
        # RA and Dec columns in cat2
        ra_col = 'PLUG_RA'
        dec_col = 'PLUG_DEC'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['stripe82-dr12-specz.fits.gz']
        output_filenames = ['decals-dr'+dr+'-stripe82-specz.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_stripe82_specz/'
    elif catalog.lower()=='deep2':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-target-selection/catalog_matching/misc/deep2_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_deep2/'
    elif catalog.lower()=='vipers':
        # RA and Dec columns in cat2
        ra_col = 'alpha'
        dec_col = 'delta'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-target-selection/catalog_matching/misc/vipers_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_vipers/'
    elif catalog.lower()=='cfhtls':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-target-selection/catalog_matching/misc/cfhtls_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_cfhtls/'
    elif catalog.lower()=='allqso':
        # RA and Dec columns in cat2
        ra_col = 'ra_2'
        dec_col = 'dec_2'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['AllQSO.DECaLS.dr2.fits']
        output_filenames = ['decals-dr'+dr+'-AllQSO.DECaLS.dr2.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_allqso/'
    elif catalog.lower()=='stars_str82_355_4':
        # RA and Dec columns in cat2
        ra_col = 'ra_2'
        dec_col = 'dec_2'
        # Search radius in arcsec
        search_radius = 1.
        cat2_filenames = ['Stars_str82_355_4.DECaLS.dr2.fits']
        output_filenames = ['decals-dr'+dr+'-Stars-str82-355-4.DECaLS.dr2.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_stars_str82_355_4/'
    elif catalog.lower()=='vvds':
        # RA and Dec columns in cat2
        ra_col = 'ALPHA'
        dec_col = 'DELTA'
        # Search radius in arcsec
        search_radius = 1.
        filelist_path = '/global/homes/r/rongpu/git/desi-target-selection/catalog_matching/misc/vvds_filelist.txt'
        cat2_filenames, output_filenames = get_filenames(filelist_path, dr)
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_vvds/'
    elif catalog.lower()=='shela':
        # RA and Dec columns in cat2
        ra_col = 'RA'
        dec_col = 'DEC'
        # Search radius in arcsec
        search_radius = 3.
        cat2_filenames = ['shela_irac_v1.3_flux_cat.fits']
        output_filenames = ['decals-dr'+dr+'-shela-irac-v1.3-flux-cat.fits']
        plot_path = '/project/projectdirs/desi/target/analysis/truth/qaplots/dr'+dr+'/decals_match_shela/'
    else:
        raise ValueError('ERROR: '+catalog+' not found!')

    return ra_col, dec_col, search_radius, cat2_filenames, output_filenames, plot_path
