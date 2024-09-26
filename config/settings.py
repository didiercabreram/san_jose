import os
from dotenv import load_dotenv
load_dotenv()



def eapb(fec_init, fec_final):
    return f"""
        SELECT DISTINCT
        GENPACIEN.PACNUMDOC AS A_4_Número,
        GENDETCON.GDENOMBRE AS A_0_EAPB,
        CASE WHEN GENDETCON.GDEPOSSUB = 1 THEN 'SUBSIDIADO' WHEN GENDETCON.GDEPOSSUB = 0 THEN 'CONTRIBUTIVO' ELSE '' END AS A_1_EAPB
        --FORMAT(ADNINGRESO.AINFECING, 'yyyy-MM-dd', 'en-us') AS F_init
        FROM ADNINGRESO
        INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
        INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
        INNER JOIN GENDETCON ON GENPACIEN.GENDETCON = GENDETCON.OID
        -- filtros
        WHERE ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '{fec_init}', 120) AND CONVERT(DATETIME, '{fec_final}', 120)
        """


def datos_init(fec_init, fec_final):
    return f"""SELECT DISTINCT
            GENPACIEN.PACNUMDOC AS A_4_Número,
            DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, ADNINGRESO.AINFECING) - CASE WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(ADNINGRESO.AINFECING) OR  (MONTH(GENPACIEN.GPAFECNAC) = MONTH(ADNINGRESO.AINFECING) AND DAY(GENPACIEN.GPAFECNAC) > DAY(ADNINGRESO.AINFECING))) THEN 1 ELSE 0 END AS A_0_EDAD,
            CASE GENPACIEN.PACTIPDOC WHEN 1 THEN 'CC' WHEN 2 THEN 'CE' WHEN 3 THEN 'TI' WHEN 4 THEN 'RC' WHEN 5 THEN 'PA' WHEN 6 THEN 'AS' WHEN 7 THEN 'MS' WHEN 8 THEN 'NU' WHEN 10 THEN 'CN' WHEN 12 THEN 'PE' WHEN 14 THEN 'PE' WHEN 15 THEN 'PE' WHEN 9 THEN 'PE'
            ELSE 'NONE' END AS A_3_TIPODOC,
            GENPACIEN.PACPRIAPE AS A_5_APELLIDO1,
            CASE WHEN GENPACIEN.PACSEGAPE = '' THEN 'NONE' ELSE GENPACIEN.PACSEGAPE END AS A_6_APELLIDO2, 
            GENPACIEN.PACPRINOM as A_7_NOMBRE1,
            CASE WHEN GENPACIEN.PACSEGNOM = '' THEN 'NONE' ELSE GENPACIEN.PACSEGNOM END as A_8_NOMBRE1, 
            FORMAT(GENPACIEN.GPAFECNAC, 'yyyy-MM-dd', 'en-us') AS A_9_NACIMIENTO,
            CASE WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' ELSE NULL END AS A_10_SEXO,
            GENPACIEN.GPANIVEDU
            FROM ADNINGRESO
            INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
            INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
            -- filtros
            WHERE ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '{fec_init}', 120) AND CONVERT(DATETIME, '{fec_final}', 120)
            """

