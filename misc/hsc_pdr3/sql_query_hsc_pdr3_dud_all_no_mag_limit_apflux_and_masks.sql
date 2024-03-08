SELECT
    main.object_id,
    ------- aperture fluxes and errors -------
    main3.g_apertureflux_15_flux, main3.r_apertureflux_15_flux, main3.i_apertureflux_15_flux, main3.z_apertureflux_15_flux, main3.y_apertureflux_15_flux,
    main3.g_apertureflux_15_fluxerr, main3.r_apertureflux_15_fluxerr, main3.i_apertureflux_15_fluxerr, main3.z_apertureflux_15_fluxerr, main3.y_apertureflux_15_fluxerr,

    ------- masks -------
    masks.g_mask_brightstar_any, masks.g_mask_brightstar_halo, masks.g_mask_brightstar_dip, masks.g_mask_brightstar_ghost, masks.g_mask_brightstar_blooming, masks.g_mask_brightstar_ghost12, masks.g_mask_brightstar_ghost15,
    masks.r_mask_brightstar_any, masks.r_mask_brightstar_halo, masks.r_mask_brightstar_dip, masks.r_mask_brightstar_ghost, masks.r_mask_brightstar_blooming, masks.r_mask_brightstar_ghost12, masks.r_mask_brightstar_ghost15,
    masks.i_mask_brightstar_any, masks.i_mask_brightstar_halo, masks.i_mask_brightstar_dip, masks.i_mask_brightstar_ghost, masks.i_mask_brightstar_blooming, masks.i_mask_brightstar_ghost12, masks.i_mask_brightstar_ghost15,
    masks.z_mask_brightstar_any, masks.z_mask_brightstar_halo, masks.z_mask_brightstar_dip, masks.z_mask_brightstar_ghost, masks.z_mask_brightstar_blooming, masks.z_mask_brightstar_ghost12, masks.z_mask_brightstar_ghost15,
    masks.y_mask_brightstar_any, masks.y_mask_brightstar_halo, masks.y_mask_brightstar_dip, masks.y_mask_brightstar_ghost, masks.y_mask_brightstar_blooming, masks.y_mask_brightstar_ghost12, masks.y_mask_brightstar_ghost15

FROM
    pdr3_dud.forced main
    LEFT JOIN pdr3_dud.forced3 main3 USING (object_id) 
    LEFT JOIN pdr3_dud.masks masks USING (object_id)

WHERE
    isprimary

-- LIMIT 100;