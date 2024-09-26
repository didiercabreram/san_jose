from proces import conect
import config.settings as seting

def data_dow(fec_init, fec_final):

    # consulta datos basicos
    #conect.load_data(seting.datos_init(fec_init, fec_final)).to_excel("service/init/name/consulta.xlsx",  header=True, index=False, sheet_name="Sheet1")

    # consulta de eapb
    #conect.load_data(seting.eapb(fec_init, fec_final)).to_excel("service/init/eapb/consulta.xlsx",  header=True,  index=False,  sheet_name="Sheet1")

    # descarga de gestantes
    #conect.load_data(seting.gestante(fec_init, fec_final)).to_excel("service/init/gestante/consulta.xlsx",  header=True,  index=False,  sheet_name="Sheet1")

    #obtener resultado de laboratorios
    conect.load_data(seting.obtener_laborat(fec_init, fec_final)).to_excel("service/init/laboratorio/consulta.xlsx",  header=True,  index=False,  sheet_name="Sheet1")
