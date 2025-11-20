# 📊 Análisis Exhaustivo de Clusterización

## 📝 Descripción

Este directorio contiene un análisis completo para determinar si es conveniente crear **modelos separados por clusters** en lugar de un **modelo único** para predecir `ganancia_promedio_gramos`.

## 🎯 Objetivo

Responder la pregunta: **¿Conviene clusterizar los datos y crear modelos especializados por cluster, o es mejor mantener un único modelo global?**

## 🔬 Estrategias Evaluadas

1. **Modelo Único** (Baseline)
2. **Modelos por Sexo** (HEMBRA/MACHO)
3. **Modelos por Densidad** (pollos/m²)
4. **Modelos por Tipo de Construcción** (Tradicional/Transversal/Black Out)
5. **Modelos por Sector** (alhue, bosque viejo, etc.)
6. **Modelos por K-Means Clustering** (automático)
7. **Modelos por Hierarchical Clustering** (automático)
8. **Modelos por DBSCAN** (detección de densidad)

## 📦 Requisitos

### Paquetes Necesarios

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

### Librerías Utilizadas

#### Análisis de Datos
- `pandas` - Manipulación de datos
- `numpy` - Operaciones numéricas

#### Visualización
- `matplotlib` - Gráficos
- `seaborn` - Visualizaciones estadísticas

#### Machine Learning
- `scikit-learn`:
  - `KMeans` - Clustering k-medias
  - `DBSCAN` - Clustering basado en densidad
  - `AgglomerativeClustering` - Clustering jerárquico
  - `RandomForestRegressor` - Modelo de predicción
  - `GradientBoostingRegressor` - Boosting
  - Métricas de clustering: Silhouette, Davies-Bouldin, Calinski-Harabasz
  - Métricas de regresión: MAE, RMSE, R²

#### Estadística
- `scipy.stats` - Análisis estadístico (ANOVA)
- `scipy.cluster.hierarchy` - Dendrogramas

## 🚀 Ejecución

### Opción 1: Ejecución Directa

```bash
python analisis_clusterizacion_avanzado.py
```

### Opción 2: Desde Jupyter Notebook

```python
%run analisis_clusterizacion_avanzado.py
```

### Opción 3: Importar como módulo

```python
import sys
sys.path.append(r'C:\tecnoandina\f35_modelacion2\analisis\clusterizacion')
from analisis_clusterizacion_avanzado import *
```

## 📊 Resultados Generados

Al ejecutar el script, se generan los siguientes archivos:

### 📈 Visualizaciones

1. **`comparacion_estrategias.png`**
   - Comparación de MAE, RMSE, R² y CV MAE para todas las estrategias
   - Gráficos de barras horizontales

2. **`kmeans_metricas.png`**
   - Elbow curve (Inertia)
   - Silhouette Score por K
   - Davies-Bouldin Score por K

3. **`visualizacion_clusters.png`**
   - Proyección PCA de clusters K-Means
   - Proyección PCA de clusters Hierarchical
   - Distribución por Sexo en espacio PCA

4. **`dendrograma.png`**
   - Dendrograma del clustering jerárquico
   - Visualización de las últimas 30 fusiones

### 📁 Datos

5. **`comparacion_estrategias.csv`**
   - Tabla comparativa de todas las estrategias
   - Columnas: Estrategia, N_Modelos, MAE, RMSE, R², CV_MAE

6. **`resultados_detallados.json`**
   - Resultados completos en formato JSON
   - Incluye métricas por cada grupo/cluster

7. **`dataset_con_clusters.csv`**
   - Dataset original con asignaciones de clusters
   - Columnas adicionales: cluster_kmeans, cluster_hierarchical, cluster_dbscan

### 📄 Reporte

8. **`REPORTE_CLUSTERIZACION.md`**
   - Reporte ejecutivo en Markdown
   - Resumen de hallazgos
   - Recomendación final
   - Análisis estadístico detallado

## 🔍 Análisis Realizados

### 1. Análisis Exploratorio de Grupos Naturales
- Estadísticas descriptivas por grupo
- ANOVA para detectar diferencias significativas
- Identificación de p-values

### 2. Clustering Automático

#### K-Means
- Búsqueda del K óptimo (2-10 clusters)
- Métricas: Silhouette, Davies-Bouldin, Calinski-Harabasz
- Selección automática del mejor K

#### Hierarchical Clustering
- Método: Ward linkage
- Dendrograma para visualización
- Comparación con K-Means

#### DBSCAN
- Detección de clusters por densidad
- Identificación de outliers
- Parámetros: eps=2.0, min_samples=5

### 3. Evaluación de Modelos

