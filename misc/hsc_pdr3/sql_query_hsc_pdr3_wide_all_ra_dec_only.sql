SELECT
    main.ra,
    main.dec
FROM
    pdr3_wide.forced main
WHERE
    isprimary
    AND (g_cmodel_mag<25.0 OR r_cmodel_mag<25.0 OR i_cmodel_mag<24.4 OR z_cmodel_mag<23.7)

-- LIMIT 100;