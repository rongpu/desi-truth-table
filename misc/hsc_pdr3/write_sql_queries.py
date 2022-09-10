# Write SQL queries for HSC-PDR3 wide fields, splitting each field into smaller (<10 GB) chunks

from __future__ import division, print_function


ra_bins_dict = {'autumn': [[0, 10], [10, 20], [20, 30], [30, 35], [35, 50], [320, 335], [335, 340], [340, 345], [345, 350], [350, 360]],
                'spring': [[125, 135], [135, 145], [145, 155], [155, 165], [165, 175], [175, 185], [185, 195], [195, 205], [205, 215], [215, 230]],
                'hectomap': [[190, 210], [210, 220], [220, 230], [230, 240], [240, 260]],
                'aegis': [200, 250]}
dec_limits_dict = {'autumn': [-10, 10], 'spring': [-10, 10], 'hectomap': [40, 48], 'aegis': [48, 55]}

path = '/Users/rongpu/git/desi-truth-table/misc/hsc_pdr3/sql_query_hsc_pdr3_wide_all.sql'
with open(path, 'r') as f:
    lines = f.readlines()


for field in ['autumn', 'spring', 'hectomap', 'aegis']:

    decmin, decmax = dec_limits_dict[field]
    ra_bins = ra_bins_dict[field]

    if not isinstance(ra_bins[0], list):
        ramin, ramax = ra_bins
        with open('/Users/rongpu/git/desi-truth-table/misc/hsc_pdr3/sql_query_hsc_pdr3_wide/sql_query_hsc_pdr3_wide_{}.sql'.format(field), 'w') as f:
            for line in lines:
                if 'boxSearch' not in line:
                    f.write(line)
                else:
                    f.write('    AND boxSearch(coord, {}, {}, {}, {})\n'.format(ramin, ramax, decmin, decmax))
    else:
        for index, ra_bin in enumerate(ra_bins):
            ramin, ramax = ra_bin
            with open('/Users/rongpu/git/desi-truth-table/misc/hsc_pdr3/sql_query_hsc_pdr3_wide/sql_query_hsc_pdr3_wide_{}_{}.sql'.format(field, index+1), 'w') as f:
                for line in lines:
                    if 'boxSearch' not in line:
                        f.write(line)
                    else:
                        f.write('    AND boxSearch(coord, {}, {}, {}, {})\n'.format(ramin, ramax, decmin, decmax))
