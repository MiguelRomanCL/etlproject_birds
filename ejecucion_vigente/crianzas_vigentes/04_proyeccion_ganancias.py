"""
PROYECCIÓN DE GANANCIAS - Modelo 03
====================================

Script para proyectar ganancias de crianzas vigentes usando el Modelo 03 (30 días).

Entrada:
- C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_para_proyeccion.csv

Salida:
- Mismo CSV con columna adicional: ganancia_proyectada

Autor: Sistema de Modelación F35
Fecha: 2025-10-06

"""

import sys
import os

# Hack temporal para importar config desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src import config

import pandas as pd
import numpy as np
from pathlib import Path
from pycaret.regression import load_model, predict_model
import warnings

warnings.filterwarnings("ignore")

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_FILE = SCRIPT_DIR.parent / "work_data" / "resumen_crianzas_para_proyeccion.csv"
OUTPUT_FILE = SCRIPT_DIR.parent / "work_data" / "resumen_crianzas_con_proyeccion.csv"

# Ruta al modelo (ruta absoluta desde la ubicación del script)
MODELO_PATH = SCRIPT_DIR.parent.parent / "analisis" / "modelo03" / "modelo_limpio_final"

# Variables requeridas por el Modelo 03
VARIABLES_REQUERIDAS = [
    "mes_carga",
    "sexo",
    "kilos_recibidos_percapita",
    "tipoConstruccion",
    "densidad_pollos_m2",
]

# Mapeo de columnas del CSV a nombres esperados por el modelo
MAPEO_COLUMNAS = {"Sexo": "sexo"}

# Valores válidos
VALORES_VALIDOS = {
    "sexo": ["HEMBRA", "MACHO"],
    "tipoConstruccion": ["Tradicional", "Black Out", "Transversal"],
}

RANGOS_VALIDOS = {
    "mes_carga": (1, 12),
    "kilos_recibidos_percapita": (1.0, 6.0),
    "densidad_pollos_m2": (9.0, 50.0),
}

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================


def validar_archivo_existe(filepath):
    """Validar que el archivo de entrada exista"""
    if not filepath.exists():
        raise FileNotFoundError(
            f"❌ No se encontró el archivo de entrada:\n"
            f"   {filepath}\n"
            f"   Por favor, verifica que el archivo exista."
        )
    print(f"✓ Archivo encontrado: {filepath.name}")


def cargar_datos(filepath):
    """Cargar datos del CSV"""
    print(f"\n📂 Cargando datos desde: {filepath}")
    df = pd.read_csv(filepath)
    print(f"   ✓ Datos cargados: {len(df):,} registros")
    print(f"   ✓ Columnas: {len(df.columns)}")
    return df


def mapear_columnas(df, mapeo):
    """Mapear nombres de columnas al formato esperado"""
    print("\n🔄 Mapeando nombres de columnas...")
    df_mapeado = df.copy()

    columnas_mapeadas = []
    for col_original, col_nueva in mapeo.items():
        if col_original in df_mapeado.columns:
            df_mapeado.rename(columns={col_original: col_nueva}, inplace=True)
            columnas_mapeadas.append(f"{col_original} → {col_nueva}")

    if columnas_mapeadas:
        print(f"   ✓ Columnas mapeadas:")
        for mapeo_str in columnas_mapeadas:
            print(f"      • {mapeo_str}")
    else:
        print(f"   ℹ  No se requirió mapeo de columnas")

    return df_mapeado


def limpiar_datos_nulos(df, variables_requeridas):
    """Limpiar y reportar datos nulos en variables requeridas"""
    print("\n🧹 Limpiando datos nulos...")

    df_limpio = df.copy()
    registros_originales = len(df_limpio)

    # Identificar registros con nulos en variables requeridas
    nulos_por_columna = {}
    for var in variables_requeridas:
        if var in df_limpio.columns:
            nulos = df_limpio[var].isna().sum()
            if nulos > 0:
                nulos_por_columna[var] = nulos

    if nulos_por_columna:
        print(f"   ⚠️  Se encontraron valores nulos:")
        for var, count in nulos_por_columna.items():
            pct = count / registros_originales * 100
            print(f"      • {var}: {count:,} registros ({pct:.1f}%)")

        # Eliminar registros con nulos en variables requeridas
        for var in variables_requeridas:
            if var in df_limpio.columns:
                df_limpio = df_limpio[df_limpio[var].notna()]

        registros_eliminados = registros_originales - len(df_limpio)
        print(
            f"\n   🗑️  Registros eliminados: {registros_eliminados:,} ({registros_eliminados/registros_originales*100:.1f}%)"
        )
        print(
            f"   ✓ Registros válidos: {len(df_limpio):,} ({len(df_limpio)/registros_originales*100:.1f}%)"
        )
    else:
        print(f"   ✓ No se encontraron valores nulos")

    return df_limpio


