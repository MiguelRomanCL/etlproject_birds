import sys
import os

# Hack temporal para importar config desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src import config

import pandas as pd
import numpy as np
import sqlalchemy
import unicodedata
import re


def uniformar_strings(input_str, remove_accents=True):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    s = ''.join(c for c in nfkd_form if not unicodedata.combining(c))
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()


def query_database(query, database):
    # __server = 'replica-it-eastus2-mysql-spga-prd-001.mysql.database.azure.com'
    __server = config.DB_HOST
    # __username = 'maestros'
    __username = config.DB_USER
    # __password = '8btU0JenEyKqajtc'
    __password = config.DB_PASSWORD
    __database = database
    __mysql_driver = 'mysql+pymysql'
    __connection_string = f'{__mysql_driver}://{__username}:{__password}@{__server}/{__database}'
    __engine_sqlalchemy = sqlalchemy.create_engine(__connection_string, connect_args={'ssl': {'ssl': True}})
    df_result = pd.read_sql(query, __engine_sqlalchemy)
    __engine_sqlalchemy.dispose()
    return df_result


df = pd.read_csv(r'..\work_data\resumen_crianzas_para_modelo.csv')
df_maestros_pabellones = query_database('SELECT * FROM maestrospabellones', 'ta_ags_pollos')
print(list(df_maestros_pabellones.columns))
df_maestros_pabellones['nombre_sector_code'] = df_maestros_pabellones['nombreSector'].apply(uniformar_strings)
df_maestros_pabellones = df_maestros_pabellones[['nombre_sector_code', 'numero', 'tipoConstruccion', 'areaUtil', 'sistemaVentilacion']]
df = pd.merge(df, df_maestros_pabellones, left_on=['nombre_sector_code', 'Pabellón'], right_on=['nombre_sector_code', 'numero'], how='left')
df['densidad_pollos_m2'] = df['Cantidad Total'] / df['areaUtil']

# filtros de sectores
# df = df[~df['nombre_sector_code'].isin(['santa ana', 'los tilos', 'casablanca', 'la fragua', 'las burras', 'las varas', 'los perales'])]
# df.drop(columns=['numero', 'areaUtil', 'sistemaVentilacion', 'Cantidad Total'], inplace=True)
df.drop(columns=['numero', 'areaUtil', 'sistemaVentilacion'], inplace=True)

df_maestros_sectores = query_database('SELECT nombre, zonaGeografica FROM maestrossectorescrianza', 'ta_ags_pollos')
df_maestros_sectores['nombre'] = df_maestros_sectores['nombre'].apply(uniformar_strings)

df = pd.merge(df, df_maestros_sectores, left_on='nombre_sector_code', right_on='nombre', how='left')
df = df[(df['edad_actual'] >= 32) & (df['edad_actual'] <= 41)]

df['tipoConstruccion'] = np.where(df['tipoConstruccion'].isna(), 'Black Out', df['tipoConstruccion'])

df_null = df[df['tipoConstruccion'].isnull()]

# df = df[['nombre_sector_code', 'nro_crianza', 'nro_pabellon', 'mes_carga', 'edad_madres_dias', 'peso_inicial_gramos', 'sexo', 'edad_promedio_faena_dias', 'edad_proyeccion_dias', 'kilos_recibidos_percapita', 'ganancia_promedio_gramos', 'tipoConstruccion', 'densidad_pollos_m2']]
df.to_excel(r'..\work_data\resumen_crianzas_para_proyeccion.xlsx', index=False)
df.to_csv(r'..\work_data\resumen_crianzas_para_proyeccion.csv', index=False)
