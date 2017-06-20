## Reduction

AGES reduction and remove duplicates:

    ages_reduction.py
    **THIS CODE SHOULD BE USED AS THE STANDARD DUPLICATE REMOVAL CODE** 

Convert VVDS data to fits format: 
     vvds_fits.py


## Matching

Match DECaLS to other catalogs: 

   decals_matching.py

Create catalogs that only contain matched objects: 

    trim_matched_catalogs.py

__Catalogs currently included:__ 

     AGES
     SDSS+BOSS DR13
     DEEP2
     COSMOS Photo-z
     COSMOS HST/ACS
     CFHTLS
     VIPERS
     SpIES
     Stripe 82 Stars
     Stripe 82 Spectroscopy
     VVDS
     SHELA

---------------------------------------------------------------------------
Thing to modify for a new DECaLS DR: 

    decals_matching.py: data_dir, output_dir, sweep_dir 
    catalog_info.py: dr, filelist_path 
    trim_matched_catalogs: dr, parent_dir 

