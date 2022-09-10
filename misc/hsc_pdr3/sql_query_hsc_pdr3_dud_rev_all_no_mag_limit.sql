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
    main.g_cmodel_flag, main.r_cmodel_flag, main.i_cmodel_flag, main.z_cmodel_flag, main.y_cmodel_flag

FROM
    pdr3_dud_rev.forced main
    LEFT JOIN pdr3_dud_rev.forced2 main2 USING (object_id) 

WHERE
    isprimary

-- LIMIT 100;