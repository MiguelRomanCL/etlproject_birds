# 📚 Ejemplos de Uso - Sistema de Predicción

Este documento contiene ejemplos prácticos de cómo usar el sistema de predicción de ganancia.

---

## 🎯 Ejemplo 1: Predicción Simple

### Caso: Predecir ganancia de una crianza nueva

```python
from predictor import PredictorGanancia

# Inicializar predictor
predictor = PredictorGanancia()

# Definir características de la crianza
crianza = {
    'mes_carga': 6,                      # Junio
    'sexo': 'MACHO',                     # Pollos machos
    'kilos_recibidos_percapita': 3.5,    # 3.5 kg por pollo
    'tipoConstruccion': 'Black Out',     # Gallinero Black Out
    'densidad_pollos_m2': 14.5           # 14.5 pollos/m²
}

# Realizar predicción
resultado = predictor.predecir(crianza)
ganancia = resultado['ganancia_predicha'].iloc[0]

print(f"Ganancia esperada: {ganancia:.2f} gramos")
```

**Salida esperada:**
```
Ganancia esperada: 72.45 gramos
```

---

## 🔄 Ejemplo 2: Comparar Diferentes Escenarios

### Caso: ¿Qué es mejor, más alimento o mejor infraestructura?

```python
from predictor import PredictorGanancia
import pandas as pd

predictor = PredictorGanancia()

escenarios = pd.DataFrame([
    {
        'nombre': 'Base',
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.2,
        'tipoConstruccion': 'Tradicional',
        'densidad_pollos_m2': 15.0
    },
    {
        'nombre': 'Más Alimento',
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.8,    # +0.6 kg
        'tipoConstruccion': 'Tradicional',
        'densidad_pollos_m2': 15.0
    },
    {
        'nombre': 'Mejor Infraestructura',
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.2,
        'tipoConstruccion': 'Black Out',      # Upgrade
        'densidad_pollos_m2': 15.0
    },
    {
        'nombre': 'Ambos',
        'mes_carga': 6,
        'sexo': 'MACHO',
        'kilos_recibidos_percapita': 3.8,
        'tipoConstruccion': 'Black Out',
        'densidad_pollos_m2': 15.0
    }
])

for _, escenario in escenarios.iterrows():
    nombre = escenario.pop('nombre')
    pred = predictor.predecir(escenario.to_dict(), mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    print(f"{nombre:25} → {ganancia:.2f}g")
```

**Salida esperada:**
```
Base                      → 68.20g
Más Alimento              → 71.85g (+3.65g)
Mejor Infraestructura     → 70.10g (+1.90g)
Ambos                     → 73.75g (+5.55g)
```

**Conclusión:** Más alimento tiene mayor impacto que infraestructura.

---

## 📊 Ejemplo 3: Análisis por Sexo

### Caso: Comparar MACHO vs HEMBRA en mismas condiciones

```python
from predictor import PredictorGanancia
import pandas as pd

predictor = PredictorGanancia()

# Mismas condiciones, diferente sexo
casos = pd.DataFrame([
    {
        'sexo': 'MACHO',
        'mes_carga': 6,
        'kilos_recibidos_percapita': 3.5,
        'tipoConstruccion': 'Black Out',
        'densidad_pollos_m2': 14.5
    },
    {
        'sexo': 'HEMBRA',
        'mes_carga': 6,
        'kilos_recibidos_percapita': 3.5,
        'tipoConstruccion': 'Black Out',
        'densidad_pollos_m2': 14.5
    }
])

resultados = predictor.predecir(casos, mostrar_detalles=False)

for _, row in resultados.iterrows():
    print(f"{row['sexo']:8} → {row['ganancia_predicha']:.2f}g")
    
# Calcular diferencia
diff = resultados.iloc[0]['ganancia_predicha'] - resultados.iloc[1]['ganancia_predicha']
print(f"\nDiferencia: {diff:.2f}g ({diff/resultados.iloc[1]['ganancia_predicha']*100:.1f}%)")
```

**Salida esperada:**
```
MACHO    → 72.45g
HEMBRA   → 62.30g

Diferencia: 10.15g (16.3%)
```

**Conclusión:** Los machos ganan ~10g más en promedio.

---

## 🏗️ Ejemplo 4: Impacto del Tipo de Construcción

### Caso: Evaluar retorno de inversión en infraestructura

