# 🚀 Sistema de Predicción - Producción 01

Sistema de producción para predecir ganancia promedio de pollos usando **Modelo 02 (Versión Limpia)**.

---

## 📊 Características del Modelo

**Modelo:** ExtraTreesRegressor  
**Performance:**
- MAE: 1.54 gramos
- R²: 0.896 (89.6% de varianza explicada)
- MAPE: 2.36%

**Variables Utilizadas (5):**
1. `mes_carga` - Mes de carga (1-12)
2. `sexo` - MACHO o HEMBRA
3. `kilos_recibidos_percapita` - Kilos de alimento por pollo
4. `tipoConstruccion` - Tradicional, Black Out, o Transversal
5. `densidad_pollos_m2` - Pollos por metro cuadrado

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

# Inicializar
predictor = PredictorGanancia()

# Definir caso
caso = {
    'mes_carga': 6,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.5,
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

# Se genera automáticamente mis_datos_predicciones.csv
```

---

## 📋 Formato de Datos de Entrada

### Variables Requeridas

| Variable | Tipo | Valores Válidos | Descripción |
|----------|------|-----------------|-------------|
| `mes_carga` | Numérico | 1-12 | Mes del año |
| `sexo` | Categórico | MACHO, HEMBRA | Sexo del pollo |
| `kilos_recibidos_percapita` | Numérico | 2.0-5.0 | Kilos de alimento por pollo |
| `tipoConstruccion` | Categórico | Tradicional, Black Out, Transversal | Tipo de gallinero |
| `densidad_pollos_m2` | Numérico | 9.0-50.0 | Pollos por metro cuadrado |

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
produccion01/
│
├── predictor.py              # Clase principal del predictor
├── uso_simple.py            # Script simple para usuarios
├── README.md                # Esta documentación
├── EJEMPLOS.md              # Ejemplos detallados de uso
│
└── (generados al ejecutar)
    └── *_predicciones.csv   # Resultados de predicciones masivas
```

---

## 🎯 Casos de Uso

### Caso 1: Planificación de Producción

```python
# Comparar diferentes configuraciones
escenarios = [
    {'mes_carga': 6, 'sexo': 'MACHO', 'kilos_recibidos_percapita': 3.2, 
     'tipoConstruccion': 'Tradicional', 'densidad_pollos_m2': 15.0},
    {'mes_carga': 6, 'sexo': 'MACHO', 'kilos_recibidos_percapita': 3.5,
     'tipoConstruccion': 'Black Out', 'densidad_pollos_m2': 14.0}
]

predictor = PredictorGanancia()
for i, escenario in enumerate(escenarios, 1):
    pred = predictor.predecir(escenario, mostrar_detalles=False)
    ganancia = pred['ganancia_predicha'].iloc[0]
    print(f"Escenario {i}: {ganancia:.2f}g")
```

### Caso 2: Validación de Crianza

```python
# Predecir ganancia esperada para una nueva crianza
nueva_crianza = {
    'mes_carga': 10,
    'sexo': 'MACHO',
    'kilos_recibidos_percapita': 3.6,
    'tipoConstruccion': 'Black Out',
    'densidad_pollos_m2': 14.0
}

predictor = PredictorGanancia()
resultado = predictor.predecir(nueva_crianza)
ganancia_esperada = resultado['ganancia_predicha'].iloc[0]

print(f"Ganancia esperada: {ganancia_esperada:.2f}g")
# Usar este valor para comparar con el resultado real
```

### Caso 3: Análisis Masivo

```python
# Procesar todas las crianzas del último año
predictor = PredictorGanancia()
resultado = predictor.predecir_lote('crianzas_2024.csv', guardar_resultado=True)

# Analizar resultados
predictor.estadisticas_prediccion(resultado)
```

---

## ⚙️ Configuración

### Cambiar Ruta del Modelo

Por defecto, el predictor busca el modelo en:
```
../../analisis/modelo02/modelo_limpio_final.pkl
```

Para cambiar:
```python
predictor = PredictorGanancia(modelo_path='ruta/a/tu/modelo')
```

### Personalizar Validación

Puedes modificar los rangos válidos editando `predictor.py`:

```python
# En la clase PredictorGanancia.__init__()
self.rangos_validos = {
    'mes_carga': (1, 12),
    'kilos_recibidos_percapita': (2.0, 5.0),  # Ajustar según necesidad
    'densidad_pollos_m2': (9.0, 50.0)
}
```

---

## 📊 Interpretación de Resultados

### Precisión del Modelo

- **MAE = 1.54g:** El modelo se equivoca en promedio ±1.54 gramos
- **R² = 0.896:** El modelo explica el 89.6% de la variabilidad
- **MAPE = 2.36%:** Error porcentual promedio de 2.36%

### Intervalos de Confianza

El modelo predice con alta precisión, pero considera:
- ±1.54g es el error promedio (MAE)
- ±2.06g cubre ~68% de predicciones (RMSE)
- El 95% de predicciones están dentro de ±4g

### Factores que Afectan la Predicción

**Mayor impacto:**
1. `sexo` (correlación 0.84) - MACHO gana ~10g más
2. `kilos_recibidos_percapita` (0.83) - Más alimento = mayor ganancia
3. `tipoConstruccion` (-0.33) - Black Out mejor que Tradicional

**Menor impacto:**
4. `densidad_pollos_m2` (-0.19) - Más densidad = menor ganancia
5. `mes_carga` (0.05) - Efecto estacional menor

---

## 🚨 Solución de Problemas

### Error: "Modelo no encontrado"

```bash
# Verificar que existe:
../../analisis/modelo02/modelo_limpio_final.pkl

# O especificar ruta completa:
predictor = PredictorGanancia(modelo_path='C:/ruta/completa/al/modelo')
```

### Error: "Valores inválidos"

```python
# Verificar valores válidos:
Sexo: 'MACHO' o 'HEMBRA' (case-sensitive)
Tipo: 'Tradicional', 'Black Out', o 'Transversal'
```

### Error: "Columna faltante"

Asegúrate de que tu CSV/DataFrame tenga exactamente estas columnas:
- mes_carga
- sexo
- kilos_recibidos_percapita
- tipoConstruccion
- densidad_pollos_m2

---

## 📞 Soporte

### Preguntas Frecuentes

**P: ¿Puedo usar el modelo con datos de otras granjas?**  
R: Sí, siempre que las variables estén en los mismos rangos y categorías.

**P: ¿Cómo actualizo el modelo?**  
R: Entrena un nuevo modelo en `analisis/` y actualiza la ruta en el predictor.

**P: ¿Qué hacer si la predicción parece incorrecta?**  
R: Verifica que los datos de entrada estén en los rangos válidos. El modelo fue entrenado con datos históricos específicos.

**P: ¿Puedo exportar predicciones a Excel?**  
R: Sí, el CSV generado se puede abrir directamente en Excel.

---

## 🔄 Actualizaciones y Mejoras

### Versión Actual: 1.0

**Próximas mejoras planeadas:**
- [ ] API REST para predicciones remotas
- [ ] Dashboard web interactivo
- [ ] Exportación a múltiples formatos (JSON, Excel, PDF)
- [ ] Cálculo de intervalos de confianza
- [ ] Comparación con datos históricos reales

---

## 📚 Referencias

- **Modelo Base:** Modelo02 (Versión Limpia)
- **Algoritmo:** ExtraTreesRegressor
- **Documentación PyCaret:** https://pycaret.gitbook.io/
- **Análisis Completo:** Ver carpeta `analisis/modelo02/`

---

**Última actualización:** 2025-10-05  
**Versión:** 1.0  
**Proyecto:** F35 Modelación - Sistema de Producción