Para cada estrategia se calcula:
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R²** (Coeficiente de determinación)
- **CV MAE** (Cross-Validation MAE con k-fold)

Modelo utilizado: **Random Forest Regressor**
- 100 árboles
- Paralelización automática
- Validación cruzada de 5 folds

### 4. Comparación y Ranking

Las estrategias se ordenan por MAE (menor es mejor) y se determina:
- Mejor estrategia absoluta
- Mejora porcentual vs baseline
- Recomendación de implementación

## 📋 Interpretación de Resultados

### Métricas Clave

- **MAE < 3.0**: Excelente
- **MAE 3.0-5.0**: Bueno
- **MAE 5.0-7.0**: Aceptable
- **MAE > 7.0**: Necesita mejora

### Criterios de Decisión

#### ✅ Usar Clusterización si:
- Mejora > 5% vs baseline
- Diferencias significativas entre grupos (ANOVA p < 0.05)
- Clusters bien definidos (Silhouette > 0.5)

#### ⚠️ Evaluar Trade-off si:
- Mejora 1-5% vs baseline
- Complejidad operacional alta
- Recursos limitados para mantenimiento

#### ❌ Mantener Modelo Único si:
- Mejora < 1% o negativa
- ANOVA p > 0.05 (no hay diferencias significativas)
- Clusters mal definidos (Silhouette < 0.3)

## 🔧 Personalización

### Modificar Parámetros de Clustering

```python
# K-Means
k_range = range(2, 15)  # Probar más valores de K

# DBSCAN
dbscan = DBSCAN(eps=3.0, min_samples=10)  # Ajustar sensibilidad
```

### Cambiar Modelo de Predicción

```python
# Usar Gradient Boosting en lugar de Random Forest
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
```

### Agregar Nuevas Estrategias

```python
# Ejemplo: Modelos por combinación de variables
df['combo'] = df['sexo'] + '_' + df['tipoConstruccion']
estrategias_resultados.append(
    evaluar_estrategia(df, "MODELOS POR SEXO+TIPO", grupo_col='combo')
)
```

## 📊 Output Esperado

### Consola

```
================================================================================
ANÁLISIS EXHAUSTIVO DE CLUSTERIZACIÓN
================================================================================

1. Cargando datos...
   ✓ Dataset cargado: 1234 filas, 13 columnas

2. Variables identificadas:
   • Numéricas: 5
   • Categóricas: 3
   • Target: ganancia_promedio_gramos

================================================================================
2. ANÁLISIS DE GRUPOS NATURALES
================================================================================

   📊 SEXO:
   ...
   ANOVA: F-statistic=125.4567, p-value=0.000001
   ✓ Diferencias SIGNIFICATIVAS entre grupos (p < 0.05)

...

================================================================================
6. RECOMENDACIÓN FINAL
================================================================================

   🏆 MEJOR ESTRATEGIA: 2. MODELOS POR SEXO

   Métricas:
   • MAE: 2.8451
   • RMSE: 3.6789
   • R²: 0.8567
   • Número de modelos: 2

   📈 Mejora vs Baseline: 8.34%

   ✅ RECOMENDACIÓN: Usar clusterización (2. MODELOS POR SEXO)
      La mejora de 8.34% justifica la complejidad adicional.
```

## 🎓 Conceptos Clave

### Clustering
- **K-Means**: Agrupa datos en K clusters minimizando la varianza intra-cluster
- **Hierarchical**: Construye una jerarquía de clusters (árbol)
- **DBSCAN**: Identifica clusters de alta densidad y outliers

### Métricas de Clustering
- **Silhouette Score**: Qué tan bien están separados los clusters (-1 a 1, mayor es mejor)
- **Davies-Bouldin**: Relación entre distancias intra e inter-cluster (menor es mejor)
- **Calinski-Harabasz**: Ratio de varianza entre vs dentro de clusters (mayor es mejor)

### ANOVA (Analysis of Variance)
- Prueba si las medias de múltiples grupos son significativamente diferentes
- p-value < 0.05: Diferencias estadísticamente significativas

## 🐛 Troubleshooting

### Error: "No module named 'sklearn'"
```bash
pip install scikit-learn
```

### Error: Memoria insuficiente
```python
# Reducir n_estimators o usar submuestreo
rf = RandomForestRegressor(n_estimators=50, max_samples=0.5)
```

### Warning: Convergencia de K-Means
```python
# Aumentar max_iter
kmeans = KMeans(n_clusters=k, max_iter=500, n_init=20)
```

## 📞 Soporte

Para preguntas o mejoras, contactar al equipo de Data Science de Tecnoandina.

---

**Última actualización:** 2025-10-05
**Versión:** 1.0
**Autor:** Sistema de Análisis Automatizado