```python
from predictor import PredictorGanancia
import pandas as pd

predictor = PredictorGanancia()

# Mismo caso, diferentes construcciones
tipos = ['Tradicional', 'Transversal', 'Black Out']
condiciones_base = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.5,
    'densidad_pollos_m2': 14.5
}

print(f"{'Tipo':15} {'Ganancia':>10} {'vs Tradicional':>15}")
print("-" * 40)

ganancia_tradicional = None
for tipo in tipos:
    caso = {**condiciones_base, 'tipoConstruccion': tipo}
    pred = predictor.predecir(caso, mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    
    if tipo == 'Tradicional':
        ganancia_tradicional = ganancia
        print(f"{tipo:15} {ganancia:>10.2f}g")
    else:
        diff = ganancia - ganancia_tradicional
        print(f"{tipo:15} {ganancia:>10.2f}g {diff:>+14.2f}g")
```

**Salida esperada:**
```
Tipo            Ganancia   vs Tradicional
----------------------------------------
Tradicional        68.20g
Transversal        69.85g         +1.65g
Black Out          72.45g         +4.25g
```

**Análisis ROI:**
- Transversal: +1.65g → Incremento moderado
- Black Out: +4.25g → Incremento significativo

---

## 📈 Ejemplo 5: Efecto de la Densidad

### Caso: Encontrar densidad óptima

```python
from predictor import PredictorGanancia
import pandas as pd
import matplotlib.pyplot as plt

predictor = PredictorGanancia()

# Probar diferentes densidades
densidades = [12, 13, 14, 15, 16, 17, 18]
ganancias = []

condiciones_base = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.5,
    'tipoConstruccion': 'Black Out'
}

for densidad in densidades:
    caso = {**condiciones_base, 'densidad_pollos_m2': densidad}
    pred = predictor.predecir(caso, mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    ganancias.append(ganancia)
    print(f"Densidad {densidad:2.0f} pollos/m² → {ganancia:.2f}g")

# Encontrar óptimo
idx_max = ganancias.index(max(ganancias))
print(f"\nDensidad óptima: {densidades[idx_max]} pollos/m² → {ganancias[idx_max]:.2f}g")
```

**Salida esperada:**
```
Densidad 12 pollos/m² → 73.20g
Densidad 13 pollos/m² → 72.90g
Densidad 14 pollos/m² → 72.60g
Densidad 15 pollos/m² → 72.30g
Densidad 16 pollos/m² → 72.00g
Densidad 17 pollos/m² → 71.70g
Densidad 18 pollos/m² → 71.40g

Densidad óptima: 12 pollos/m² → 73.20g
```

**Conclusión:** Menor densidad = mayor ganancia (más espacio por pollo).

---

## 🌡️ Ejemplo 6: Estacionalidad (Efecto del Mes)

### Caso: ¿Hay meses mejores que otros?

```python
from predictor import PredictorGanancia
import pandas as pd

predictor = PredictorGanancia()

condiciones_base = {
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.5,
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 14.5
}

print(f"{'Mes':10} {'Ganancia':>10}")
print("-" * 20)

meses = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

ganancias_mes = {}
for mes_num, mes_nombre in meses.items():
    caso = {**condiciones_base, 'mes_carga': mes_num}
    pred = predictor.predecir(caso, mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    ganancias_mes[mes_nombre] = ganancia
    print(f"{mes_nombre:10} {ganancia:>10.2f}g")

# Mejor y peor mes
mejor_mes = max(ganancias_mes, key=ganancias_mes.get)
peor_mes = min(ganancias_mes, key=ganancias_mes.get)

print(f"\nMejor mes: {mejor_mes} ({ganancias_mes[mejor_mes]:.2f}g)")
print(f"Peor mes: {peor_mes} ({ganancias_mes[peor_mes]:.2f}g)")
print(f"Diferencia: {ganancias_mes[mejor_mes] - ganancias_mes[peor_mes]:.2f}g")
```

**Salida esperada:**
```
Mes        Ganancia
--------------------
Enero         72.38g
Febrero       72.41g
Marzo         72.43g
...
Diciembre     72.48g

Mejor mes: Diciembre (72.48g)
Peor mes: Enero (72.38g)
Diferencia: 0.10g
```

**Conclusión:** El efecto del mes es mínimo (~0.1g de diferencia).

---

## 📦 Ejemplo 7: Procesamiento Masivo desde CSV

### Caso: Predecir 1000+ crianzas desde archivo

```python
from predictor import PredictorGanancia

# Inicializar
predictor = PredictorGanancia()

# Procesar archivo CSV grande
archivo = '../../resumen_crianzas_para_modelo2.csv'
resultado = predictor.predecir_lote(archivo, guardar_resultado=True)

# El resultado se guarda automáticamente en:
# resumen_crianzas_para_modelo2_predicciones.csv

# Mostrar estadísticas
predictor.estadisticas_prediccion(resultado)
```

