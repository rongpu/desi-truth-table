SELECT
    main.object_id,
    main.ra,
    main.dec,

    ------- flux and flux errors -------
    main2.g_psfflux_flux, main2.r_psfflux_flux, main2.i_psfflux_flux, main2.z_psfflux_flux, main2.y_psfflux_flux,
    main2.g_psfflux_fluxsigma, main2.r_psfflux_fluxsigma, main2.i_psfflux_fluxsigma, main2.z_psfflux_fluxsigma, main2.y_psfflux_fluxsigma,
    main.g_cmodel_flux, main.r_cmodel_flux, main.i_cmodel_flux, main.z_cmodel_flux, main.y_cmodel_flux,
    main.g_cmodel_fluxsigma, main.r_cmodel_fluxsigma, main.i_cmodel_fluxsigma, main.z_cmodel_fluxsigma, main.y_cmodel_fluxsigma,

    ------- fraction of flux in de Vaucouleur component -------
    main.g_cmodel_fracdev, main.r_cmodel_fracdev, main.z_cmodel_fracdev,

    ------- shape measurements -------
    main.g_extendedness_value, main.r_extendedness_value, main.i_extendedness_value, main.z_extendedness_value,
    main.g_extendedness_flag, main.r_extendedness_flag, main.i_extendedness_flag, main.z_extendedness_flag,
    main2.i_kronflux_radius,
    main2.i_sdssshape_shape11, main2.i_sdssshape_shape22, main2.i_sdssshape_shape12,

    ------- flags -------
    main2.g_sdsscentroid_flag, main2.r_sdsscentroid_flag, main2.i_sdsscentroid_flag, main2.z_sdsscentroid_flag, main2.y_sdsscentroid_flag, 
    main.g_pixelflags_edge, main.r_pixelflags_edge, main.i_pixelflags_edge, main.z_pixelflags_edge, main.y_pixelflags_edge, 
    main.g_pixelflags_interpolatedcenter, main.r_pixelflags_interpolatedcenter, main.i_pixelflags_interpolatedcenter, main.z_pixelflags_interpolatedcenter, main.y_pixelflags_interpolatedcenter, 
    main.g_pixelflags_saturatedcenter, main.r_pixelflags_saturatedcenter, main.i_pixelflags_saturatedcenter, main.z_pixelflags_saturatedcenter, main.y_pixelflags_saturatedcenter, 
    main.g_pixelflags_crcenter, main.r_pixelflags_crcenter, main.i_pixelflags_crcenter, main.z_pixelflags_crcenter, main.y_pixelflags_crcenter, 
    main.g_pixelflags_bad, main.r_pixelflags_bad, main.i_pixelflags_bad, main.z_pixelflags_bad, main.y_pixelflags_bad, 
    main.g_cmodel_flag, main.r_cmodel_flag, main.i_cmodel_flag, main.z_cmodel_flag, main.y_cmodel_flag

    -- ------- photo-z's -------
    -- pz_demp.photoz_best AS demp_photoz_best, pz_demp.photoz_risk_best AS demp_photoz_risk_best, pz_demp.photoz_std_best AS demp_photoz_std_best,
    -- pz_ephor.photoz_best AS ephor_photoz_best, pz_ephor.photoz_risk_best AS ephor_photoz_risk_best, pz_ephor.photoz_std_best AS ephor_photoz_std_best,
    -- pz_ephor_ab.photoz_best AS ephor_ab_photoz_best, pz_ephor_ab.photoz_risk_best AS ephor_ab_photoz_risk_best, pz_ephor_ab.photoz_std_best AS ephor_ab_photoz_std_best,
    -- pz_frankenz.photoz_best AS frankenz_photoz_best, pz_frankenz.photoz_risk_best AS frankenz_photoz_risk_best, pz_frankenz.photoz_std_best AS frankenz_photoz_std_best,
    -- pz_mizuki.photoz_best AS mizuki_photoz_best, pz_mizuki.photoz_risk_best AS mizuki_photoz_risk_best, pz_mizuki.photoz_std_best AS mizuki_photoz_std_best,
    -- pz_mlz.photoz_best AS mlz_photoz_best, pz_mlz.photoz_risk_best AS mlz_photoz_risk_best, pz_mlz.photoz_std_best AS mlz_photoz_std_best,
    -- pz_nnpz.photoz_best AS nnpz_photoz_best, pz_nnpz.photoz_risk_best AS nnpz_photoz_risk_best, pz_nnpz.photoz_std_best AS nnpz_photoz_std_best

FROM
    pdr2_wide.forced main
    LEFT JOIN pdr2_wide.forced2 main2 USING (object_id) 
    -- LEFT JOIN pdr2_wide.photoz_demp pz_demp USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_ephor pz_ephor USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_ephor_ab pz_ephor_ab USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_frankenz pz_frankenz USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_mizuki pz_mizuki USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_mlz pz_mlz USING (object_id)
    -- LEFT JOIN pdr2_wide.photoz_nnpz pz_nnpz USING (object_id)

WHERE
    pdr2_wide.search_w01(object_id)
    -- pdr2_wide.search_w02(object_id)
    -- pdr2_wide.search_w03(object_id)
    -- pdr2_wide.search_w04(object_id)
    -- pdr2_wide.search_w05(object_id)
    -- pdr2_wide.search_w06(object_id)
    -- pdr2_wide.search_w07(object_id)
    AND isprimary
    AND r_cmodel_mag<25.0

-- LIMIT 100;