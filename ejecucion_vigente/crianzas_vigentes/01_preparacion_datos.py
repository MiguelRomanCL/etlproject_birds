from pkg_sap_agrosuper import resumen_documentos
import pandas as pd
import unicodedata
import re
from tqdm import tqdm
import os


def uniformar_strings(input_str, remove_accents=True):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    s = ''.join(c for c in nfkd_form if not unicodedata.combining(c))
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()


def split_filename(categoria_param, filename_param):
    if categoria_param == 'cargado_pabellones':
        return {'nombre_sector': filename_param.split('_')[1], 'nro_crianza': int(filename_param.split('_')[2].split('.')[0])}
    elif categoria_param == 'guias_alimento':
        return {'nombre_sector': filename_param.split('_')[2], 'nro_crianza': int(filename_param.split('_')[3].split('.')[0])}
    elif categoria_param == 'cierre_final':
        return {'nombre_sector': filename_param.split('_')[2], 'nro_crianza': int(filename_param.split('_')[3].split('.')[0])}
    elif categoria_param == 'salidas_faena':
        return {'nombre_sector': filename_param.split('_')[1], 'nro_crianza': int(filename_param.split('_')[2].split('.')[0])}
    elif categoria_param == 'mortalidad':
        return {'nombre_sector': filename_param.split('_')[1], 'nro_crianza': int(filename_param.split('_')[2].split('.')[0])}
    else:
        raise ValueError(f"Categoria {categoria_param} no reconocida")


REGENERAR_DATOS = True
base_path = r'C:\repositorio_data\crianza_web_pollos_vigentes'

