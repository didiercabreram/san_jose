-- NOMBRES Y DATOS INICIALES

SELECT DISTINCT

GENPACIEN.PACNUMDOC AS A_4_N�mero,
DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, ADNINGRESO.AINFECING) - CASE WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(ADNINGRESO.AINFECING) OR  (MONTH(GENPACIEN.GPAFECNAC) = MONTH(ADNINGRESO.AINFECING) AND DAY(GENPACIEN.GPAFECNAC) > DAY(ADNINGRESO.AINFECING))) THEN 1 ELSE 0 END AS A_0_EDAD,

CASE GENPACIEN.PACTIPDOC WHEN 1 THEN 'CC' WHEN 2 THEN 'CE' WHEN 3 THEN 'TI' WHEN 4 THEN 'RC' WHEN 5 THEN 'PA' WHEN 6 THEN 'AS' WHEN 7 THEN 'MS' WHEN 8 THEN 'NU' WHEN 10 THEN 'CN' WHEN 12 THEN 'PE' WHEN 14 THEN 'PE' WHEN 15 THEN 'PE' WHEN 9 THEN 'PE'
ELSE 'NONE' END AS A_3_TIPODOC,
GENPACIEN.PACPRIAPE AS A_5_APELLIDO1,
CASE WHEN GENPACIEN.PACSEGAPE = '' THEN 'NONE' ELSE GENPACIEN.PACSEGAPE END AS A_6_APELLIDO2, 
GENPACIEN.PACPRINOM as A_7_NOMBRE1,
CASE WHEN GENPACIEN.PACSEGNOM = '' THEN 'NONE' ELSE GENPACIEN.PACSEGNOM END as A_8_NOMBRE1, 
FORMAT(GENPACIEN.GPAFECNAC, 'yyyy-MM-dd', 'en-us') AS A_9_NACIMIENTO,
CASE WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' ELSE NULL END AS A_10_SEXO
--GENPACIEN.GPANIVEDU

FROM ADNINGRESO
INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
-- filtros
WHERE ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '2024-09-06', 120) AND CONVERT(DATETIME, '2024-09-07', 120)

--AND GENPACIEN.PACNUMDOC IN ('25544106', '25544642')


