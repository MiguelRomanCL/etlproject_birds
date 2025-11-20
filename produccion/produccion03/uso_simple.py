"""
USO SIMPLE DEL PREDICTOR - MODELO 03
Script fácil de usar para predicciones rápidas
Modelo entrenado con 30 días de alimentación
"""

from predictor import PredictorGanancia
import pandas as pd

# ============================================================================
# INICIALIZAR PREDICTOR
# ============================================================================
print("🤖 Inicializando predictor (Modelo 03 - 30 días)...")
predictor = PredictorGanancia()

# ============================================================================
# OPCIÓN 1: PREDICCIÓN INDIVIDUAL
# ============================================================================
print("\n" + "="*70)
print("OPCIÓN 1: PREDICCIÓN DE UN CASO")
print("="*70)

# Define tus datos aquí
mi_caso = {
    'mes_carga': 6,                          # Mes del año (1-12)
    'sexo': 'MACHO',                         # 'MACHO' o 'HEMBRA'
    'kilos_recibidos_percapita': 3.5,        # Kilos hasta día 30
    'tipoConstruccion': 'Black Out',         # 'Tradicional', 'Black Out', o 'Transversal'
    'densidad_pollos_m2': 14.5               # Pollos por metro cuadrado
}

# Predecir
resultado = predictor.predecir(mi_caso)
ganancia = resultado['ganancia_predicha'].iloc[0]

print(f"\n🎯 GANANCIA PREDICHA: {ganancia:.2f} gramos")

# ============================================================================
# OPCIÓN 2: PREDICCIÓN MÚLTIPLE (VARIOS CASOS)
# ============================================================================
print("\n" + "="*70)
print("OPCIÓN 2: PREDICCIÓN DE MÚLTIPLES CASOS")
print("="*70)

# Define varios casos
casos = pd.DataFrame([
    {
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.5,
        'tipoConstruccion': 'Black Out',
        'densidad_pollos_m2': 14.5
    },
    {
        'mes_carga': 7,
        'sexo': 'HEMBRA',
        'kilos_recibidos_percapita': 3.2,
        'tipoConstruccion': 'Tradicional',
        'densidad_pollos_m2': 15.0
    },
    {
        'mes_carga': 8,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.8,
        'tipoConstruccion': 'Transversal',
        'densidad_pollos_m2': 13.5
    }
])

# Predecir todos
resultados = predictor.predecir(casos)

print("\n📊 Resultados:")
print(resultados[['sexo', 'tipoConstruccion', 'ganancia_predicha']].to_string(index=False))

# ============================================================================
# OPCIÓN 3: PREDICCIÓN DESDE ARCHIVO CSV
# ============================================================================
print("\n" + "="*70)
print("OPCIÓN 3: PREDICCIÓN DESDE ARCHIVO CSV")
print("="*70)

# Cargar y predecir desde CSV
# El CSV debe tener las columnas: mes_carga, sexo, kilos_recibidos_percapita, 
#                                  tipoConstruccion, densidad_pollos_m2

archivo_entrada = '../../work_data/resumen_crianzas_para_modelo2.csv'

print(f"\n📂 Procesando archivo: {archivo_entrada}")
print("   (Esto puede tomar unos segundos...)")

resultado_masivo = predictor.predecir_lote(archivo_entrada, guardar_resultado=True)

# Mostrar estadísticas
predictor.estadisticas_prediccion(resultado_masivo)

print("\n✅ ¡Proceso completado!")
print("   Revisa el archivo *_predicciones_modelo03.csv generado")
