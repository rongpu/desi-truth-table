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
     DEEP2
     DEEP3
     COSMOS Photo-z
     COSMOS HST/ACS
     CFHTLS
     VIPERS
     SpIES
     Stripe 82 Stars
     VVDS
     SHELA

---------------------------------------------------------------------------
Thing to modify for a new DECaLS DR: 

    decals_matching.py: dr, top_dir, sweep_dir 
    trim_matched_catalogs: dr, top_dir 

