from __future__ import division, print_function
import os, sys
import yaml

def get_output_filenames(cat2_filenames, dr):
    output_filenames = []
    for filename in cat2_filenames:
        if filename[-3:]=='.gz':
            filename = filename[:-3]
        output_filenames.append('ls-dr'+dr+'-'+filename)
    return output_filenames

def catalog_info(catalog_yaml_fn, dr, field=None, predr8=False):
    '''
    Return the essential catalog information.
    '''

    # by default use the default fitsio setting
    ext = None

    catalog = os.path.basename(catalog_yaml_fn).replace('.yaml', '')

    try:
        with open(catalog_yaml_fn) as f:
            cat2_dict = yaml.safe_load(f)
    except IOError:
        raise IOError(catalog_yaml_fn+' not found!')

    ra_col = cat2_dict['ra_col']
    dec_col = cat2_dict['dec_col']
    search_radius = cat2_dict['search_radius']
    cat2_filenames = cat2_dict['filenames']
    output_filenames = get_output_filenames(cat2_filenames, dr)
    if not predr8:
        if field is None:
            raise ValueError('field is not specified!')
        plot_path = 'qaplots/dr'+dr+'/'+field+'/'+catalog+'/'
    else:
        plot_path = 'qaplots/dr'+dr+'/'+catalog+'/'
    if 'ext' in cat2_dict:
        ext = cat2_dict['ext']

    return ra_col, dec_col, search_radius, cat2_filenames, output_filenames, plot_path, ext
