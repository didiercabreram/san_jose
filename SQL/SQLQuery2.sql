SELECT DISTINCT

                    --DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, '2024-08-02') - 
                    --    CASE
                    --        WHEN DATEDIFF(MONTH, GENPACIEN.GPAFECNAC, '2024-08-02') > 0 OR 
                    --            (DATEDIFF(MONTH, GENPACIEN.GPAFECNAC, '2024-08-02') = 0 AND DATEDIFF(DAY, GENPACIEN.GPAFECNAC, '2024-08-02') > 0) THEN 1
                    --        ELSE 0
                    --    END AS edad,

                        GENPACIEN.PACNUMDOC AS A_NODOC_4,
                        HCNFOLIO.HCFECFOL,
                        GENSERIPS.SIPCODCUP,
                        GENSERIPS.SIPDESCUP,
                        HCNRESEXA.HCRFECRES,
                        HCNRESEXA.HCRDESCRIP
                    FROM
                        HCNFOLIO
                    INNER JOIN
                        GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
                    INNER JOIN
                        HCNRESEXA ON HCNFOLIO.OID = HCNRESEXA.HCNFOLIO
                    INNER JOIN
                        HCNSOLEXA ON HCNSOLEXA.OID = HCNRESEXA.HCNSOLEXA
                    INNER JOIN
                        GENSERIPS ON GENSERIPS.OID = HCNSOLEXA.GENSERIPS
                    WHERE
                        HCNFOLIO.HCFECFOL BETWEEN CONVERT(DATETIME, '2024-08-01', 120) AND CONVERT(DATETIME, '2024-08-02', 120)
						--ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '2024-07-01', 120) AND CONVERT(DATETIME, '2024-08-02', 120)
                        --AND GENSERIPS.SIPCODCUP IN {exam}
                    ORDER BY
                        HCNFOLIO.HCFECFOL DESC;