def validar_columnas_requeridas(df, variables_requeridas):
    """Validar que estén todas las columnas necesarias"""
    print("\n🔍 Validando columnas requeridas...")

    columnas_presentes = df.columns.tolist()
    columnas_faltantes = [
        var for var in variables_requeridas if var not in columnas_presentes
    ]

    if columnas_faltantes:
        print(f"\n❌ ERROR: Faltan las siguientes columnas requeridas:")
        for col in columnas_faltantes:
            print(f"   • {col}")
        print(f"\n📋 Columnas presentes en el archivo:")
        for col in columnas_presentes:
            print(f"   • {col}")
        raise ValueError("Columnas requeridas faltantes")

    print(f"   ✓ Todas las columnas requeridas están presentes:")
    for var in variables_requeridas:
        print(f"      • {var}")

    return True


def validar_valores(df, valores_validos, rangos_validos):
    """Validar valores categóricos y rangos numéricos"""
    print("\n✅ Validando valores...")

    errores = []

    # Validar categóricas
    for var, valores in valores_validos.items():
        if var in df.columns:
            valores_unicos = df[var].unique()
            invalidos = set(valores_unicos) - set(valores)
            if invalidos:
                errores.append(
                    f"Valores inválidos en {var}: {invalidos}. Válidos: {valores}"
                )
                pass

    # Validar rangos
    for var, (min_val, max_val) in rangos_validos.items():
        if var in df.columns:
            if df[var].min() < min_val or df[var].max() > max_val:
                errores.append(
                    f"{var} fuera de rango [{min_val}, {max_val}]. "
                    f"Valores: {df[var].min():.2f}-{df[var].max():.2f}"
                )
                pass

    if errores:
        print(f"   ❌ Se encontraron errores de validación:")
        for error in errores:
            print(f"      • {error}")
        raise ValueError("Errores de validación encontrados")

    print(f"   ✓ Todos los valores son válidos")
    return True


def mostrar_estadisticas_input(df):
    """Mostrar estadísticas del dataset de entrada"""
    print("\n📊 Estadísticas del dataset:")
    print(f"   • Total de registros: {len(df):,}")
    print(f"   • Crianzas únicas: {df['nro_crianza'].nunique():,}")
    print(f"   • Pabellones únicos: {df['Pabellón'].nunique():,}")
    print(f"   • Sectores únicos: {df['nombre_sector'].nunique():,}")

    print(f"\n   📍 Distribución por sexo:")
    for sexo, count in df["sexo"].value_counts().items():
        pct = count / len(df) * 100
        print(f"      • {sexo}: {count:,} ({pct:.1f}%)")

    print(f"\n   🏗️  Distribución por tipo de construcción:")
    for tipo, count in df["tipoConstruccion"].value_counts().items():
        pct = count / len(df) * 100
        print(f"      • {tipo}: {count:,} ({pct:.1f}%)")

    print(f"\n   📈 Rango de alimento (kg/pollo):")
    print(f"      • Mínimo: {df['kilos_recibidos_percapita'].min():.2f} kg")
    print(f"      • Máximo: {df['kilos_recibidos_percapita'].max():.2f} kg")
    print(f"      • Promedio: {df['kilos_recibidos_percapita'].mean():.2f} kg")


def preparar_features(df):
    """Aplicar el mismo feature engineering que en entrenamiento"""
    df_features = df.copy()

    # Variables cíclicas para mes
    df_features["mes_sin"] = np.sin(2 * np.pi * df_features["mes_carga"] / 12)
    df_features["mes_cos"] = np.cos(2 * np.pi * df_features["mes_carga"] / 12)

    # Ratio alimento por densidad
    df_features["alimento_por_densidad"] = (
        df_features["kilos_recibidos_percapita"] / df_features["densidad_pollos_m2"]
    )

    # Categoría de densidad
    df_features["densidad_categoria"] = pd.cut(
        df_features["densidad_pollos_m2"],
        bins=[0, 13, 15, 20, 50],
        labels=["Baja", "Media", "Alta", "Muy_Alta"],
    )

    return df_features


def realizar_proyeccion(df, modelo):
    """Realizar la proyección usando el Modelo 03"""
    print("\n🤖 Realizando proyección con Modelo 03...")

    try:
        # Preparar features
        df_preparado = preparar_features(df)

        # Realizar predicción
        resultado = predict_model(modelo, data=df_preparado)

        # Extraer predicciones
        predicciones = resultado["prediction_label"].values

        print(f"   ✓ Proyección completada para {len(predicciones):,} registros")

        return predicciones

    except Exception as e:
        print(f"\n❌ Error durante la proyección:")
        print(f"   {str(e)}")
        raise


def agregar_columna_proyeccion(df, predicciones):
    """Agregar columna de ganancia proyectada al dataframe original"""
    print("\n📝 Agregando columna de proyección...")

    df_resultado = df.copy()
    df_resultado["ganancia_proyectada"] = predicciones

    print(f"   ✓ Columna 'ganancia_proyectada' agregada")

    return df_resultado


