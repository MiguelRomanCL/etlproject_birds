import pandas as pd
import os
import unicodedata
import re
from datetime import date, datetime, timedelta
import math


def uniformar_strings(input_str, remove_accents=True):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    s = ''.join(c for c in nfkd_form if not unicodedata.combining(c))
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()


df_proyecciones_ganancia = pd.read_csv(r'C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_con_proyeccion.csv')
FECHA_ACTUAL = date.today().strftime('%Y-%m-%d')

base_path = r'C:\repositorio_data\crianza_web_pollos_vigentes\info_general'
list_files = os.listdir(base_path)
list_files = [f for f in list_files if 'pabellones' in f]

lista_estaus_actual = []
for archivo in list_files:
    # print(archivo)
    nombre_sector = archivo.split('_')[2]
    nombre_sector_code = uniformar_strings(nombre_sector)
    nro_crianza = archivo.split('_')[3].split('.')[0]
    # df head is on row 2
    df = pd.read_excel(os.path.join(base_path, archivo), header=1)
    df = df[~df['T.Animal'].isna()]
    df['F.Partida'] = pd.to_datetime(df['F.Partida'], format='%d/%m/%y')
    df['nombre_sector'] = nombre_sector
    df['nombre_sector_code'] = nombre_sector_code
    df['nro_crianza'] = int(nro_crianza)
    lista_columnas = [str(c) for c in list(df.columns) if 'Unnamed' not in str(c)]
    lista_columnas = lista_columnas[1:]
    df = df[lista_columnas]
    lista_estaus_actual.append(df)

df_status_actual = pd.concat(lista_estaus_actual, ignore_index=True)
print(list(df_status_actual.columns))
df_status_actual.columns = ['Pab.', 'F.Partida', 'F.Término', 'T.Animal', 'Raza', 'Sexo', 'Fecha Fin Carga', 'Edad Inicio', 'Edad Proy.', 'Hembras', 'Machos', 'Mixto', 'Animales Ingres.', 'Detalle MORT NECR', 'Detalle', 'MORT', 'NECR', 'Stock', 'Estado', 'nombre_sector', 'nombre_sector_code', 'nro_crianza', 'Detalle MORT NECR SAL', 'SAL', 'Detalle.1', 'Detalle MORT NECR SAL AJU + AJU -', 'AJU +', 'AJU -', 'Detalle MORT']
df_status_actual = df_status_actual[(df_status_actual['Edad Proy.'] >= 32) & (df_status_actual['Edad Proy.'] <= 41)]

# ['Pab.', 'F.Partida', 'F.Término', 'T.Animal', 'Raza', 'Sexo', 'Fecha Fin Carga', 'Edad Inicio', 'Edad Proy.', 'Hembras', 'Machos', 'Mixto', 'Animales Ingres.', 'Detalle MORT NECR', 'Detalle', 'MORT', 'NECR', 'Stock', 'Estado', 'nombre_sector', 'nombre_sector_code', 'nro_crianza', 'Detalle MORT NECR SAL', 'SAL', 'Detalle.1', 'Detalle MORT NECR SAL AJU + AJU -', 'AJU +', 'AJU -', 'Detalle MORT']
# ['Pab.', 'F.Partida', 'F.Término', 'T.Animal', 'Raza', 'Sexo', 'Fecha\nFin Carga', 'Edad\nInicio', 'Edad\nProy.', 'Hembras', 'Machos', 'Mixto', 'Animales\nIngres.', 'Detalle', 'Detalle.1', 'mortalidad', 'necropsia', 'Stock', 'Estado', 'nombre_sector', 'nombre_sector_code', 'nro_crianza', 'Detalle\nMORT NECR', 'MORT', 'NECR', 'Detalle\nMORT', 'Detalle\nMORT NECR SAL', 'SAL']