def gestante(fec_init, fec_final):
    return f"""
    SELECT DISTINCT
        GENPACIEN.PACNUMDOC AS Número,
        CASE 
            WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' 
            WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' 
            ELSE NULL 
        END AS sexo,
        --ADNINGRESO.AINCONSEC as ingreso,
        DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, ADNINGRESO.AINFECING) - 
            CASE 
                WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(ADNINGRESO.AINFECING) OR  
                    (MONTH(GENPACIEN.GPAFECNAC) = MONTH(ADNINGRESO.AINFECING) AND DAY(GENPACIEN.GPAFECNAC) > DAY(ADNINGRESO.AINFECING))) 
                THEN 1 
                ELSE 0 
            END AS edad,
        --GENDIAGNO.DIACODIGO,
        --GENDIAGNO.DIANOMBRE,
        CASE
            WHEN GENDIAGNO.DIACODIGO IN ('O100','O101','O102','O103','O104','O109','O11X','O120','O121','O122','O13X','O140','O141','O142','O149','O150','O151','O152','O159','O16X','O200','O208','O209','O210','O211','O212','O218','O219','O220','O221','O222','O223','O224','O225','O228','O229','O230','O231','O232','O233','O234','O235','O239','O240','O241','O242','O243','O244','O249','O25X','O260','O261','O262','O263','O264','O265','O266','O267','O268','O269','O280','O281','O282','O283','O284','O285','O288','O289','O290','O291','O292','O293','O294','O295','O296','O298','O299','O300','O301','O302','O308','O309','O311','O318','O320','O321','O322','O323','O324','O325','O326','O328','O329','O330','O331','O332','O333','O334','O335','O336','O337','O338','O339','O340','O341','O342','O343','O344','O345','O346','O347','O348','O349','O350','O351','O352','O353','O354','O355','O356','O357','O358','O359','O360','O361','O362','O363','O365','O366','O367','O368','O369','O40X','O410','O411','O418','O419','O420','O421','O422','O429','O430','O431','O432','O438','O439','O450','O458','O459','O470','O471','O479','O48X','O710','O712','O715','O716','O717','O718','O719','O880','O881','O882','O883','O888','O93X','O980','O981','O982','O983','O984','O985','O986','O987','O988','O989','O990','O991','O992','O993','O994','O995','O996','O997','O998','P080','P081','P082','Z321','Z33X','Z340','Z348','Z349','Z350','Z351','Z352','Z353','Z354','Z355','Z356','Z357','Z358','Z359','Z640')
            THEN 'Gestantes'
            WHEN GENDIAGNO.DIACODIGO IN ('O000','O001','O002','O008','O009','O010','O011','O019','O020','O021','O028','O029','O030','O031','O032','O033','O034','O035','O036','O037','O038','O039','O040','O041','O042','O043','O044','O045','O046','O047','O048','O049','O050','O051','O052','O053','O054','O055','O056','O057','O058','O059','O060','O061','O062','O063','O064','O065','O066','O067','O068','O069','O070','O071','O072','O073','O074','O075','O076','O077','O078','O079','O080','O081','O082','O083','O084','O085','O086','O087','O088','O089','O312','O364','P964')
            THEN 'Abortos'
            WHEN GENDIAGNO.DIACODIGO IN ('O95X','O960','O961','O969','O970','O971','O979','O310','O440','O441','O460','O468','O469','O600','O601','O602','O603','O60X','O610','O611','O618','O619','O620','O621','O622','O623','O624','O628','O629','O630','O631','O632','O639','O640','O641','O642','O643','O644','O645','O648','O649','O650','O651','O652','O653','O654','O655','O658','O659','O660','O661','O662','O663','O664','O665','O668','O669','O670','O678','O679','O680','O681','O682','O683','O688','O689','O690','O691','O692','O693','O694','O695','O698','O699','O700','O701','O702','O703','O709','O711','O713','O714','O720','O721','O722','O723','O730','O731','O740','O741','O742','O743','O744','O745','O746','O747','O748','O749','O750','O751','O752','O753','O754','O755','O756','O757','O758','O759','O800','O801','O808','O809','O810','O811','O812','O813','O814','O815','O820','O821','O822','O828','O829','O830','O831','O832','O833','O834','O838','O839','O840','O841','O842','O848','O849','O85X','O860','O861','O862','O863','O864','O868','O870','O871','O872','O873','O878','O879','O890','O891','O892','O893','O894','O895','O896','O898','O899','O900','O901','O902','O903','O904','O905','O908','O909','O910','O911','O912','O920','O921','O922','O923','O924','O925','O926','O927','O94X')
            THEN 'Parto'
            ELSE 'Otro'
        END AS Grupo_Diagnostico
    FROM ADNINGRESO
    INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
    INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
    INNER JOIN HCNDIAPAC ON HCNFOLIO.OID = HCNDIAPAC.HCNFOLIO
    INNER JOIN GENDIAGNO ON GENDIAGNO.OID = HCNDIAPAC.GENDIAGNO
    WHERE ADNINGRESO.AINFECING BETWEEN CONVERT(DATETIME, '{fec_init}', 120) AND CONVERT(DATETIME, '{fec_final}', 120)
    AND GENDIAGNO.DIACODIGO IN ('O95X','O960','O961','O969','O970','O971','O979','O310','O440','O441','O460','O468','O469','O600','O601','O602','O603','O60X','O610','O611','O618','O619','O620','O621','O622','O623','O624','O628','O629','O630','O631','O632','O639','O640','O641','O642','O643','O644','O645','O648','O649','O650','O651','O652','O653','O654','O655','O658','O659','O660','O661','O662','O663','O664','O665','O668','O669','O670','O678','O679','O680','O681','O682','O683','O688','O689','O690','O691','O692','O693','O694','O695','O698','O699','O700','O701','O702','O703','O709','O711','O713','O714','O720','O721','O722','O723','O730','O731','O740','O741','O742','O743','O744','O745','O746','O747','O748','O749','O750','O751','O752','O753','O754','O755','O756','O757','O758','O759','O800','O801','O808','O809','O810','O811','O812','O813','O814','O815','O820','O821','O822','O828','O829','O830','O831','O832','O833','O834','O838','O839','O840','O841','O842','O848','O849','O85X','O860','O861','O862','O863','O864','O868','O870','O871','O872','O873','O878','O879','O890','O891','O892','O893','O894','O895','O896','O898','O899','O900','O901','O902','O903','O904','O905','O908','O909','O910','O911','O912','O920','O921','O922','O923','O924','O925','O926','O927','O94X','O000','O001','O002','O008','O009','O010','O011','O019','O020','O021','O028','O029','O030','O031','O032','O033','O034','O035','O036','O037','O038','O039','O040','O041','O042','O043','O044','O045','O046','O047','O048','O049','O050','O051','O052','O053','O054','O055','O056','O057','O058','O059','O060','O061','O062','O063','O064','O065','O066','O067','O068','O069','O070','O071','O072','O073','O074','O075','O076','O077','O078','O079','O080','O081','O082','O083','O084','O085','O086','O087','O088','O089','O312','O364','P964','O100','O101','O102','O103','O104','O109','O11X','O120','O121','O122','O13X','O140','O141','O142','O149','O150','O151','O152','O159','O16X','O200','O208','O209','O210','O211','O212','O218','O219','O220','O221','O222','O223','O224','O225','O228','O229','O230','O231','O232','O233','O234','O235','O239','O240','O241','O242','O243','O244','O249','O25X','O260','O261','O262','O263','O264','O265','O266','O267','O268','O269','O280','O281','O282','O283','O284','O285','O288','O289','O290','O291','O292','O293','O294','O295','O296','O298','O299','O300','O301','O302','O308','O309','O311','O318','O320','O321','O322','O323','O324','O325','O326','O328','O329','O330','O331','O332','O333','O334','O335','O336','O337','O338','O339','O340','O341','O342','O343','O344','O345','O346','O347','O348','O349','O350','O351','O352','O353','O354','O355','O356','O357','O358','O359','O360','O361','O362','O363','O365','O366','O367','O368','O369','O40X','O410','O411','O418','O419','O420','O421','O422','O429','O430','O431','O432','O438','O439','O450','O458','O459','O470','O471','O479','O48X','O710','O712','O715','O716','O717','O718','O719','O880','O881','O882','O883','O888','O93X','O980','O981','O982','O983','O984','O985','O986','O987','O988','O989','O990','O991','O992','O993','O994','O995','O996','O997','O998','P080','P081','P082','Z321','Z33X','Z340','Z348','Z349','Z350','Z351','Z352','Z353','Z354','Z355','Z356','Z357','Z358','Z359','Z640')
    AND GENPACIEN.GPASEXPAC = 2
    """

