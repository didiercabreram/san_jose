import download.service as dow
import validate.app as valid

fec_init = '2024-08-08'
fec_final = '2024-08-09'

#valid.app_run



# funcion para descargar todos los datso de la plataforma
#dow.data_dow(fec_init, fec_final)

valid.app_run()

#carpetas = config.get("carpetas")
#examens = config.get("exams")

#querygest = seting.gestante(fec_init, fec_final)
#df = conect.load_data(querygest)

#file_name = f"consulta.xlsx"
#df.to_excel(file_name, header=True, index=False, sheet_name="Sheet1")