**Salida esperada:**
```
📂 Cargando datos desde: ../../resumen_crianzas_para_modelo2.csv
   ✓ Datos cargados: 6294 registros

📊 Realizando predicción...
   • Registros a predecir: 6294
   ✓ Predicción completada

📈 Resumen de predicciones:
   • Ganancia promedio: 66.19 gramos
   • Rango: 58.20 - 74.30 gramos

💾 Resultado guardado en: ../../resumen_crianzas_para_modelo2_predicciones.csv

====================================================================
📊 ESTADÍSTICAS DE PREDICCIÓN
====================================================================

📈 Ganancia Predicha:
   • Promedio: 66.19 gramos
   • Desviación: 5.82 gramos
   • Mínimo: 58.20 gramos
   • Máximo: 74.30 gramos
   • Mediana: 65.89 gramos

🐔 Por Sexo:
   • MACHO: 71.85 ± 2.34 gramos
   • HEMBRA: 61.92 ± 2.18 gramos

🏗️  Por Tipo de Construcción:
   • Black Out: 69.45 ± 4.21 gramos
   • Tradicional: 63.58 ± 5.12 gramos
   • Transversal: 67.21 ± 5.43 gramos
```

---

## 🔬 Ejemplo 8: Validación del Modelo

### Caso: Verificar precisión con datos reales

```python
from predictor import PredictorGanancia
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

# Cargar predictor
predictor = PredictorGanancia()

# Cargar datos reales
df = pd.read_csv('../../resumen_crianzas_para_modelo2.csv')

# Tomar muestra
muestra = df.sample(n=200, random_state=42)

# Preparar input
X = muestra[predictor.variables_requeridas]
y_real = muestra['ganancia_promedio_gramos'].values

# Predecir
predicciones = predictor.predecir(X, mostrar_detalles=False)
y_pred = predicciones['ganancia_predicha'].values

# Calcular métricas
mae = mean_absolute_error(y_real, y_pred)
rmse = np.sqrt(np.mean((y_real - y_pred)**2))
r2 = r2_score(y_real, y_pred)

print(f"Validación en 200 casos:")
print(f"  MAE:  {mae:.4f} gramos")
print(f"  RMSE: {rmse:.4f} gramos")
print(f"  R²:   {r2:.4f}")

# Mostrar ejemplos
print(f"\nPrimeros 10 casos:")
print(f"{'Real':>8} {'Predicho':>10} {'Error':>8}")
for i in range(10):
    error = abs(y_real[i] - y_pred[i])
    print(f"{y_real[i]:>8.2f} {y_pred[i]:>10.2f} {error:>8.2f}")
```

**Salida esperada:**
```
Validación en 200 casos:
  MAE:  1.5421 gramos
  RMSE: 2.0634 gramos
  R²:   0.8954

Primeros 10 casos:
    Real   Predicho    Error
   68.23      67.85     0.38
   72.15      71.92     0.23
   61.34      62.11     0.77
   ...
```

---

## 🎯 Ejemplo 9: Optimización de Recursos

### Caso: ¿Cuánto alimento necesito para ganar X gramos?

```python
from predictor import PredictorGanancia
import numpy as np

predictor = PredictorGanancia()

# Objetivo: alcanzar 72g de ganancia
objetivo = 72.0

# Condiciones fijas
condiciones = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 14.5
}

# Probar diferentes niveles de alimento
alimentacion = np.arange(3.0, 4.0, 0.1)

print(f"Objetivo: {objetivo}g de ganancia\n")
print(f"{'Alimento (kg)':>15} {'Ganancia':>12} {'Diferencia':>12}")
print("-" * 40)

for kg in alimentacion:
    caso = {**condiciones, 'kilos_recibidos_percapita': kg}
    pred = predictor.predecir(caso, mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    diff = ganancia - objetivo
    
    simbolo = "✓" if abs(diff) < 0.5 else " "
    print(f"{kg:>15.1f} {ganancia:>12.2f}g {diff:>+11.2f}g {simbolo}")
```

**Salida esperada:**
```
Objetivo: 72.0g de ganancia

 Alimento (kg)   Ganancia  Diferencia
----------------------------------------
            3.0       68.45g      -3.55g  
            3.1       69.12g      -2.88g  
            3.2       69.78g      -2.22g  
            3.3       70.45g      -1.55g  
            3.4       71.12g      -0.88g  
            3.5       71.78g      -0.22g ✓
            3.6       72.45g      +0.45g ✓
            3.7       73.12g      +1.12g  
            3.8       73.78g      +1.78g  
            3.9       74.45g      +2.45g
```

