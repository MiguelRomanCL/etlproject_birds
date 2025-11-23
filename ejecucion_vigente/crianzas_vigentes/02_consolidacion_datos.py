import sys
import os

# Hack temporal para importar config desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src import config

import pandas as pd
import numpy as np
import unicodedata
import re


def uniformar_strings(input_str, remove_accents=True):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    s = ''.join(c for c in nfkd_form if not unicodedata.combining(c))
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()


EDAD_PROYECCION = config.PROJECTION_AGE_DAYS

# TODO: Aún no tengo una buena forma de calcular la edad actual por pabellón
df_resumen_crianzas = pd.read_pickle(r'..\data\resumen_crianzas.pkl')
df_resumen_crianzas['mes_carga'] = pd.to_datetime(df_resumen_crianzas['Fecha Guía Inicio']).dt.month
df_resumen_crianzas['anio_carga'] = pd.to_datetime(df_resumen_crianzas['Fecha Guía Inicio']).dt.year


df_resumen_crianzas['edad_actual'] = (pd.to_datetime('today') - pd.to_datetime(df_resumen_crianzas['Fecha Guía Fin'])).dt.days
df_resumen_crianzas['edad_proyeccion_dias'] = EDAD_PROYECCION


df_resumen_crianzas['edad_criterio_proyeccion'] = df_resumen_crianzas.groupby(['nombre_sector_code', 'nro_crianza'])['edad_actual'].transform('mean')
df_resumen_crianzas_bk = df_resumen_crianzas.copy()
df_resumen_crianzas = df_resumen_crianzas[df_resumen_crianzas['edad_criterio_proyeccion'] >= 32]

""" merge con guías de alimento """
df_resumen_alimento = pd.read_pickle(r'..\data\resumen_alimento.pkl')
df_resumen_alimento['Edad'] = np.ceil(df_resumen_alimento['Edad']).astype(int)
df_resumen_crianzas = pd.merge(df_resumen_crianzas, df_resumen_alimento, left_on=['nombre_sector_code', 'nro_crianza', 'edad_proyeccion_dias'], right_on=['nombre_sector_code', 'nro_crianza', 'Edad'], how='left')

df_resumen_crianzas.to_excel(r'..\work_data\resumen_crianzas_para_modelo.xlsx', index=False)
df_resumen_crianzas.to_csv(r'..\work_data\resumen_crianzas_para_modelo.csv', index=False)