def mostrar_estadisticas_proyeccion(df):
    """Mostrar estadísticas de las proyecciones"""
    print("\n📊 Estadísticas de proyección:")

    ganancia_proy = df["ganancia_proyectada"]

    print(f"   • Ganancia promedio proyectada: {ganancia_proy.mean():.2f} gramos")
    print(f"   • Desviación estándar: {ganancia_proy.std():.2f} gramos")
    print(f"   • Mínimo: {ganancia_proy.min():.2f} gramos")
    print(f"   • Máximo: {ganancia_proy.max():.2f} gramos")
    print(f"   • Mediana: {ganancia_proy.median():.2f} gramos")

    print(f"\n   🐔 Ganancia proyectada por sexo:")
    for sexo in df["sexo"].unique():
        proy_sexo = df[df["sexo"] == sexo]["ganancia_proyectada"]
        print(f"      • {sexo}: {proy_sexo.mean():.2f} ± {proy_sexo.std():.2f} gramos")

    print(f"\n   🏗️  Ganancia proyectada por tipo de construcción:")
    for tipo in df["tipoConstruccion"].unique():
        proy_tipo = df[df["tipoConstruccion"] == tipo]["ganancia_proyectada"]
        print(f"      • {tipo}: {proy_tipo.mean():.2f} ± {proy_tipo.std():.2f} gramos")


def guardar_resultado(df, output_path):
    """Guardar el resultado con las proyecciones"""
    print(f"\n💾 Guardando resultado en: {output_path.name}")

    # Crear directorio si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar CSV
    df.to_csv(output_path, index=False)

    print(f"   ✓ Archivo guardado exitosamente")
    print(f"   📍 Ruta completa: {output_path}")


def mostrar_ejemplos(df, n=10):
    """Mostrar ejemplos de registros con proyección"""
    print(f"\n📋 Primeros {n} registros con proyección:")
    print("=" * 140)

    columnas_mostrar = [
        "nombre_sector",
        "nro_crianza",
        "Pabellón",
        "sexo",
        "kilos_recibidos_percapita",
        "tipoConstruccion",
        "densidad_pollos_m2",
        "ganancia_proyectada",
    ]

    df_ejemplos = df[columnas_mostrar].head(n)

    # Formatear para mejor visualización
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 140)
    pd.set_option("display.float_format", lambda x: f"{x:.2f}")

    print(df_ejemplos.to_string(index=False))
    print("=" * 140)


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================


def main():
    """Función principal del script"""

    print("=" * 80)
    print("🚀 PROYECCIÓN DE GANANCIAS - MODELO 03")
    print("=" * 80)
    print(f"\nModelo: Producción 03 (datos hasta día 30)")
    print(f"Fecha: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 1. Validar que existe el archivo de entrada
        validar_archivo_existe(INPUT_FILE)

        # 2. Cargar datos
        df = cargar_datos(INPUT_FILE)
        df = df[~df["nombre_sector"].isin(["DON WILSON", "EL CARMEN"])]

        # 3. Mapear columnas
        df = mapear_columnas(df, MAPEO_COLUMNAS)

        # 4. Validar columnas requeridas
        validar_columnas_requeridas(df, VARIABLES_REQUERIDAS)

        # 5. Limpiar datos nulos
        df = limpiar_datos_nulos(df, VARIABLES_REQUERIDAS)

        # 6. Validar valores

        # TODO: VALORES HARCODEADOS
        df["tipoConstruccion"] = np.where(
            df["tipoConstruccion"] == "Sin Información",
            "Black Out",
            df["tipoConstruccion"],
        )
        df["densidad_pollos_m2"] = np.where(
            df["densidad_pollos_m2"] < 0, config.DEFAULT_DENSITY, df["densidad_pollos_m2"]
        )

        validar_valores(df, VALORES_VALIDOS, RANGOS_VALIDOS)

        # 7. Mostrar estadísticas del input
        mostrar_estadisticas_input(df)

        # 8. Cargar modelo
        print(f"\n🤖 Cargando Modelo 03 (30 días de alimentación)...")
        modelo = load_model(str(MODELO_PATH))
        print(f"   ✓ Modelo cargado exitosamente")

        # 9. Realizar proyección
        predicciones = realizar_proyeccion(df, modelo)

        # 10. Agregar columna de proyección
        df_resultado = agregar_columna_proyeccion(df, predicciones)

        # 11. Mostrar estadísticas de proyección
        mostrar_estadisticas_proyeccion(df_resultado)

        # 12. Mostrar ejemplos
        mostrar_ejemplos(df_resultado, n=10)

        # 13. Guardar resultado
        guardar_resultado(df_resultado, OUTPUT_FILE)

        print("\n" + "=" * 80)
        print("✅ PROYECCIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 80)

        # Resumen final
        print(f"\n📊 Resumen:")
        print(f"   • Registros procesados: {len(df_resultado):,}")
        print(
            f"   • Ganancia promedio proyectada: {df_resultado['ganancia_proyectada'].mean():.2f}g"
        )
        print(f"   • Archivo de salida: {OUTPUT_FILE.name}")

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Error: Archivo no encontrado")
        print(f"   {str(e)}")
        return 1

    except ValueError as e:
        print(f"\n❌ Error de validación")
        print(f"   {str(e)}")
        return 1

    except Exception as e:
        print(f"\n❌ Error inesperado:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        import traceback

        print("\n📋 Traceback completo:")
        traceback.print_exc()
        return 1


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