def obtener_laborat(fec_init, fec_final):
    return  f"""
    SELECT DISTINCT
    GENPACIEN.PACNUMDOC AS A_4_Número,
        CASE WHEN GENPACIEN.GPASEXPAC = 1 THEN 'M' WHEN GENPACIEN.GPASEXPAC = 2 THEN 'F' ELSE NULL END AS A_10_SEXO,
            DATEDIFF(YEAR, GENPACIEN.GPAFECNAC, ADNINGRESO.AINFECING) - CASE WHEN (MONTH(GENPACIEN.GPAFECNAC) > MONTH(ADNINGRESO.AINFECING) OR  (MONTH(GENPACIEN.GPAFECNAC) = MONTH(ADNINGRESO.AINFECING) AND DAY(GENPACIEN.GPAFECNAC) > DAY(ADNINGRESO.AINFECING))) THEN 1 ELSE 0 END AS A_0_EDAD,
                FORMAT(HCNRESEXA.HCRFECRES, 'yyyy-MM-dd', 'en-us') AS F_Resultado,
                GENSERIPS.SIPCODCUP AS Información_Servicio,
                
                CASE 
                WHEN GENSERIPS.SIPCODCUP = '901101' THEN 'BACILOSCOPIA'
                WHEN GENSERIPS.SIPCODCUP = '907008' THEN 'SANGRE_OCULTAMF'
                WHEN GENSERIPS.SIPCODCUP = '906610' THEN 'ANTIGENO_PROSTATA'
                WHEN GENSERIPS.SIPCODCUP = '903895' THEN 'CREATININA' 
                WHEN GENSERIPS.SIPCODCUP = '906625' THEN 'GONADOTROPINA'
                WHEN GENSERIPS.SIPCODCUP = '904508' THEN 'GONADOTROPINA'
                WHEN GENSERIPS.SIPCODCUP = '903815' THEN 'COLESTEROL_HDL'
                WHEN GENSERIPS.SIPCODCUP = '902210' THEN 'HEMOGRAMA' 
                WHEN GENSERIPS.SIPCODCUP = '902213' THEN 'HEMOGRAMA'
                WHEN GENSERIPS.SIPCODCUP = '908806' THEN 'HEPATITIS_B'
                WHEN GENSERIPS.SIPCODCUP = '906223' THEN 'HEPATITIS_B'
                WHEN GENSERIPS.SIPCODCUP = '906317' THEN 'HEPATITIS_B'
                WHEN GENSERIPS.SIPCODCUP = '906225' THEN 'Hepatitis_C'
                WHEN GENSERIPS.SIPCODCUP = '908807' THEN 'Hepatitis_C'
                WHEN GENSERIPS.SIPCODCUP = '903816' THEN 'COLESTEROL_LDL'
                WHEN GENSERIPS.SIPCODCUP = '906039' THEN 'Treponema_pallidum'
                WHEN GENSERIPS.SIPCODCUP = '903868' THEN 'TRIGLICERIDOS' 
                WHEN GENSERIPS.SIPCODCUP = '906249' THEN 'Virus_Inmunodeficiencia'
                WHEN GENSERIPS.SIPCODCUP = '908832' THEN 'Virus_Inmunodeficiencia'
                WHEN GENSERIPS.SIPCODCUP = '18504' THEN 'COLONOSCOPIA'

                ELSE GENSERIPS.SIPCODCUP END AS tipo_exam,
                GENSERIPS.SIPDESCUP,

                HCNRESEXA.HCRDESCRIP AS Descripción
                FROM ADNINGRESO
                INNER JOIN HCNFOLIO ON HCNFOLIO.ADNINGRESO = ADNINGRESO.OID
                INNER JOIN GENPACIEN ON HCNFOLIO.GENPACIEN = GENPACIEN.OID
                INNER JOIN HCNSOLEXA ON HCNFOLIO.OID = HCNSOLEXA.HCNFOLIO
                INNER JOIN HCNRESEXA ON HCNSOLEXA.OID = HCNRESEXA.HCNSOLEXA
                INNER JOIN GENSERIPS ON GENSERIPS.OID = HCNSOLEXA.GENSERIPS
                WHERE GENSERIPS.SIPCODCUP IN ('902210','903895','903868','906249','906039','906625','906317','906225','901101','903815','903815','907008','902213',
                '903816','904508','906610','908807','908806','908832','906223')
                AND HCNRESEXA.HCRFECRES BETWEEN CONVERT(DATETIME, '{fec_init}', 120) AND CONVERT(DATETIME, '{fec_final}', 120)
    """