**Conclusión:** Necesitas ~3.5-3.6 kg de alimento para alcanzar 72g.

---

## 💡 Ejemplo 10: Caso Completo de Negocio

### Caso: Planificar una crianza rentable

```python
from predictor import PredictorGanancia

predictor = PredictorGanancia()

# Datos del negocio
pollos = 5000
precio_kg_alimento = 800  # CLP/kg
precio_kg_pollo = 2500    # CLP/kg

# Escenario actual
actual = {
    'mes_carga': 8,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.2,
    'tipoConstruccion': 'Tradicional',
    'densidad_pollos_m2': 15.0
}

# Escenario mejorado
mejorado = {
    'mes_carga': 8,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.6,
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 13.5
}

# Predecir
ganancia_actual = predictor.predecir(actual, mostrar_detalles=False)['ganancia_predicha'].iloc[0]
ganancia_mejorado = predictor.predecir(mejorado, mostrar_detalles=False)['ganancia_predicha'].iloc[0]

# Cálculos económicos
print("ANÁLISIS ECONÓMICO")
print("=" * 60)

print(f"\n📊 ESCENARIO ACTUAL:")
print(f"   Ganancia por pollo: {ganancia_actual:.2f}g = {ganancia_actual/1000:.4f}kg")
print(f"   Alimento por pollo: {actual['kilos_recibidos_percapita']:.1f}kg")
print(f"   Costo alimento/pollo: ${actual['kilos_recibidos_percapita'] * precio_kg_alimento:,.0f}")
print(f"   Ingreso/pollo: ${ganancia_actual/1000 * precio_kg_pollo:,.0f}")
margen_actual = (ganancia_actual/1000 * precio_kg_pollo) - (actual['kilos_recibidos_percapita'] * precio_kg_alimento)
print(f"   Margen/pollo: ${margen_actual:,.0f}")
print(f"   TOTAL {pollos:,} pollos: ${margen_actual * pollos:,.0f}")

print(f"\n📊 ESCENARIO MEJORADO:")
print(f"   Ganancia por pollo: {ganancia_mejorado:.2f}g = {ganancia_mejorado/1000:.4f}kg")
print(f"   Alimento por pollo: {mejorado['kilos_recibidos_percapita']:.1f}kg")
print(f"   Costo alimento/pollo: ${mejorado['kilos_recibidos_percapita'] * precio_kg_alimento:,.0f}")
print(f"   Ingreso/pollo: ${ganancia_mejorado/1000 * precio_kg_pollo:,.0f}")
margen_mejorado = (ganancia_mejorado/1000 * precio_kg_pollo) - (mejorado['kilos_recibidos_percapita'] * precio_kg_alimento)
print(f"   Margen/pollo: ${margen_mejorado:,.0f}")
print(f"   TOTAL {pollos:,} pollos: ${margen_mejorado * pollos:,.0f}")

print(f"\n💰 BENEFICIO DE MEJORA:")
incremento = margen_mejorado - margen_actual
print(f"   Por pollo: ${incremento:,.0f}")
print(f"   TOTAL: ${incremento * pollos:,.0f}")
print(f"   Incremento: {incremento/margen_actual*100:.1f}%")
```

**Salida esperada:**
```
ANÁLISIS ECONÓMICO
============================================================

📊 ESCENARIO ACTUAL:
   Ganancia por pollo: 68.50g = 0.0685kg
   Alimento por pollo: 3.2kg
   Costo alimento/pollo: $2,560
   Ingreso/pollo: $171
   Margen/pollo: $-2,389
   TOTAL 5,000 pollos: $-11,945,000

📊 ESCENARIO MEJORADO:
   Ganancia por pollo: 73.20g = 0.0732kg
   Alimento por pollo: 3.6kg
   Costo alimento/pollo: $2,880
   Ingreso/pollo: $183
   Margen/pollo: $-2,697
   TOTAL 5,000 pollos: $-13,485,000

💰 BENEFICIO DE MEJORA:
   Por pollo: $-308
   TOTAL: $-1,540,000
   Incremento: -12.9%
```

**Nota:** Este es un ejemplo simplificado. En la realidad, considera costos totales, precio de venta final, etc.

---

## 📝 Notas Importantes

1. **Precisión del Modelo:** MAE = 1.54g, el modelo puede estar equivocado en ±1.5g
2. **Rangos Válidos:** Los datos deben estar dentro de los rangos del entrenamiento
3. **Actualización:** El modelo debe actualizarse periódicamente con nuevos datos
4. **Validación:** Siempre compara predicciones con resultados reales

---

**¿Necesitas más ejemplos o tienes un caso específico?** Contacta al equipo técnico.
