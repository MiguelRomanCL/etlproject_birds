# 🚀 Sistema de Predicción - Producción 03

Sistema de producción para predecir ganancia promedio de pollos usando **Modelo 03** (datos de alimentación hasta 30 días).

---

## 📊 Características del Modelo

**Modelo:** ExtraTreesRegressor  
**Datos de entrenamiento:** Alimentación hasta día 30 (vs 32 días del Modelo 02)

**Performance:**
- MAE: 1.55 gramos
- R²: 0.895 (89.5% de varianza explicada)
- MAPE: 2.36%

**Ventaja clave:** Predicción 2 días antes que Modelo 02, con performance prácticamente idéntica

**Variables Utilizadas (5):**
1. `mes_carga` - Mes de carga (1-12)
2. `sexo` - MACHO o HEMBRA
3. `kilos_recibidos_percapita` - Kilos de alimento hasta día 30
4. `tipoConstruccion` - Tradicional, Black Out, o Transversal
5. `densidad_pollos_m2` - Pollos por metro cuadrado

---

## 🎯 ¿Por Qué Modelo 03?

### **Comparación con Modelo 02:**

| Aspecto | Modelo 02 (32 días) | Modelo 03 (30 días) |
|---------|---------------------|---------------------|
| **MAE** | 1.5407g | 1.5459g (+0.005g) |
| **R²** | 0.8956 | 0.8951 (-0.05%) |
| **Días requeridos** | 32 | 30 (-2 días) ⚡ |
| **Predicción anticipada** | No | Sí (2 días antes) ✅ |

### **Ventajas:**
- ✅ **Predicción más temprana:** Decide estrategias 2 días antes
- ✅ **Datos más accesibles:** No necesitas esperar al día 32
- ✅ **Performance casi idéntico:** Solo 0.005g más de error
- ✅ **Mayor flexibilidad operativa**

### **Ideal para:**
- Toma de decisiones anticipada
- Planificación logística temprana
- Ajustes de manejo en tiempo real
- Escenarios donde los datos del día 31-32 no están disponibles

---

## 🚀 Inicio Rápido

### Opción 1: Uso Simple (Recomendado para principiantes)

```bash
python uso_simple.py
```

Este script incluye 3 ejemplos listos para usar:
- Predicción individual
- Predicción múltiple
- Predicción desde archivo CSV

### Opción 2: Uso Avanzado (Para desarrolladores)

```bash
python predictor.py
```

Ejecuta 4 ejemplos completos:
- Predicción simple
- Comparación de escenarios
- Predicción masiva
- Validación del modelo

---

## 📝 Uso Programático

### Predicción Individual

```python
from predictor import PredictorGanancia

# Inicializar (Modelo 03 - 30 días)
predictor = PredictorGanancia()

# Definir caso (alimento hasta día 30)
caso = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.5,  # Hasta día 30
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 14.5
}

# Predecir
resultado = predictor.predecir(caso)
ganancia = resultado['ganancia_predicha'].iloc[0]

print(f"Ganancia predicha: {ganancia:.2f} gramos")
```

### Predicción Múltiple

```python
import pandas as pd
from predictor import PredictorGanancia

predictor = PredictorGanancia()

# Crear DataFrame con varios casos
casos = pd.DataFrame([
    {'mes_carga': 6, 'sexo': 'MACHO', 'kilos_recibidos_percapita': 3.5, 
     'tipoConstruccion': 'Black Out', 'densidad_pollos_m2': 14.5},
    {'mes_carga': 7, 'sexo': 'HEMBRA', 'kilos_recibidos_percapita': 3.2,
     'tipoConstruccion': 'Tradicional', 'densidad_pollos_m2': 15.0}
])

# Predecir
resultados = predictor.predecir(casos)
print(resultados[['sexo', 'ganancia_predicha']])
```

### Predicción desde CSV

```python
from predictor import PredictorGanancia

predictor = PredictorGanancia()

# El CSV debe tener las columnas requeridas
resultado = predictor.predecir_lote('mis_datos.csv', guardar_resultado=True)

# Se genera automáticamente mis_datos_predicciones_modelo03.csv
```

---

## 📋 Formato de Datos de Entrada

### Variables Requeridas

