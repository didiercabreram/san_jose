"""
import data_server
import os

from config.settings import config
carpetas = config.get("carpetas")
examens = config.get("exams")

meds = tuple(config.get("meds"))
gestantes = tuple(config.get("gestantes"))
aborto = tuple(config.get("aborto"))
parto = tuple(config.get("parto"))
nueva_eps = tuple(config.get("nueva_eps"))

init_ = "2024-07-01"
fin_ = "2024-08-01"

def crear_carpetas(carpetas):
    for carpeta, subcarpetas in carpetas.items():
        # Verificar si la carpeta principal existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear subcarpetas dentro de la carpeta principal
        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(carpeta, subcarpeta)
            if not os.path.exists(subcarpeta_path):
                os.makedirs(subcarpeta_path)
            else:
                print(f"La carpeta {subcarpeta_path} ya existe.")

def examns():
    "Funcion para descargar todos los examenes"
    for exam, file_path in examens.items():
        print(file_path)
        data_server.eject_exam(init_, fin_, exam, file_path)

def initt():
    
    crear_carpetas(config.get("carpetas"))# crear todas las carpetas
    data_server.eject_name(init_, fin_)
    
    data_server.eject_peso(init_, fin_)
    data_server.eject_proced(init_, fin_)
    data_server.eject_medic(init_, fin_, meds)
    data_server.eject_fpp(init_, fin_)
    data_server.eject_riesgo_ges(init_, fin_)
    
    data_server.eject_recien_nacido(init_, fin_)
    data_server.eject_recien_nacido2(init_, fin_)
    data_server.eject_recien_nacido_2023(init_, fin_)
   
    data_server.eject_colposcopia(init_, fin_)
    data_server.eject_gestantes(init_, fin_, gestantes, "Gestantes")# gestantes
    data_server.eject_gestantes(init_, fin_, aborto, "aborto")# gestantes
    data_server.eject_gestantes(init_, fin_, parto, "parto")# gestantescls
    #data_server.eject_gestantes(init_, fin_, nueva_eps, "nueva_eps")# data_eps
    data_server.eject_visual(init_, fin_)
    
    data_server.eject_salida_materna(init_, fin_)
    examns()# descargar todos los examenes
    
"""

#
#print(config.get("carpetas").get('1_data_new'))
#print(config.get("carpetas").get("1_data_new", []).get(1))
#values = config.get("carpetas").get('1_data_new')
#carp = config.get("carpetas")

#fourth_value = list(config.get("carpetas").get('1_data_new'))[3]  # Selecciona el cuarto elemento de la lista
