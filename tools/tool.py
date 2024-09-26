import functools
import glob
import pandas as pd
import re
#import os


def scan_data(link):
    "Funcion para escanear todos los exceles de una carpeta"
    try:
        return pd.concat(map(functools.partial(pd.read_excel, header=0, index_col=False),glob.glob(f'{link}')))
    except:
        print(f"no se puede escanear {link}")
        pass


def limp_exa(exa, x, name):
    '''
        sirve para limpiar carros de linea saltos entre otros
    '''
    exa[x] = exa[x].astype(str).apply(lambda x: re.sub(r'[\n\r\t\v\f() :-]', '', x.lower())).apply(lambda x: re.sub(r'[áéíóú]', lambda m: {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}[m.group(0)], x))
    return exa #limp_exa(fnt.scan_data("1_data_new//3_exam//vih/*.xlsx"), "HCRDESCRIP")


def extract_values(row, regex_pattern):
    #print(row)
    print(regex_pattern)
    """
        extraer datos relevantes de los examenes de laboratorio
    """
    
    if row["Descripción"]:
        match = re.search(regex_pattern, row["Descripción"])
        #match = re.search(r"hemoglobina(.{04})", row["Descripción"])
        datas = []
        
        if match:
            datas.append(f'-{match.group(1)}-')
            #print(datas)
            return datas
        else:
            return row["Descripción"]
        


def scan():
    print("prueba exito")
    return "prueba exito"