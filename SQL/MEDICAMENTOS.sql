-- DESCARGA DE MEDICAMENTOS

SELECT DISTINCT
--ADNINGRESO.AINCONSEC as ingreso
GENPACIEN.PACNUMDOC AS A_NODOC_4,
FORMAT(HCNFOLIO.HCFECFOL, 'yyyy-MM-dd', 'en-us') AS F_Resultado,
CASE WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' ELSE NULL END AS sexo,
                        --HCNMEDPAC.HCSINTRAH,
                        INNPRODUC.IPRCODIGO,
                        INNPRODUC.IPRDESCOR,
						GENCONFAC.GCFNOMBRE
                    FROM
                        ADNINGRESO
					INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
                    INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
                    INNER JOIN HCNMEDPAC ON HCNFOLIO.OID = HCNMEDPAC.HCNFOLIO
                    INNER JOIN INNPRODUC ON HCNMEDPAC.INNPRODUC = INNPRODUC.OID
					INNER JOIN GENCONFAC ON GENCONFAC.OID = INNPRODUC.GENCONFAC
                    WHERE
                        HCNFOLIO.HCFECFOL BETWEEN CONVERT(DATETIME, '2024-09-10', 120) AND CONVERT(DATETIME, '2024-09-11', 120)
                        --AND INNPRODUC.IPRCODIGO IN ('DMT0001253')
                        and HCNMEDPAC.HCSINTRAH = 1
						AND GENPACIEN.GPASEXPAC = 2
                    --ORDER BY
                    --    HCNFOLIO.HCFECFOL DESC;







SELECT DISTINCT
                        DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, HCNFOLIO.HCFECFOL) - 
                            CASE
                                WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(HCNFOLIO.HCFECFOL) OR 
                                    (MONTH(GENPACIEN.GPAFECNAC) = MONTH(HCNFOLIO.HCFECFOL) AND DAY(GENPACIEN.GPAFECNAC) > DAY(HCNFOLIO.HCFECFOL))) THEN 1
                                ELSE 0
                            END AS edad,

                        GENPACIEN.PACNUMDOC AS A_NODOC_4,
                        HCNFOLIO.HCFECFOL,
                        HCNMEDPAC.HCSINTRAH,
                        INNPRODUC.IPRCODIGO,
                        CASE 
                            WHEN INNPRODUC.IPRCODIGO = 'G03AA080900' THEN 'w9'
                            WHEN INNPRODUC.IPRCODIGO = 'NPP0000004' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'G03FA110100' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'G03AC031010' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'G03DM004011' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'G03AC09000-1' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'NPY0000001' THEN 'x5'
                            WHEN INNPRODUC.IPRCODIGO = 'G03DM004711' THEN 'y7'
                            WHEN INNPRODUC.IPRCODIGO = 'G03AC030001' THEN 'b3'
                            WHEN INNPRODUC.IPRCODIGO = 'G03AC080100' THEN 'b3'
                            WHEN INNPRODUC.IPRCODIGO = 'G03AC030100' THEN 'c1'
                            WHEN INNPRODUC.IPRCODIGO = 'DMC0000051' THEN 'z15'
                            ELSE INNPRODUC.IPRCODIGO 
                        END AS b_54,
                        INNPRODUC.IPRDESCOR
                    FROM
                        HCNFOLIO
                    INNER JOIN
                        GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
                    INNER JOIN
                        HCNMEDPAC ON HCNFOLIO.OID = HCNMEDPAC.HCNFOLIO
                    INNER JOIN
                        INNPRODUC ON HCNMEDPAC.INNPRODUC = INNPRODUC.OID
                    WHERE
                        HCNFOLIO.HCFECFOL BETWEEN CONVERT(DATETIME, '2024-09-01', 120) AND CONVERT(DATETIME, '2024-09-02', 120)
                        --AND INNPRODUC.IPRCODIGO IN {list}
                        and HCNMEDPAC.HCSINTRAH = 1
                    ORDER BY
                        HCNFOLIO.HCFECFOL DESC;


