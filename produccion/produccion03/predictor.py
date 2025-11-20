"""
PREDICTOR DE GANANCIA - PRODUCCIÓN 03
Sistema de predicción basado en Modelo03 (30 días de alimentación)

Variables requeridas:
- mes_carga
- sexo  
- kilos_recibidos_percapita (hasta 30 días)
- tipoConstruccion
- densidad_pollos_m2
"""

import pandas as pd
import numpy as np
from pycaret.regression import load_model, predict_model
import warnings
warnings.filterwarnings('ignore')

class PredictorGanancia:
    """
    Predictor de ganancia promedio de pollos usando Modelo03
    Modelo entrenado con datos de alimentación hasta 30 días
    """
    
    def __init__(self, modelo_path='../../analisis/modelo03/modelo_limpio_final'):
        """
        Inicializar el predictor
        
        Args:
            modelo_path: Ruta al modelo guardado (sin extensión .pkl)
        """
        print("🤖 Cargando Modelo 03 (30 días de alimentación)...")
        self.modelo = load_model(modelo_path)
        print("   ✓ Modelo cargado exitosamente")
        
        # Variables requeridas
        self.variables_requeridas = [
            'mes_carga',
            'sexo',
            'kilos_recibidos_percapita',
            'tipoConstruccion',
            'densidad_pollos_m2'
        ]
        
        # Valores válidos para categóricas
        self.valores_validos = {
            'sexo': ['HEMBRA', 'MACHO'],
            'tipoConstruccion': ['Tradicional', 'Black Out', 'Transversal']
        }
        
        # Rangos válidos para numéricas
        self.rangos_validos = {
            'mes_carga': (1, 12),
            'kilos_recibidos_percapita': (2.0, 5.0),
            'densidad_pollos_m2': (9.0, 50.0)
        }
    
    def validar_input(self, datos):
        """
        Validar que los datos de entrada sean correctos
        
        Args:
            datos: dict o DataFrame con los datos a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Convertir a DataFrame si es dict
        if isinstance(datos, dict):
            df = pd.DataFrame([datos])
        else:
            df = datos.copy()
        
        # Verificar variables requeridas
        for var in self.variables_requeridas:
            if var not in df.columns:
                return False, f"Falta la variable requerida: {var}"
        
        # Validar categóricas
        for var, valores in self.valores_validos.items():
            valores_unicos = df[var].unique()
            invalidos = set(valores_unicos) - set(valores)
            if invalidos:
                return False, f"Valores inválidos en {var}: {invalidos}. Valores válidos: {valores}"
        
        # Validar rangos numéricos
        for var, (min_val, max_val) in self.rangos_validos.items():
            if df[var].min() < min_val or df[var].max() > max_val:
                return False, f"{var} fuera de rango [{min_val}, {max_val}]. Valores: {df[var].min()}-{df[var].max()}"
        
        return True, "Validación exitosa"
    
    def preparar_features(self, datos):
        """
        Aplicar el mismo feature engineering que en entrenamiento
        
        Args:
            datos: DataFrame con las variables base
            
        Returns:
            DataFrame con features adicionales
        """
        df = datos.copy()
        
        # Variables cíclicas para mes
        df['mes_sin'] = np.sin(2 * np.pi * df['mes_carga'] / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['mes_carga'] / 12)
        
        # Ratio alimento por densidad
        df['alimento_por_densidad'] = df['kilos_recibidos_percapita'] / df['densidad_pollos_m2']
        
        # Categoría de densidad
        df['densidad_categoria'] = pd.cut(
            df['densidad_pollos_m2'],
            bins=[0, 13, 15, 20, 50],
            labels=['Baja', 'Media', 'Alta', 'Muy_Alta']
        )
        
        return df
    
    def predecir(self, datos, mostrar_detalles=True):
        """
        Realizar predicciones
        
        Args:
            datos: dict o DataFrame con los datos
            mostrar_detalles: Si mostrar información detallada
            
        Returns:
            DataFrame con predicciones
        """
        # Convertir a DataFrame si es necesario
        if isinstance(datos, dict):
            df = pd.DataFrame([datos])
        else:
            df = datos.copy()
        
        # Validar input
        es_valido, mensaje = self.validar_input(df)
        if not es_valido:
            raise ValueError(f"❌ Error de validación: {mensaje}")
        
        # Preparar features
        df_preparado = self.preparar_features(df)
        
        # Predecir
        if mostrar_detalles:
            print("\n📊 Realizando predicción...")
            print(f"   • Registros a predecir: {len(df)}")
        
        predicciones = predict_model(self.modelo, data=df_preparado)
        
        # Agregar columnas útiles
        df_resultado = df.copy()
        df_resultado['ganancia_predicha'] = predicciones['prediction_label'].values
        
        if mostrar_detalles:
            print(f"   ✓ Predicción completada")
            print(f"\n📈 Resumen de predicciones:")
            print(f"   • Ganancia promedio: {df_resultado['ganancia_predicha'].mean():.2f} gramos")
            print(f"   • Rango: {df_resultado['ganancia_predicha'].min():.2f} - {df_resultado['ganancia_predicha'].max():.2f} gramos")
        
        return df_resultado
    
    def predecir_lote(self, archivo_csv, guardar_resultado=True):
        """
        Predecir para un archivo CSV completo
        
        Args:
            archivo_csv: Ruta al archivo CSV
            guardar_resultado: Si guardar el resultado
            
        Returns:
            DataFrame con predicciones
        """
        print(f"\n📂 Cargando datos desde: {archivo_csv}")
        df = pd.read_csv(archivo_csv)
        
        # Verificar que tenga las columnas necesarias
        columnas_faltantes = set(self.variables_requeridas) - set(df.columns)
        if columnas_faltantes:
            raise ValueError(f"❌ Columnas faltantes en el CSV: {columnas_faltantes}")
        
        # Seleccionar solo las variables necesarias
        df_input = df[self.variables_requeridas].copy()
        
        print(f"   ✓ Datos cargados: {len(df_input)} registros")
        
        # Predecir
        resultado = self.predecir(df_input, mostrar_detalles=True)
        
        # Guardar si se solicita
        if guardar_resultado:
            archivo_salida = archivo_csv.replace('.csv', '_predicciones_modelo03.csv')
            resultado.to_csv(archivo_salida, index=False)
            print(f"\n💾 Resultado guardado en: {archivo_salida}")
        
        return resultado
    
    def estadisticas_prediccion(self, predicciones):
        """
        Mostrar estadísticas de las predicciones
        
        Args:
            predicciones: DataFrame con predicciones
        """
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS DE PREDICCIÓN")
        print("="*70)
        
        ganancia = predicciones['ganancia_predicha']
        
        print(f"\n📈 Ganancia Predicha:")
        print(f"   • Promedio: {ganancia.mean():.2f} gramos")
        print(f"   • Desviación: {ganancia.std():.2f} gramos")
        print(f"   • Mínimo: {ganancia.min():.2f} gramos")
        print(f"   • Máximo: {ganancia.max():.2f} gramos")
        print(f"   • Mediana: {ganancia.median():.2f} gramos")
        
        # Estadísticas por sexo
        if 'sexo' in predicciones.columns:
            print(f"\n🐔 Por Sexo:")
            for sexo in predicciones['sexo'].unique():
                ganancia_sexo = predicciones[predicciones['sexo'] == sexo]['ganancia_predicha']
                print(f"   • {sexo}: {ganancia_sexo.mean():.2f} ± {ganancia_sexo.std():.2f} gramos")
        
        # Estadísticas por tipo de construcción
        if 'tipoConstruccion' in predicciones.columns:
            print(f"\n🏗️  Por Tipo de Construcción:")
            for tipo in predicciones['tipoConstruccion'].unique():
                ganancia_tipo = predicciones[predicciones['tipoConstruccion'] == tipo]['ganancia_predicha']
                print(f"   • {tipo}: {ganancia_tipo.mean():.2f} ± {ganancia_tipo.std():.2f} gramos")
        
        print("\n" + "="*70)


def ejemplo_prediccion_simple():
    """Ejemplo 1: Predicción de un caso individual"""
    
    print("\n" + "="*70)
    print("EJEMPLO 1: PREDICCIÓN INDIVIDUAL")
    print("="*70)
    
    # Inicializar predictor
    predictor = PredictorGanancia()
    
    # Datos de ejemplo
    caso = {
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.5,
        'tipoConstruccion': 'Black Out',
        'densidad_pollos_m2': 14.5
    }
    
    print("\n📋 Caso a predecir:")
    for key, value in caso.items():
        print(f"   • {key}: {value}")
    
    # Predecir
    resultado = predictor.predecir(caso)
    
    print(f"\n🎯 PREDICCIÓN: {resultado['ganancia_predicha'].iloc[0]:.2f} gramos")
    

def ejemplo_comparacion_escenarios():
    """Ejemplo 2: Comparar diferentes escenarios"""
    
    print("\n" + "="*70)
    print("EJEMPLO 2: COMPARACIÓN DE ESCENARIOS")
    print("="*70)
    
    predictor = PredictorGanancia()
    
    # Escenarios a comparar
    escenarios = [
        {
            'nombre': 'Escenario Base',
            'mes_carga': 6,
            'sexo': 'MACHO',
            'kilos_recibidos_percapita': 3.2,
            'tipoConstruccion': 'Tradicional',
            'densidad_pollos_m2': 15.0
        },
        {
            'nombre': 'Escenario Mejorado',
            'mes_carga': 6,
            'sexo': 'MACHO',
            'kilos_recibidos_percapita': 3.5,
            'tipoConstruccion': 'Black Out',
            'densidad_pollos_m2': 14.0
        },
        {
            'nombre': 'Escenario Hembra',
            'mes_carga': 6,
            'sexo': 'HEMBRA',
            'kilos_recibidos_percapita': 3.2,
            'tipoConstruccion': 'Tradicional',
            'densidad_pollos_m2': 15.0
        }
    ]
    
    # Predecir todos
    resultados = []
    for escenario in escenarios:
        nombre = escenario.pop('nombre')
        prediccion = predictor.predecir(escenario, mostrar_detalles=False)
        ganancia = prediccion['ganancia_predicha'].iloc[0]
        resultados.append({
            'Escenario': nombre,
            'Ganancia Predicha': f"{ganancia:.2f}g",
            **escenario
        })
    
    # Mostrar comparación
    df_comparacion = pd.DataFrame(resultados)
    print("\n📊 Comparación de Escenarios:")
    print(df_comparacion.to_string(index=False))
    

def ejemplo_prediccion_masiva():
    """Ejemplo 3: Predicción sobre datos reales"""
    
    print("\n" + "="*70)
    print("EJEMPLO 3: PREDICCIÓN MASIVA - DATOS REALES")
    print("="*70)
    
    predictor = PredictorGanancia()
    
    # Cargar datos reales
    archivo_datos = '../../resumen_crianzas_para_modelo2.csv'
    
    # Predecir para todo el dataset
    resultado = predictor.predecir_lote(archivo_datos, guardar_resultado=True)
    
    # Mostrar estadísticas
    predictor.estadisticas_prediccion(resultado)
    
    return resultado


def ejemplo_validacion_modelo():
    """Ejemplo 4: Validar precisión del modelo con datos reales"""
    
    print("\n" + "="*70)
    print("EJEMPLO 4: VALIDACIÓN DEL MODELO")
    print("="*70)
    
    predictor = PredictorGanancia()
    
    # Cargar datos reales
    df = pd.read_csv('../../resumen_crianzas_para_modelo2.csv')
    
    # Tomar muestra aleatoria
    muestra = df.sample(n=100, random_state=42)
    
    # Preparar input (solo variables necesarias)
    X = muestra[predictor.variables_requeridas].copy()
    y_real = muestra['ganancia_promedio_gramos'].values
    
    # Predecir
    predicciones = predictor.predecir(X, mostrar_detalles=False)
    y_pred = predicciones['ganancia_predicha'].values
    
    # Calcular métricas
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(y_real, y_pred)
    rmse = np.sqrt(mean_squared_error(y_real, y_pred))
    r2 = r2_score(y_real, y_pred)
    
    print(f"\n📊 Validación en 100 casos aleatorios:")
    print(f"   • MAE: {mae:.4f} gramos")
    print(f"   • RMSE: {rmse:.4f} gramos")
    print(f"   • R²: {r2:.4f}")
    
    # Mostrar algunos ejemplos
    print(f"\n📋 Ejemplos de predicciones:")
    print(f"   {'Real':>10} {'Predicho':>10} {'Error':>10}")
    print(f"   {'-'*10} {'-'*10} {'-'*10}")
    for i in range(5):
        error = abs(y_real[i] - y_pred[i])
        print(f"   {y_real[i]:>10.2f} {y_pred[i]:>10.2f} {error:>10.2f}")


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    
    print("\n" + "🚀 "*35)
    print("SISTEMA DE PREDICCIÓN - MODELO 03 (30 DÍAS)")
    print("🚀 "*35)
    
    # Ejemplo 1: Predicción simple
    ejemplo_prediccion_simple()
    
    # Ejemplo 2: Comparación de escenarios
    ejemplo_comparacion_escenarios()
    
    # Ejemplo 3: Predicción masiva
    ejemplo_prediccion_masiva()
    
    # Ejemplo 4: Validación
    ejemplo_validacion_modelo()
    
    print("\n" + "="*70)
    print("✅ EJEMPLOS COMPLETADOS")
    print("="*70)
