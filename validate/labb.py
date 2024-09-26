import tools.tool as tol
from config import settings

microservices = settings.config.get("exams_scan")

def eject():
    print("--"*30)
    "escaneamos el documentos que tiene los examenes "
    agrega = tol.scan_data(f"service/init/laboratorio/*.xlsx")#[columns].drop_duplicates().astype(str)

    "Limpia la columna donde estan los valores de los examenes "
    dat = tol.limp_exa(agrega, "Descripción", "otra cosa")

    ""
    #values = dat.assign(HCRDESCRIP=dat.apply(tol.extract_values, args=(file_path,), axis=1))
    #for exam, file_path in microservices.items():
        #print(exam)
        #print(file_path)
    #print(dat['tipo_exam'])
    print("--"*30)



    # Definir los patrones correspondientes para cada tipo de examen
    patterns = {
        "HEMOGRAMA": r"hemoglobina(.{04})",
        "CREATININA": r"creatininaensuero(\d+\.\d+)",
        "COLESTEROL_LDL": r"colesterolldl(\d+\.\d+)",
        "Virus_Inmunodeficiencia": r"virusdeinmunodeficienciahumana1y2anticuerposvihsida(\d+\.\d+)",
        "TRIGLICERIDOS": r"trigtrigliceridostrigliceridos(\d+\.\d+)",
        "HEPATITIS_B": r"antigenodesuperficiehepatitisbantigenodesuperficiehepatitisb(\d+\.\d+)",
        "Hepatitis_C": r"hvchvchepatitischvchepatitisc(\d+\.\d+)"
    }

    # Función para aplicar el patrón adecuado basado en el tipo de examen
    def apply_extractor(row, patterns):
        tipo_exam = row["tipo_exam"]
        
        # Verificar si el tipo de examen tiene un patrón definido
        if tipo_exam in patterns:
            pattern = patterns[tipo_exam]
            # Aplicar la función de extracción tol.extract_values usando el patrón adecuado
            return tol.extract_values(row, pattern)
        
        return None  # Si no coincide con ninguno, devolver None o el valor que prefieras

    # Aplicar la función a cada fila del DataFrame y crear una nueva columna 'dat_new'
    values = dat.assign(dat_new=dat.apply(apply_extractor, args=(patterns,), axis=1))
    #values = dat.assign(dat_new=dat.apply(tol.extract_values, args=(patterns,), axis=1))
    #print(values)
    values.to_excel(f"consulta.xlsx", header=True, index=False, sheet_name="Sheet1")

    # Filtrar los datos si es necesario (opcional)
    hemogramas = dat[dat["tipo_exam"] == "Virus_Inmunodeficiencia"]
    print(hemogramas)
    #hemogramas2 = dat[dat["tipo_exam"] == "CREATININA"]







        #file_path2 = r"hemoglobina(.{04})"
            #return row["b_103"]
    #elif dat["tipo_exam"].astype(str) != "HEMOGRAMA":
    #    pass


    #values = dat.assign(dat_new=dat.apply(tol.extract_values, args=(file_path2,), axis=1))
        #values = dat.assign(dat_new=dat.apply(tol.extract_values, args=(file_path,), axis=1))
    #print(values['dat_new'])
        #print(values['tipo_exam'])
    #print(dat[['tipo_exam','Descripción']])
    #print(dat)
    #print(microservices)
    print("--"*30)
    #tol.scan