lista_proyeccion_pabellones = []
for _, fila in df_status_actual.iterrows():
    nombre_sector = fila['nombre_sector']
    nombre_sector_code = fila['nombre_sector_code']
    nro_crianza = int(fila['nro_crianza'])
    nro_pabellon = int(fila['Pab.'])
    sexo_pabellon = fila['Sexo']

    # if nombre_sector_code in ['don gaston', 'la mina', 'los hornos', 'los naranjos', 'trompeta', 'las lomas norte', 'don wilson', 'los loros']:
    # if nombre_sector_code in ['compania', 'don wilson', 'las vegas']:
    if nombre_sector_code in ['alhue', 'don wilson', 'el carmen', 'la punta']:
        continue

    edad_actual = fila['Edad Proy.']

    edades_futuras = list(range(int(edad_actual) + 1, 51))
    fechas_futuras = [pd.to_datetime(FECHA_ACTUAL) + timedelta(days=i) for i in range(1, len(edades_futuras) + 1)]

    _ganancia_pabellon = df_proyecciones_ganancia[
        (df_proyecciones_ganancia['nombre_sector_code'] == nombre_sector_code) &
        (df_proyecciones_ganancia['nro_crianza'] == nro_crianza) &
        (df_proyecciones_ganancia['Pabellón'] == nro_pabellon)
        ]['ganancia_proyectada'].values[0]

    df_proyecciones_pabellon = pd.DataFrame({
        'fecha': fechas_futuras,
        'edad': edades_futuras,
        'cumplimiento_consumo': 0,
        'consumo_estandar_edad': 0,
        'proyeccion_consumo': 0
    })
    df_proyecciones_pabellon['proyeccion_peso'] = df_proyecciones_pabellon['edad'].apply(lambda edad: _ganancia_pabellon * edad)
    df_proyecciones_pabellon.insert(0, 'nombre_sector', nombre_sector)
    df_proyecciones_pabellon.insert(1, 'nombre_sector_code', nombre_sector_code)
    df_proyecciones_pabellon.insert(2, 'nro_crianza', nro_crianza)
    df_proyecciones_pabellon.insert(3, 'nro_pabellon', nro_pabellon)
    df_proyecciones_pabellon.insert(4, 'sexo', sexo_pabellon)

    lista_proyeccion_pabellones.append(df_proyecciones_pabellon)

df_proyecciones_general = pd.concat(lista_proyeccion_pabellones, ignore_index=True)

lista_proyecciones_con_silos = []
for _, fila in df_status_actual.iterrows():
    nombre_sector = fila['nombre_sector']
    nombre_sector_code = fila['nombre_sector_code']
    nro_crianza = int(fila['nro_crianza'])
    nro_pabellon = int(fila['Pab.'])
    sexo_pabellon = fila['Sexo']

    # check with os if the file C:\tecnoandina\f35\data\proyecciones_oficiales\proyecciones_ALHUE_167_sin_formatear.xlsx exists
    if os.path.exists(os.path.join(fr"C:\tecnoandina\f35\data\proyecciones_oficiales\proyecciones_{nombre_sector}_{nro_crianza}_sin_formatear.xlsx")):
        df_proyeccion_sector_silos = pd.read_excel(fr"C:\tecnoandina\f35\data\proyecciones_oficiales\proyecciones_{nombre_sector}_{nro_crianza}_sin_formatear.xlsx")
        df_proyeccion_pabellon_silos = df_proyeccion_sector_silos[df_proyeccion_sector_silos['nro_pabellon'] == nro_pabellon]
        if not df_proyeccion_pabellon_silos.empty:
            print('proyeccion de pabellón con silos existe: ', nombre_sector_code, nro_crianza, nro_pabellon)
            df_proyecciones_general = df_proyecciones_general[~((df_proyecciones_general['nombre_sector_code'] == nombre_sector_code) & (df_proyecciones_general['nro_crianza'] == nro_crianza) & (df_proyecciones_general['nro_pabellon'] == nro_pabellon))]

            df_proyeccion_silos_pabellon = pd.DataFrame({
                'fecha': df_proyeccion_pabellon_silos['fecha'],
                'edad': df_proyeccion_pabellon_silos['edad'],
                'cumplimiento_consumo': df_proyeccion_pabellon_silos['cumplimiento_consumo'],
                'consumo_estandar_edad': df_proyeccion_pabellon_silos['consumo_estandar_edad'],
                'proyeccion_consumo': df_proyeccion_pabellon_silos['proyeccion_consumo'],
                'proyeccion_peso': [p for p in df_proyeccion_pabellon_silos['proyeccion_peso']]
            })
            df_proyeccion_silos_pabellon.insert(0, 'nombre_sector', nombre_sector)
            df_proyeccion_silos_pabellon.insert(1, 'nombre_sector_code', nombre_sector_code)
            df_proyeccion_silos_pabellon.insert(2, 'nro_crianza', nro_crianza)
            df_proyeccion_silos_pabellon.insert(3, 'nro_pabellon', nro_pabellon)
            df_proyeccion_silos_pabellon.insert(4, 'sexo', sexo_pabellon)
            lista_proyecciones_con_silos.append(df_proyeccion_silos_pabellon)
