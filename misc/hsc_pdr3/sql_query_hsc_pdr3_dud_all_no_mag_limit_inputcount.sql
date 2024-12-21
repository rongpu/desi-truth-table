SELECT
    main.object_id, main.g_inputcount_value, main.r_inputcount_value, main.i_inputcount_value, main.z_inputcount_value, main.y_inputcount_value

FROM
    pdr3_dud.forced main

WHERE
    isprimary

-- LIMIT 100;