a = "1_data_new"# carpetas de descarga

a1 = "1_name"
a2 = "2_peso"
a3 = "3_exam"

a3a = f"BACILOSCOPIA"# ok
a3b = f"SANGRE_OCULTAMF"# ok
a3c = f"ANTIGENO_PROSTATA"# ok
a3d = f"CREATININA"# ok
a3e = f"GONADOTROPINA"# ok
a3f = f"COLESTEROL_HDL"# ok
a3g = f"HEMOGRAMA"# ok
a3h = f"HEPATITIS_B"# ok
a3i = f"Hepatitis_C"# ok
a3j = f"COLESTEROL_LDL"# ok
a3k = f"Treponema_pallidum"# ok
a3l = f"TRIGLICERIDOS"
a3m = f"Virus_Inmunodeficiencia"
a3z = f"nueva_eps"

a4 = "4_lab"
a5 = "5_medicament"
a6 = "6_fpp"
a7 = "7_riego_gesta"
a8 = "8_recien_nacido"
a9 = "9_colposcopia"
a10 = "10_gestantes"
a11 = "11_visual_cariopa"
a12 = "12_salida_materna"

medio = "2_data_tra"# procesacion
fin = "3_result"# resultado final
cuatro = "4_validate"
extra = "extra"
listo = '5_empre'