if REGENERAR_DATOS:

    lista_resumenes_crianza = []
    lista_cargado_alimento = []

    files_cargado_pabellones = os.listdir(fr"{base_path}\cargado_pabellones")
    for archivo_cargado in files_cargado_pabellones:
        nombre_sector = split_filename('cargado_pabellones', archivo_cargado)['nombre_sector']

        nro_crianza = split_filename('cargado_pabellones', archivo_cargado)['nro_crianza']

        try:
            df_guias_alimento_check = pd.read_html(fr"{base_path}\guias_alimento\guias_alimento_{nombre_sector}_{nro_crianza}.xls", skiprows=2, header=0, thousands='.')[0]
        except Exception as e:
            print(f"Archivo de guias de alimento para {nombre_sector} crianza {nro_crianza} no encontrado, se omite.")
            continue

        df_cargado_pabellones_sector_crianza = pd.read_excel(fr"{base_path}\cargado_pabellones\{archivo_cargado}", skiprows=6)
        if df_cargado_pabellones_sector_crianza.empty:
            print(f"Archivo de cargado para {nombre_sector} crianza {nro_crianza} está vacío, se omite.")
            continue
        df_file_encabezado = pd.read_excel(fr"{base_path}\cargado_pabellones\{archivo_cargado}", nrows=5, usecols="A:B")
        if len(list(df_cargado_pabellones_sector_crianza.columns)) == 12:
            df_cargado_pabellones_sector_crianza['nombre_sector'] = nombre_sector
            df_cargado_pabellones_sector_crianza['nro_crianza'] = nro_crianza
            df_cargado_pabellones_sector_crianza['Fecha Guía'] = pd.to_datetime(df_cargado_pabellones_sector_crianza['Fecha Guía'], format='%Y-%m-%d', errors='coerce')
        else:
            raise ValueError(f"...... Archivo {archivo_cargado} con problemas .........")
        df_cargado_pabellones_sector_crianza_resumen = resumen_documentos.resumen_carga_pabellones_pollos(df_cargado_pabellones_sector_crianza)
        df_cargado_pabellones_sector_crianza_resumen['nombre_sector_code'] = df_cargado_pabellones_sector_crianza_resumen['nombre_sector'].apply(uniformar_strings)
        df_cargado_pabellones_sector_crianza_resumen = df_cargado_pabellones_sector_crianza_resumen[['nombre_sector', 'nombre_sector_code', 'nro_crianza', 'Pabellón', 'Cantidad Total', 'Fecha Guía Inicio', 'Fecha Guía Fin', 'Peso Promedio', 'Sexo']]

        lista_resumenes_crianza.append(df_cargado_pabellones_sector_crianza_resumen)

        cantidad_animales_inicial_sector_crianza = df_cargado_pabellones_sector_crianza_resumen['Cantidad Total'].sum()
        try:
            df_mortalidad_sector_crianza = pd.read_html(fr"{base_path}\mortalidad\mortalidad_{nombre_sector}_{nro_crianza}.xls", thousands='.', decimal=',')[0]
        except Exception as e:
            print(f"Archivo de mortalidad para {nombre_sector} crianza {nro_crianza} no encontrado, se omite.")
            continue
        if df_mortalidad_sector_crianza.empty:
            print(f"Archivo de mortalidad para {nombre_sector} crianza {nro_crianza} está vacío, se omite.")
            continue
        df_mortalidad_sector_crianza = df_mortalidad_sector_crianza.iloc[:-1].iloc[:-1]
        df_mortalidad_sector_crianza['Fecha Movimiento'] = pd.to_datetime(df_mortalidad_sector_crianza['Fecha Movimiento'], format='%d/%m/%y')
        df_mortalidad_sector_crianza['nombre_sector'] = nombre_sector
        df_mortalidad_sector_crianza['nombre_sector_code'] = df_mortalidad_sector_crianza['nombre_sector'].apply(uniformar_strings)
        df_mortalidad_sector_crianza['nro_crianza'] = nro_crianza
        df_mortalidad_sector_crianza['Fecha Movimiento'] = pd.to_datetime(df_mortalidad_sector_crianza['Fecha Movimiento'], format='%Y-%m-%d', errors='coerce')
        df_mortalidad_sector_crianza_grouped = df_mortalidad_sector_crianza.groupby(['nombre_sector_code', 'nro_crianza', 'Fecha Movimiento'], as_index=False).agg({'Cantidad': 'sum', 'Edad': 'mean'}).rename(columns={'Cantidad': 'Mortalidad Total'})
        df_mortalidad_sector_crianza_grouped['stock_animales'] = cantidad_animales_inicial_sector_crianza - df_mortalidad_sector_crianza_grouped['Mortalidad Total'].cumsum()

        df_guias_alimento_sector_crianza = pd.read_html(fr"{base_path}\guias_alimento\guias_alimento_{nombre_sector}_{nro_crianza}.xls", skiprows=2, header=0, thousands='.')[0]
        df_guias_alimento_sector_crianza['nombre_sector'] = nombre_sector
        df_guias_alimento_sector_crianza['nombre_sector_code'] = df_guias_alimento_sector_crianza['nombre_sector'].apply(uniformar_strings)
        df_guias_alimento_sector_crianza['nro_crianza'] = nro_crianza
        df_guias_alimento_sector_crianza['F.Guía'] = pd.to_datetime(df_guias_alimento_sector_crianza['F.Guía'], format='%d/%m/%Y', errors='coerce')
        df_guias_alimento_sector_crianza_grouped = df_guias_alimento_sector_crianza.groupby(['nombre_sector_code', 'nro_crianza', 'F.Guía'], as_index=False).agg({'Kilos': 'sum'})

        alimento_inicial_sector_crianza = df_guias_alimento_sector_crianza_grouped[df_guias_alimento_sector_crianza_grouped['F.Guía'] < df_mortalidad_sector_crianza_grouped['Fecha Movimiento'].min()]['Kilos'].sum()

        df_cargas_alimento = pd.merge(df_mortalidad_sector_crianza_grouped, df_guias_alimento_sector_crianza_grouped[['nombre_sector_code', 'nro_crianza', 'F.Guía', 'Kilos']], left_on=['nombre_sector_code', 'nro_crianza', 'Fecha Movimiento'], right_on=['nombre_sector_code', 'nro_crianza', 'F.Guía'], how='left')
        df_cargas_alimento['Kilos'] = df_cargas_alimento['Kilos'].fillna(0)
        if not df_cargas_alimento.empty:
            df_cargas_alimento.loc[df_cargas_alimento.index[0], 'Kilos'] = df_cargas_alimento.loc[df_cargas_alimento.index[0], 'Kilos'] + alimento_inicial_sector_crianza
            df_cargas_alimento['Kilos'] = df_cargas_alimento['Kilos'].fillna(0)
            df_cargas_alimento['kilos_recibidos'] = df_cargas_alimento['Kilos'].cumsum()
        df_cargas_alimento['kilos_recibidos_percapita'] = df_cargas_alimento['kilos_recibidos'] / df_cargas_alimento['stock_animales']
        df_cargas_alimento = df_cargas_alimento[['nombre_sector_code', 'nro_crianza', 'Edad', 'kilos_recibidos_percapita']]

        lista_cargado_alimento.append(df_cargas_alimento)

    df_resumen_crianzas = pd.concat(lista_resumenes_crianza, ignore_index=True)
    df_resumen_crianzas.to_pickle(r'..\data\resumen_crianzas.pkl')
    df_resumen_alimento = pd.concat(lista_cargado_alimento, ignore_index=True)
    df_resumen_alimento.to_pickle(r'..\data\resumen_alimento.pkl')