| Variable | Tipo | Valores Válidos | Descripción |
|----------|------|-----------------|-------------|
| `mes_carga` | Numérico | 1-12 | Mes del año |
| `sexo` | Categórico | MACHO, HEMBRA | Sexo del pollo |
| `kilos_recibidos_percapita` | Numérico | 2.0-5.0 | Kilos de alimento **hasta día 30** |
| `tipoConstruccion` | Categórico | Tradicional, Black Out, Transversal | Tipo de gallinero |
| `densidad_pollos_m2` | Numérico | 9.0-50.0 | Pollos por metro cuadrado |

### ⚠️ Importante: Alimento hasta Día 30

A diferencia del Modelo 02 (32 días), este modelo usa:
```
kilos_recibidos_percapita = Alimento acumulado hasta el día 30
```

Asegúrate de usar los datos correctos según el día de proyección.

### Ejemplo de CSV

```csv
mes_carga,sexo,kilos_recibidos_percapita,tipoConstruccion,densidad_pollos_m2
6,MACHO,3.5,Black Out,14.5
7,HEMBRA,3.2,Tradicional,15.0
8,MACHO,3.8,Transversal,13.5
```

---

## 🔧 Funcionalidades Avanzadas

### Validación Automática

El predictor valida automáticamente:
- ✅ Presencia de todas las variables requeridas
- ✅ Valores válidos para categóricas
- ✅ Rangos numéricos correctos

```python
predictor = PredictorGanancia()

# Esto lanzará un error si los datos son inválidos
try:
    resultado = predictor.predecir(datos_invalidos)
except ValueError as e:
    print(f"Error: {e}")
```

### Feature Engineering Automático

El predictor aplica automáticamente:
- **Variables cíclicas:** `mes_sin`, `mes_cos` (para capturar estacionalidad)
- **Ratios:** `alimento_por_densidad`
- **Categorías:** `densidad_categoria` (Baja/Media/Alta/Muy_Alta)

### Estadísticas de Predicción

```python
predictor = PredictorGanancia()
resultado = predictor.predecir_lote('datos.csv')

# Mostrar estadísticas detalladas
predictor.estadisticas_prediccion(resultado)
```

Muestra:
- Promedio, desviación, min/max de ganancias predichas
- Estadísticas por sexo
- Estadísticas por tipo de construcción

---

## 📂 Estructura de Archivos

```
produccion03/
│
├── predictor.py              # Clase principal del predictor
├── uso_simple.py            # Script simple para usuarios
├── README.md                # Esta documentación
├── EJEMPLOS.md              # Ejemplos detallados de uso
│
└── (generados al ejecutar)
    └── *_predicciones_modelo03.csv   # Resultados de predicciones
```

---

## 🎯 Casos de Uso

### Caso 1: Decisión Temprana de Manejo

```python
# Al día 30, predecir ganancia final
predictor = PredictorGanancia()

caso_dia_30 = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.4,  # Hasta día 30
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 14.5
}

pred = predictor.predecir(caso_dia_30)
ganancia_esperada = pred['ganancia_predicha'].iloc[0]

print(f"Ganancia esperada al día 30: {ganancia_esperada:.2f}g")

# Decidir si ajustar alimentación días 31-32
if ganancia_esperada < 68.0:
    print("⚠️ Considerar aumentar alimento días 31-32")
```

### Caso 2: Comparación de Lotes

```python
# Evaluar múltiples lotes al día 30
lotes = pd.DataFrame([
    {'mes_carga': 6, 'sexo': 'MACHO', 'kilos_recibidos_percapita': 3.2,
     'tipoConstruccion': 'Tradicional', 'densidad_pollos_m2': 15.0},
    {'mes_carga': 6, 'sexo': 'MACHO', 'kilos_recibidos_percapita': 3.5,
     'tipoConstruccion': 'Black Out', 'densidad_pollos_m2': 14.0}
])

predictor = PredictorGanancia()
resultados = predictor.predecir(lotes, mostrar_detalles=False)

print("Comparación de lotes:")
for i, row in resultados.iterrows():
    print(f"Lote {i+1}: {row['ganancia_predicha']:.2f}g")
```

### Caso 3: Validación de Proyecciones

```python
# Comparar predicción día 30 vs resultado real día 32
predictor = PredictorGanancia()

# Predicción día 30
resultado = predictor.predecir_lote('datos_dia_30.csv')

# Luego al día 32, comparar con real
# Para evaluar precisión de la predicción anticipada
```

---

## 📊 Interpretación de Resultados

### Precisión del Modelo