# examenes
embarazo = ('904508','904508')
prostata = ('19140','906610')
colon = ('907008','907012')
hemobina = ('902208','902209','902210','902213')
hdl = ("903815","903815")
ldl = ("903817","903817")
creatinina = ("903895","903895")
triglicerid = ("903868","903868")
baciloscopia = ("901101","901111")
sifilis = ("906039","906039")
hepatitisc = ("906225","906225")
hepatitisb = ("906220","906223","906317")
vih = ("906249","906250","908832")

temp = "temp"

nueva_eps_cie = ('Z300','Z304','Z308','Z309','N974','N979','N970','N972','N971','N978','N973','O822')
nueva_eps_cups = ('680100','684000','684001','684010','684020','684100','684101','685110','685120','685130','686100','687000','663910','663100','662200','662100','890201','890301','890283','890383','890250','890350','890263','890363','890205','890305','890201','890301','890283','890383','890250','890350','890263','890363','890205','890305','663910','663100','697100','861801')

config = {
    "colm":{
        "m1": os.getenv("MJ1"),
    },
    "carpetas": {
        a: {
            a1, a2, a4, a5, a6, a7, a8, a9, a10, a11, a12,
            f'{a3}//{a3a}', 
            f'{a3}//{a3b}', 
            f'{a3}//{a3c}', 
            f'{a3}//{a3d}', 
            f'{a3}//{a3e}', 
            f'{a3}//{a3f}', 
            f'{a3}//{a3g}', 
            f'{a3}//{a3h}', 
            f'{a3}//{a3i}', 
            f'{a3}//{a3j}', 
            f'{a3}//{a3k}', 
            f'{a3}//{a3l}', 
            f'{a3}//{a3m}', 
            f'{a3}//{a3z}',
            fin
        },
        medio: {},
        fin: {},
        temp: {},
        cuatro:{},
        extra: {'cirugia','etnia'},
        listo:{}
    },
    "meds":{'G03AA080900','DMC0000051','G03FA110100','G03DM004711','G03AC080100','G03AC030001','G03AL005161','G03CE017161','G03CE017361',
            'G03DH010701','G03DM004011','NPP0000008','NPY0000001','NPM0000017','DMK0000013','NPM0000017-1','NPG03AC0330','G03AC030300',
            'G03DM004711-1','VPC0000003','NPG03DA0403','G03FA110100-1','DMK0000035','G03AC080102','G03AC031100','G03AC031101','G03AC080100-1',
            'G03AC030100','G03FA040001','G03AC09000-1','DMT0001253'
    },
    "gestantes":{'O100','O101','O102','O103','O104','O109','O11X','O120','O121','O122','O13X','O140','O141','O142','O149','O150','O151','O152','O159','O16X','O200','O208','O209','O210','O211','O212','O218','O219','O220','O221','O222','O223','O224','O225','O228','O229','O230','O231','O232','O233','O234','O235','O239','O240','O241','O242','O243','O244','O249','O25X','O260','O261','O262','O263','O264','O265','O266','O267','O268','O269','O280','O281','O282','O283','O284','O285','O288','O289','O290','O291','O292','O293','O294','O295','O296','O298','O299','O300','O301','O302','O308','O309','O311','O318','O320','O321','O322','O323','O324','O325','O326','O328','O329','O330','O331','O332','O333','O334','O335','O336','O337','O338','O339','O340','O341','O342','O343','O344','O345','O346','O347','O348','O349','O350','O351','O352','O353','O354','O355','O356','O357','O358','O359','O360','O361','O362','O363','O365','O366','O367','O368','O369','O40X','O410','O411','O418','O419','O420','O421','O422','O429','O430','O431','O432','O438','O439','O450','O458','O459','O470','O471','O479','O48X','O710','O712','O715','O716','O717','O718','O719','O880','O881','O882','O883','O888','O93X','O980','O981','O982','O983','O984','O985','O986','O987','O988','O989','O990','O991','O992','O993','O994','O995','O996','O997','O998','P080','P081','P082','Z321','Z33X','Z340','Z348','Z349','Z350','Z351','Z352','Z353','Z354','Z355','Z356','Z357','Z358','Z359','Z640'
    },
    "aborto":{'O000','O001','O002','O008','O009','O010','O011','O019','O020','O021','O028','O029','O030','O031','O032','O033','O034','O035','O036','O037','O038','O039','O040','O041','O042','O043','O044','O045','O046','O047','O048','O049','O050','O051','O052','O053','O054','O055','O056','O057','O058','O059','O060','O061','O062','O063','O064','O065','O066','O067','O068','O069','O070','O071','O072','O073','O074','O075','O076','O077','O078','O079','O080','O081','O082','O083','O084','O085','O086','O087','O088','O089','O312','O364','P964'
    },
    "parto":{'O95X','O960','O961','O969','O970','O971','O979','O310','O440','O441','O460','O468','O469','O600','O601','O602','O603','O60X','O610','O611','O618','O619','O620','O621','O622','O623','O624','O628','O629','O630','O631','O632','O639','O640','O641','O642','O643','O644','O645','O648','O649','O650','O651','O652','O653','O654','O655','O658','O659','O660','O661','O662','O663','O664','O665','O668','O669','O670','O678','O679','O680','O681','O682','O683','O688','O689','O690','O691','O692','O693','O694','O695','O698','O699','O700','O701','O702','O703','O709','O711','O713','O714','O720','O721','O722','O723','O730','O731','O740','O741','O742','O743','O744','O745','O746','O747','O748','O749','O750','O751','O752','O753','O754','O755','O756','O757','O758','O759','O800','O801','O808','O809','O810','O811','O812','O813','O814','O815','O820','O821','O822','O828','O829','O830','O831','O832','O833','O834','O838','O839','O840','O841','O842','O848','O849','O85X','O860','O861','O862','O863','O864','O868','O870','O871','O872','O873','O878','O879','O890','O891','O892','O893','O894','O895','O896','O898','O899','O900','O901','O902','O903','O904','O905','O908','O909','O910','O911','O912','O920','O921','O922','O923','O924','O925','O926','O927','O94X'
    },
    "nueva_eps":{'Z300','Z304','Z308','Z309','N974','N979','N970','N972','N971','N978','N973','O822'
    },
    "exams_scan":{
    a3j: r"colesterolldl(\d+\.\d+)",
    a3f: r"colesterolhdl(.{0,2})",
    a3d: r'creatininaensuero(\d+\.\d+)',
    a3l: r"trigliceridos(.{03})",
    a3e: r"pruebaembarazoensuero(.{05})",
    a3c: r"psaantigenoprostaticoespecificototal(.{03})",
    a3b: r"sangreocultacoproscopico(.{05})",
    a3g: r"hemoglobina(.{04})",
    a3a: r"(.{014})b.a.a.r",# baciloscopias
    a3k: r'treponemapallidumanticuerpos(.{0,7})',
    a3i: r"hepatitisc(.{0,7})",
    a3h: r"hepatitisbantigenodesuperficie(.{0,1})",
    a3m: r"hiv1y2pruebarapida(.{0,7})"
    },
    "exams":{
    ldl: f"{a3j}//{a3j}",
    hdl: f"{a3f}//{a3f}",
    creatinina: f"{a3d}//{a3d}",
    triglicerid: f"{a3l}//{a3l}",
    embarazo: f"{a3e}//{a3e}",
    prostata: f"{a3c}//{a3c}",
    colon: f"{a3b}//{a3b}",
    hemobina: f"{a3g}//{a3g}",
    baciloscopia: f"{a3a}//{a3a}",
    sifilis: f"{a3k}//{a3k}",
    hepatitisc: f"{a3i}//{a3i}",
    hepatitisb: f"{a3h}//{a3h}",
    vih: f"{a3m}//{a3m}",
    nueva_eps_cups: f"{a3z}//{a3z}"
    },
    "validate":{
        "22_consumo_tabaco": {
            "cols":"'b_19'",
            "colum_remp":{'b_19': '98'},
            "var_limp":{'edad': 'edad < 12'}
            },
        "0_hemoglobina": {
            "cols":"'b_103','b_104''",
            "colum_remp":{'b_103': '1845-01-01', 'b_104': '0'},
            "var_limp":{'genero': 'A_SEX_10 == "M"', 'edad': 'edad < 10', 'edad2': 'edad > 60'}
            },
        "3_parto_salida_p": {
            "cols":"'b_49','b_50''",
            "colum_remp":{'b_49': '1845-01-01', 'b_50': '1845-01-01'},
            "var_limp":{'genero': 'A_SEX_10 == "M"', 'edad': 'edad < 10', 'edad2': 'edad > 60'}
        },
        "1_var_init": {
            "cols":"'GDENOMBRE','A_APELL_5','A_APELL2_6','A_NOM1_7','A_NOM2_8','A_FECNA_9','A_ETN_11','A_OCUP_12','A_NEDU_13','A_PAIS_34'",
            "colum_remp":{'no aplica'},
            "var_limp":{'no aplica'}
        },
        "2_toda_poblacion": {
            "cols":"'b_29','b_30','b_31','b_32','b_42','b_52','b_78','b_79','b_80','b_81','b_82','b_83','b_110','b_15','b_17','b_20','b_21','b_25','b_26','b_39','b_41','b_68','b_74','b_108','b_115','b_116','b_51','b_57','b_105'",
            "colum_remp":{'no aplica'},
            "var_limp":{'no aplica'}
        },
        "4_cancer_protata": {
            "cols":"'b_22', 'b_64', 'b_73', 'b_109'",
            "colum_remp":{'b_22': '0', 'b_64': '1845-01-01', 'b_73': '1845-01-01', 'b_109': '0'},
            "var_limp":{'genero': 'A_SEX_10 == "F"', 'edad': 'edad < 40'}
        },
        "5_cancer_colon": {
            "cols":"'b_24', 'b_36', 'b_66', 'b_67'",
            "colum_remp":{'b_24': '0', 'b_36': '0', 'b_66': '1845-01-01', 'b_67': '1845-01-01'},
            "var_limp":{'genero': 'edad > 76', 'edad': 'edad < 50'}
        },
        "6_cancer_mama": {
            "cols":"'b_96', 'b_97', 'b_99', 'b_100', 'b_101'",
            "colum_remp":{'b_96': '1845-01-01', 'b_97': '0', 'b_99': '1845-01-01', 'b_100': '1845-01-01', 'b_101': '0'},
            "var_limp":{'genero': 'A_SEX_10 == "M"', 'edad': 'edad < 35'}
        },
        "7_cancer_cervix": {
            "cols":"'b_47','b_86','b_87','b_88','b_89','b_90','b_91','b_93','b_94'",
            "colum_remp":{'b_47': '0','b_86': '0', 'b_87': '1845-01-01', 'b_88': '0', 'b_89': '0','b_90': '0','b_91': '1845-01-01','b_93': '1845-01-01','b_94': '0'},
            "var_limp":{'genero': 'A_SEX_10 == "M"', 'edad': 'edad < 10'}
        },
        "8_agudeza_visual": {
            "cols":"'b_27','b_28','b_62'",
            "colum_remp":{'b_27': '0','b_28': '0', 'b_62': '1845-01-01'},
            "var_limp":{'edad': 'edad < 3'}
        },
        "9_anticoncepcion": {
            "cols":"'b_53','b_54','b_55'",
            "colum_remp":{'b_53': '1845-01-01','b_54': '0', 'b_55': '1845-01-01'},
            "var_limp":{'edad': 'edad < 10', 'edad2': 'edad >= 60'}
        },
        "10_tuberculosis": {
            "cols":"'b_18','b_112','b_113'",
            "colum_remp":{'b_18': '21','b_112': '1845-01-01', 'b_113': '4'},
            "var_limp":{'tuberculosis': 'b_113 == "21"'}
        },
        "11_test_vejez": {
            "cols":"'b_16'",
            "colum_remp":{'b_16': '0'},
            "var_limp":{'edad': 'edad < 60'}
        },
        "12_test_0_8_años": {
            "cols":"'b_43','b_44','b_45','b_46'",
            "colum_remp":{'b_43': '0','b_44': '0','b_45': '0','b_46': '0'},
            "var_limp":{'edad': 'edad >= 8'}
        },
        "13_test_0_12_años": {
            "cols":"'b_40','b_63'",
            "colum_remp":{'b_40': '0','b_63': '1845-01-01'},
            "var_limp":{'edad': 'edad >= 13'}
        },
        "14_cardiovascular1": {
            "cols":"'b_92','b_95','b_98','b_107','b_72','b_106','b_111','b_118'",
            "colum_remp":{'b_92': '0','b_95': '0','b_98': '0','b_107': '0','b_72': '1845-01-01','b_106': '1845-01-01','b_111': '1845-01-01','b_118': '1845-01-01'},
            "var_limp":{'edad': 'edad < 30'}
            #"var_limp":{'edad1': 'edad > 30', 'edad': 'edad < 18'}
        },
        "15_cardiovascular2": {
            "cols":"'b_114','b_117'",
            "colum_remp":{'b_114': '0','b_117': '0'},
            "var_limp":{'edad': 'edad < 18'}
        },
        "16_odontologia": {
            "cols":"'b_76','b_102'",
            "colum_remp":{'b_76': '1845-01-01','b_102': '0'},
            "var_limp":{'edad': 'edad < 0.6'}
        },
        "17_gestacion": {# pediente ajuste fino borrar no gestantes
            "cols":"'b_14','b_23','b_35','b_59','b_60','b_61','b_33','b_56','b_58'",
            "colum_remp":{'b_14': '0','b_23': '0','b_35': '0','b_59': '0','b_60': '0','b_61': '0','b_33': '1845-01-01','b_56': '1845-01-01','b_58': '1845-01-01',},
            "var_limp":{'genero': 'A_SEX_10 == "M"','edad': 'edad < 10','edad2': 'edad > 59'}
        },
        "18_recien_nacido": {
            "cols":"'b_37','b_38','b_48','b_85','b_65','b_69','b_75','b_84'",
            "colum_remp":{'b_37': '0', 'b_38': '0', 'b_48': '0', 'b_85': '0', 'b_65': '1845-01-01', 'b_69': '1845-01-01', 'b_75': '1845-01-01', 'b_84': '1845-01-01'},
            "var_limp":{'tip_doc': 'A_TDOC_3 != "CN"'}
        },
        "19_primera_infancia1": {
            "cols":"'b_70'",
            "colum_remp":{'b_70': '0',},
            "var_limp":{'edad': 'edad < 0.6','edad2': 'edad > 2'}
        },
        "20_primera_infancia2": {
            "cols":"'b_71','b_77'",
            "colum_remp":{'b_71': '0','b_77': '0',},
            "var_limp":{'edad': 'edad < 2','edad2': 'edad > 5'}
        },
    
    },
    "validate_eps":{
        "nueva_eps": {
            "cols":"'b_19'",
            "colum_remp":{'b_19': '98'},
            "var_limp":{'edad': 'edad < 12'}
            },
        "aic": {
            "cols":"'b_19'",
            "colum_remp":{'b_19': '98'},
            "var_limp":{'edad': 'edad < 12'}
            },
    }
}
