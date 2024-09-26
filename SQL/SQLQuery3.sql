SELECT DISTINCT
GENDETCON.GDEPOSSUB,
GENDETCON.GDENOMBRE,
GENPACIEN.PACPRINOM as A_NOM1_7,
CASE WHEN GENPACIEN.PACSEGNOM = '' THEN 'NONE' ELSE GENPACIEN.PACSEGNOM END as A_NOM2_8, 
GENPACIEN.PACPRIAPE AS A_APELL_5,
CASE WHEN GENPACIEN.PACSEGAPE = '' THEN 'NONE' ELSE GENPACIEN.PACSEGAPE 
END AS A_APELL2_6, 
CASE GENPACIEN.PACTIPDOC WHEN 1 THEN 'CC' WHEN 2 THEN 'CE' WHEN 3 THEN 'TI' WHEN 4 THEN 'RC' WHEN 5 THEN 'PA' WHEN 6 THEN 'AS' WHEN 7 THEN 'MS' WHEN 8 THEN 'NU' WHEN 10 THEN 'CN' WHEN 12 THEN 'PE' WHEN 14 THEN 'PE' WHEN 15 THEN 'PE' WHEN 9 THEN 'PE'
ELSE 'NONE' END AS Tipo,
GENPACIEN.PACNUMDOC AS N�mero,
FORMAT(GENPACIEN.GPAFECNAC, 'yyyy-MM-dd', 'en-us') AS fecha_nacimiento,
CASE WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' ELSE NULL END AS sexo,
----ADNGRUETN.ADGGRUETN AS Etnia,
TRY_CAST(ADNINGRESO.ADINFPACI AS XML).value('(/HCCLInfoPaciente/@DIRECC)[1]', 'VARCHAR(255)') AS Direcci�n_y_Contacto,
ADNINGRESO.AINTELACU,
GENMUNICI.MUNCODDEMU,
ADNINGRESO.AINCONSEC as ingreso,
--DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, ADNINGRESO.AINFECING) - CASE WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(ADNINGRESO.AINFECING) OR  (MONTH(GENPACIEN.GPAFECNAC) = MONTH(ADNINGRESO.AINFECING) AND DAY(GENPACIEN.GPAFECNAC) > DAY(ADNINGRESO.AINFECING))) THEN 1 ELSE 0 END AS edad,
--GENARESER.GASCODIGO,
GENARESER.GASNOMBRE,
--HCNTIPHIS.HCCODIGO,
--HCNTIPHIS.HCNOMBRE,
ADNINGRESO.AINFECING as fecha_ingreso_Fecha_de_Atenci�n,
---HCNFOLIO.HCFECFOL,
FORMAT(HCNFOLIO.HCFECFOL, 'yyyy-MM-dd', 'en-us') AS FECHA_ATENCION,
--HCNFOLIO.HPNDEFCAM,
--GENMEDICO.GMENOMCOM,
GENESPECI.GEEDESCRI,
--GENBARRIO.GEBNOMBRE AS Barrio_o_Vereda,
GENPACIEN.GPATIPPAC AS TIPO_PACIENTE,
GENPACIEN.GPATIPAFI AS TIPO_AFILIACION,
GENDIAGNO.DIACODIGO,
GENDIAGNO.DIANOMBRE,
HCNDIAPAC.HCPDIAPRIN,
CASE WHEN GENPACIEN.GPAZONRES = 1 THEN 'R' WHEN GENPACIEN.GPAZONRES = 2 THEN 'U' ELSE '' END AS ZONA,
GENESTRATO.GETNOMEST AS Nivel_Socioecon�mico,
--GENPACIEN.GPANIVEDU,
--GENMUNICI.MUNNOMMUN AS Municipio,
--TRY_CAST(ADNINGRESO.ADINFPACI AS XML).value('(/HCCLInfoPaciente/@NOMOCUPA)[1]', 'VARCHAR(255)') AS NombreOcupacion,
--ADNINGRESO.AINDIRACU AS DIRECION_ACUDIENTE,
--DATEDIFF(day, ADNINGRESO.AINFECING, HCNFOLIO.HCFECFOL) AS DiasDeDiferencia,
ROW_NUMBER() OVER (PARTITION BY ADNINGRESO.AINCONSEC ORDER BY HCNFOLIO.HCFECFOL DESC) AS rxdrn
--GENDETCON.*
--GENDETCON.*
FROM ADNINGRESO
INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
INNER JOIN HCNDIAPAC ON HCNFOLIO.OID = HCNDIAPAC.HCNFOLIO
INNER JOIN GENDIAGNO ON GENDIAGNO.OID = HCNDIAPAC.GENDIAGNO
INNER JOIN GENMUNICI ON GENPACIEN.DGNMUNICIPIO = GENMUNICI.OID
INNER JOIN GENBARRIO ON GENPACIEN.GENBARRIO = GENBARRIO.OID
INNER JOIN GENDETCON ON GENPACIEN.GENDETCON = GENDETCON.OID
--INNER JOIN X_EAPB ON GENPACIEN.GENDETCON = X_EAPB.oid
----INNER JOIN ADNGRUETN ON GENPACIEN.ADNGRUETN = ADNGRUETN.OID
INNER JOIN GENESTRATO on GENPACIEN.GENESTRATO = GENESTRATO.OID
INNER JOIN GENARESER on HCNFOLIO.GENARESER =  GENARESER.OID
INNER JOIN GENMEDICO ON HCNFOLIO.GENMEDICO = GENMEDICO.OID
INNER JOIN GENESPECI on HCNFOLIO.GENESPECI = GENESPECI.OID
INNER JOIN HCNTIPHIS on HCNFOLIO.HCNTIPHIS = HCNTIPHIS.OID
-- filtros del ingeniero
WHERE ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '2024-05-01', 120) AND CONVERT(DATETIME, '2024-07-01', 120)
--and GENARESER.GASCODIGO IN ('33511','33514','33512','33431','33421','33331','33311','33321','33513')
--and rxdrn == 1 
--and HCNDIAPAC.HCPDIAPRIN = 1 -- tipo de diagnostio
--AND HCNTIPHIS.HCCODIGO IN ('HC0016','HC0023','HC0071','HC0088','HC016W','HC023W','HC071W','HC088W','HC003W') -- folios
--and GENARESER.GASCODIGO not IN ('36112','36111','36213','36214','35711','35411','35412','35611','35221','35111','35413','14611','14312','13412','32121','35211','36411','11111','35612','11711','35511','36511','37111','36911','32112','32111','32113','31115','32114')
-- termina filtro ingeniero
--ORDER BY ADNINGRESO.AINCONSEC asc;
--AND GENPACIEN.PACNUMDOC = '1060876288'
--AND rxdrn = '1'
-- enf mentales
--AND ADNINGRESO.AINCONSEC IN ('1792824','1783978','1878057','1887373','1823328','1897617','1829382','1816320','1938407','1880174','1957962','1929957','1805406','1759296','1746172','1808352','1913306','1746741','1939307','1801361','1745335','1860147','1929970','1800772','1800418','1758430','1928666','1848775','1762343','1956495','1873962','1899649','1899570','1747633','1916180','1927632','1746339','1850158','1881805','1801285','1899740','1847312','1900125','1902507','1926379','1824569','1745975','1845924','1770162','1862487','1908138','1881010','1771584','1815106','1746985','1929767','1868221','1809406','1884702','1906779','1765089','1861037','1943026','1896151','1785940','1905185','1926832','1816366','1925341','1898837','1915955','1956908','1895389','1955035','1852460','1862423','1850971','1936674','1841039','1746800','1896436','1801520','1958490','1767914','1848090','1899745','1743818','1762491','1766630','1891948','1926459','1798523','1761868','1901161','1744865','1777597','1935786','1915636','1743639','1790663','1751782','1939702','1811111','1893847','1747231','1950806','1811471','1760638','1880980','1779278','1826339','1929514','1840667','1844624','1888212','1840519','1757001','1819121','1880770','1777115','1901249','1949082','1943567','1852183','1874559','1746944','1937441','1860140','1778891','1941511','1803444','1888821','1909318','1855414','1937824','1870718','1914264','1924485','1747005','1874347','1846050','1945868','1933062','1902014','1788596','1771311','1799471','1950008','1932221','1757791','1778932','1811778','1760847','1924829','1912546','1859129','1928302','1926990','1896927','1772458','1762564','1912306','1745857','1891940','1754899','1929786','1820679','1895348','1878396','1762377','1848676','1915052','1744893','1950306','1748356','1930642','1927117','1780250','1947009','1762520','1795508','1835493','1850822','1944210','1750539','1932531','1904932','1872825','1837407','1899958','1893906','1875506','1839038','1942864','1945703','1846972','1790440','1847343','1754715','1879072','1947806','1809400','1927310','1754441','1774377','1747618','1945516','1863027','1862880','1887331','1946105','1817377','1872739','1850991','1866471','1764762','1790714','1881139','1786102','1889676','1833816','1912771','1838841','1796093','1842490','1828179','1803222','1896398','1781960','1933741','1935303','1863531','1873499','1745492','1856585','1847387','1836042','1949848','1850115','1807056','1884105','1848351','1923671','1855309','1875518','1950154','1872392','1748299','1828266')
--AND ADNINGRESO.AINCONSEC IN ('1792824','1783978','1878057','1887373','1823328','1897617','1829382','1816320','1938407','1880174','1957962','1929957','1805406','1759296','1746172','1808352','1913306','1746741','1939307','1801361','1745335','1860147','1929970','1800772','1800418','1758430','1928666','1848775','1762343','1956495','1873962','1899649','1899570','1747633','1916180','1927632','1746339','1850158','1881805','1801285','1899740','1847312','1900125','1902507','1926379','1824569','1745975','1845924','1770162','1862487','1908138','1881010','1771584','1815106','1746985','1929767','1868221','1809406','1884702','1906779','1765089','1861037','1943026','1896151','1785940','1905185','1926832','1816366','1925341','1898837','1915955','1956908','1895389','1955035','1852460','1862423','1850971','1936674','1841039','1746800','1896436','1801520','1958490','1767914','1848090','1899745','1743818','1762491','1766630','1891948','1926459','1798523','1761868','1901161','1744865','1777597','1935786','1915636','1743639','1790663','1751782','1939702','1811111','1893847','1747231','1950806','1811471','1760638','1880980','1779278','1826339','1929514','1840667','1844624','1888212','1840519','1757001','1819121','1880770','1777115','1901249','1949082','1943567','1852183','1874559','1746944','1937441','1860140','1778891','1941511','1803444','1888821','1909318','1855414','1937824','1870718','1914264','1924485','1747005','1874347','1846050','1945868','1933062','1902014','1788596','1771311','1799471','1950008','1932221','1757791','1778932','1811778','1760847','1924829','1912546','1859129','1928302','1926990','1896927','1772458','1762564','1912306','1745857','1891940','1754899','1929786','1820679','1895348','1878396','1762377','1848676','1915052','1744893','1950306','1748356','1930642','1927117','1780250','1947009','1762520','1795508','1835493','1850822','1944210','1750539','1932531','1904932','1872825','1837407','1899958','1893906','1875506','1839038','1942864','1945703','1846972','1790440','1847343','1754715','1879072','1947806','1809400','1927310','1754441','1774377','1747618','1945516','1863027','1862880','1887331','1946105','1817377','1872739','1850991','1866471','1764762','1790714','1881139','1786102','1889676','1833816','1912771','1838841','1796093','1842490','1828179','1803222','1896398','1781960','1933741','1935303','1863531','1873499','1745492','1856585','1847387','1836042','1949848','1850115','1807056','1884105','1848351','1923671','1855309','1875518','1950154','1872392','1748299','1828266')
--and GENPACIEN.PACNUMDOC in ('1061706495','1061745633','34322284','1061818707','1061818386','1061813261','1061757299','1085247362','1058971252','1061753512','1061818849','1061753300','1061990229','1060872621')
--AND GENDIAGNO.DIACODIGO IN ('O008','O009','O080','O081','O082','O083','O084','O085','O086','O087','O088','O089','P014')
--AND (LOWER(GENDIAGNO.DIANOMBRE) LIKE '%fosfoli%' OR LOWER(GENDIAGNO.DIANOMBRE) LIKE '%ARTRITIS%' OR LOWER(GENDIAGNO.DIANOMBRE) LIKE '%lupus%')
--AND (LOWER(GENDIAGNO.DIANOMBRE) LIKE '%apendi%')
--and Tipo == 'CN'-- IN ('CN', 'MS', 'NU', 'PA', 'PE', 'RC', 'TI')
--AND GENDIAGNO.DIACODIGO IN ('M059', 'M060', 'M058', 'M069', 'M068')
AND GENPACIEN.PACNUMDOC IN ('48572981', '1064433066', '25685181', '1062306215', '25690765', '1062275829', '48659884', '34532560', '1064431418', '25350403', 
							'27172456', '1064431845', '25690988', '25681959', '25690532', '1061540008', '48660311', '48573886', '1064432583', '1064426514', 
							'48659900', '10720173', '4770576', '1064437514', '48659918', '4767939', '1064439696', '25691446', '1061535454', '25544642', 
							'25690727', '25742254', '10721535', '48660111', '10723577', '1003418259', '1064428983', '48659830', '48572970', '25690711', 
							'1064429238', '1061776661', '1064427796', '4769189', '7557422', '1064426143', '25544106', '48570271', '48571625', '48574046', 
							'25060947', '1059597905', '10723035', '1061536213', '41109052', '25691189', '1064441031', '36273404', '25744310', '25683585', 
							'31884043', '1144047225', '48572673', '1061529759', '25682507', '25683533', '10620398', '1002962960', '48659858', '48652870', 
							'25690949', '25688720', '48572884', '1064436288', '25691384', '48572217', '10620016', '25685196', '25172456')

--AND GENESPECI.GEEDESCRI NOT IN ('MEDICINA GENERAL', 'ENFERMERIA ONCOLOGICA')
ORDER BY rxdrn asc;