df_proyecciones_con_silos = pd.concat(lista_proyecciones_con_silos, ignore_index=True)
df_proyecciones_con_silos['proyeccion_peso'] = df_proyecciones_con_silos['proyeccion_peso'] * 1000

df_final = pd.concat([df_proyecciones_general, df_proyecciones_con_silos], ignore_index=True)
df_final.to_excel(fr"proyeccion_pollos_expandido.xlsx", index=False)

lista_proyeciones_formateadas = []
for nombre_sector in df_final['nombre_sector_code'].unique():
    df_final_sector = df_final[df_final['nombre_sector_code'] == nombre_sector]
    for nro_crianza in df_final_sector['nro_crianza'].unique():
        df_final_sector_crianza = df_final_sector[df_final_sector['nro_crianza'] == nro_crianza]
        for nro_pabellon in sorted(df_final_sector_crianza['nro_pabellon'].unique()):
            print(nombre_sector, nro_crianza, nro_pabellon)
            df_final_sector_crianza_pabellon = df_final_sector_crianza[df_final_sector_crianza['nro_pabellon'] == nro_pabellon]

            _row_fechas = df_final_sector_crianza_pabellon['fecha']
            _row_edades = [df_final_sector_crianza_pabellon[df_final_sector_crianza_pabellon['fecha'] == f]['edad'] for f in _row_fechas]
            _row_consumo = [df_final_sector_crianza_pabellon[df_final_sector_crianza_pabellon['fecha'] == f]['proyeccion_consumo'] for f in _row_fechas]
            _row_peso = [df_final_sector_crianza_pabellon[df_final_sector_crianza_pabellon['fecha'] == f]['proyeccion_peso'] for f in _row_fechas]
            _row_peso = [r / 1000 for r in _row_peso]

            _df_formateado = pd.DataFrame()
            # headers of df_formateado is _row_fechas
            _df_formateado = pd.DataFrame(columns=[str(d.date()) for d in _row_fechas])
            _df_formateado.loc[0] = [int(e.values[0]) if not e.empty else None for e in _row_edades]
            _df_formateado.loc[1] = [float(c.values[0]) if not c.empty else None for c in _row_consumo]
            _df_formateado.loc[2] = [float(p.values[0]) if not p.empty else None for p in _row_peso]

            _df_formateado.insert(0, 'ratio', ['Edad', 'Consumo Alimento', 'Proyeccion Peso'])
            _df_formateado.insert(1, 'pabellon', nro_pabellon)
            _df_formateado.insert(2, 'etapa', 'Broiler')
            _df_formateado.insert(3, 'subzona', '')
            _df_formateado.insert(4, 'grupo', nombre_sector)

            lista_proyeciones_formateadas.append(_df_formateado)

    #         break
    #     break
    # break

_df_final_formateado = pd.concat(lista_proyeciones_formateadas, ignore_index=True)
_df_final_formateado.to_excel(fr"proyeccion_pollos_20251105.xlsx", index=False)
