SELECT
    main.object_id,
    main.ra,
    main.dec,

    ------- flux and flux errors -------
    main2.g_psfflux_flux, main2.r_psfflux_flux, main2.i_psfflux_flux, main2.z_psfflux_flux, main2.y_psfflux_flux,
    main2.g_psfflux_fluxerr, main2.r_psfflux_fluxerr, main2.i_psfflux_fluxerr, main2.z_psfflux_fluxerr, main2.y_psfflux_fluxerr,
    main.g_cmodel_flux, main.r_cmodel_flux, main.i_cmodel_flux, main.z_cmodel_flux, main.y_cmodel_flux,
    main.g_cmodel_fluxerr, main.r_cmodel_fluxerr, main.i_cmodel_fluxerr, main.z_cmodel_fluxerr, main.y_cmodel_fluxerr,

    ------- fraction of flux in de Vaucouleur component -------
    main.g_cmodel_fracdev, main.r_cmodel_fracdev, main.i_cmodel_fracdev, main.z_cmodel_fracdev,

    ------- shape measurements -------
    main.g_extendedness_value, main.r_extendedness_value, main.i_extendedness_value, main.z_extendedness_value,
    main.g_extendedness_flag, main.r_extendedness_flag, main.i_extendedness_flag, main.z_extendedness_flag,
    main2.i_sdssshape_shape11, main2.i_sdssshape_shape22, main2.i_sdssshape_shape12,
    main2.i_sdssshape_shape11err, main2.i_sdssshape_shape22err, main2.i_sdssshape_shape12err,

    ------- flags -------
    main2.g_sdsscentroid_flag, main2.r_sdsscentroid_flag, main2.i_sdsscentroid_flag, main2.z_sdsscentroid_flag, main2.y_sdsscentroid_flag, 
    main.g_pixelflags_edge, main.r_pixelflags_edge, main.i_pixelflags_edge, main.z_pixelflags_edge, main.y_pixelflags_edge, 
    main.g_pixelflags_interpolatedcenter, main.r_pixelflags_interpolatedcenter, main.i_pixelflags_interpolatedcenter, main.z_pixelflags_interpolatedcenter, main.y_pixelflags_interpolatedcenter, 
    main.g_pixelflags_saturatedcenter, main.r_pixelflags_saturatedcenter, main.i_pixelflags_saturatedcenter, main.z_pixelflags_saturatedcenter, main.y_pixelflags_saturatedcenter, 
    main.g_pixelflags_crcenter, main.r_pixelflags_crcenter, main.i_pixelflags_crcenter, main.z_pixelflags_crcenter, main.y_pixelflags_crcenter, 
    main.g_pixelflags_bad, main.r_pixelflags_bad, main.i_pixelflags_bad, main.z_pixelflags_bad, main.y_pixelflags_bad, 
    main.g_cmodel_flag, main.r_cmodel_flag, main.i_cmodel_flag, main.z_cmodel_flag, main.y_cmodel_flag,

    ------- photo-z's and stellar masses -------
    pz_demp.photoz_best AS demp_photoz_best, pz_demp.photoz_risk_best AS demp_photoz_risk_best, pz_demp.photoz_std_best AS demp_photoz_std_best, 
    pz_demp.photoz_mode AS demp_photoz_mode, pz_demp.photoz_risk_mode AS demp_photoz_risk_mode, pz_demp.photoz_std_mode AS demp_photoz_std_mode, 
    pz_demp.photoz_err68_min AS demp_photoz_err68_min, pz_demp.photoz_err68_max AS demp_photoz_err68_max, pz_demp.photoz_err95_min AS demp_photoz_err95_min, pz_demp.photoz_err95_max AS demp_photoz_err95_max, 
    pz_demp.stellar_mass AS demp_stellar_mass, pz_demp.stellar_mass_err68_min AS demp_stellar_mass_err68_min, pz_demp.stellar_mass_err68_max AS demp_stellar_mass_err68_max, 
    pz_demp.sfr AS demp_sfr, pz_demp.sfr_err68_min AS demp_sfr_err68_min, pz_demp.sfr_err68_max AS demp_sfr_err68_max, 
    pz_mizuki.photoz_best AS mizuki_photoz_best, pz_mizuki.photoz_risk_best AS mizuki_photoz_risk_best, pz_mizuki.photoz_std_best AS mizuki_photoz_std_best, 
    pz_mizuki.photoz_err68_min AS mizuki_photoz_err68_min, pz_mizuki.photoz_err68_max AS mizuki_photoz_err68_max, pz_mizuki.photoz_err95_min AS mizuki_photoz_err95_min, pz_mizuki.photoz_err95_max AS mizuki_photoz_err95_max, 
    pz_mizuki.stellar_mass AS mizuki_stellar_mass, pz_mizuki.stellar_mass_err68_min AS mizuki_stellar_mass_err68_min, pz_mizuki.stellar_mass_err68_max AS mizuki_stellar_mass_err68_max, 
    pz_mizuki.sfr AS mizuki_sfr, pz_mizuki.sfr_err68_min AS mizuki_sfr_err68_min, pz_mizuki.sfr_err68_max AS mizuki_sfr_err68_max,
    pz_dnnz.photoz_best AS dnnz_photoz_best, pz_dnnz.photoz_risk_best AS dnnz_photoz_risk_best, pz_dnnz.photoz_std_best AS dnnz_photoz_std_best, 
    pz_dnnz.photoz_err68_min AS dnnz_photoz_err68_min, pz_dnnz.photoz_err68_max AS dnnz_photoz_err68_max, pz_dnnz.photoz_err95_min AS dnnz_photoz_err95_min, pz_dnnz.photoz_err95_max AS dnnz_photoz_err95_max, 
    pz_dnnz.olprob AS dnnz_olprob

FROM
    pdr3_wide.forced main
    LEFT JOIN pdr3_wide.forced2 main2 USING (object_id) 
    LEFT JOIN pdr3_wide.photoz_demp pz_demp USING (object_id)
    LEFT JOIN pdr3_wide.photoz_mizuki pz_mizuki USING (object_id)
    LEFT JOIN pdr3_wide.photoz_dnnz pz_dnnz USING (object_id)

WHERE
    isprimary
    AND boxSearch(coord, 215, 230, -10, 10)
    AND (g_cmodel_mag<25.0 OR r_cmodel_mag<25.0 OR i_cmodel_mag<24.4 OR z_cmodel_mag<23.7)

-- LIMIT 100;