- **MAE = 1.55g:** El modelo se equivoca en promedio ±1.55 gramos
- **R² = 0.895:** El modelo explica el 89.5% de la variabilidad
- **MAPE = 2.36%:** Error porcentual promedio de 2.36%

### Diferencia vs Modelo 02

Modelo 03 tiene solo **0.005g más de error** que Modelo 02:
- Diferencia insignificante en la práctica
- Beneficio de 2 días de anticipación
- Trade-off favorable: Precisión vs Tiempo

### Intervalos de Confianza

- ±1.55g es el error promedio (MAE)
- ±2.07g cubre ~68% de predicciones (RMSE)
- El 95% de predicciones están dentro de ±4g

### Factores que Afectan la Predicción

**Mayor impacto:**
1. `sexo` (correlación 0.84) - MACHO gana ~10g más
2. `kilos_recibidos_percapita` (0.79) - Más alimento = mayor ganancia
3. `tipoConstruccion` (-0.33) - Black Out mejor que Tradicional

**Menor impacto:**
4. `densidad_pollos_m2` (-0.19) - Más densidad = menor ganancia
5. `mes_carga` (0.05) - Efecto estacional menor

---

## 🔄 Comparación Modelo 02 vs Modelo 03

| Característica | Modelo 02 | Modelo 03 |
|----------------|-----------|-----------|
| **Días de datos** | 32 | 30 |
| **MAE** | 1.5407g | 1.5459g |
| **Diferencia MAE** | Baseline | +0.005g (0.3%) |
| **R²** | 0.8956 | 0.8951 |
| **Predicción anticipada** | No | Sí (2 días antes) |
| **Uso recomendado** | Máxima precisión | Decisión temprana |

**Conclusión:** Modelo 03 ofrece prácticamente la misma precisión con el beneficio de 2 días de anticipación.

---

## 🚨 Solución de Problemas

### Error: "Modelo no encontrado"

```bash
# Verificar que existe:
../../analisis/modelo03/modelo_limpio_final.pkl

# O especificar ruta completa:
predictor = PredictorGanancia(modelo_path='C:/ruta/completa/al/modelo')
```

### Error: "Valores inválidos"

```python
# Verificar valores válidos:
Sexo: 'MACHO' o 'HEMBRA' (case-sensitive)
Tipo: 'Tradicional', 'Black Out', o 'Transversal'
```

### Error: "Datos incorrectos"

⚠️ **Asegúrate de usar kilos hasta día 30:**
```python
# Correcto para Modelo 03
kilos_recibidos_percapita = alimento_acumulado_dia_30

# Incorrecto
kilos_recibidos_percapita = alimento_acumulado_dia_32  # ❌
```

---

## 📞 Soporte

### Preguntas Frecuentes

**P: ¿Cuál es la diferencia principal con Modelo 02?**  
R: Usa datos hasta día 30 en vez de día 32, permitiendo predicción 2 días antes con 0.005g más de error.

**P: ¿Es menos preciso que Modelo 02?**  
R: Prácticamente igual. Solo 0.005g más de error (0.3%), diferencia insignificante en la práctica.

**P: ¿Cuándo usar Modelo 03?**  
R: Cuando necesites decidir al día 30 o cuando los datos del día 31-32 no estén disponibles.

**P: ¿Puedo combinar ambos modelos?**  
R: Sí, puedes usar Modelo 03 al día 30 para decisión temprana, y Modelo 02 al día 32 para confirmación.

**P: ¿Los rangos de variables son los mismos?**  
R: Sí, las variables y rangos son idénticos, solo cambia el día de medición del alimento.

---

## 🔄 Actualizaciones y Mejoras

### Versión Actual: 1.0

**Características:**
- Predicción basada en 30 días de alimentación
- Performance equivalente a Modelo 02
- Predicción 2 días antes

**Próximas mejoras planeadas:**
- [ ] API REST para predicciones remotas
- [ ] Dashboard comparativo Modelo 02 vs 03
- [ ] Análisis de evolución predicción día 28-29-30-31-32
- [ ] Sistema de alertas tempranas

---

## 📚 Referencias

- **Modelo Base:** Modelo03 (30 días de alimentación)
- **Algoritmo:** ExtraTreesRegressor
- **Documentación PyCaret:** https://pycaret.gitbook.io/
- **Análisis Completo:** Ver carpeta `analisis/modelo03/`

---

**Última actualización:** 2025-10-05  
**Versión:** 1.0  
**Proyecto:** F35 Modelación - Sistema de Producción 03
