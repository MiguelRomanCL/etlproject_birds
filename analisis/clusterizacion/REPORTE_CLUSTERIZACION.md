# REPORTE: Análisis de Clusterización para Modelos Predictivos

**Fecha:** 2025-10-05 15:19:40

## 1. Resumen Ejecutivo

Este análisis evalúa si es conveniente crear modelos separados por clusters en lugar de un modelo único
para predecir `ganancia_promedio_gramos`.

### Estrategias Evaluadas:
1. Modelo Único (Baseline)
2. Modelos por Sexo
3. Modelos por Densidad
4. Modelos por Tipo de Construcción
5. Modelos por Sector
6. Modelos por K-Means Clustering
7. Modelos por Hierarchical Clustering

## 2. Mejor Estrategia Identificada

**3. MODELOS POR DENSIDAD**

- **MAE:** 1.4663
- **RMSE:** 1.8643
- **R²:** 0.4373
- **Número de Modelos:** 71

### Mejora vs Baseline: 2.58%

## 3. Tabla Comparativa Completa

| Estrategia                        |   N_Modelos |     MAE |    RMSE |       R² |   CV_MAE |
|:----------------------------------|------------:|--------:|--------:|---------:|---------:|
| 3. MODELOS POR DENSIDAD           |          71 | 1.46627 | 1.86434 | 0.437276 |  2.04579 |
| 1. MODELO ÚNICO (Baseline)        |           1 | 1.50506 | 1.95542 | 0.906109 |  2.27114 |
| 4. MODELOS POR TIPO CONSTRUCCIÓN  |           3 | 1.52145 | 1.93427 | 0.875787 |  2.33187 |
| 5. MODELOS POR SECTOR             |          70 | 1.5368  | 1.93014 | 0.49345  |  2.51629 |
| 6. MODELOS POR K-MEANS (k=2)      |           2 | 1.53875 | 2.0044  | 0.638064 |  2.32475 |
| 2. MODELOS POR SEXO               |           2 | 1.53875 | 2.0044  | 0.638064 |  2.32475 |
| 7. MODELOS POR HIERARCHICAL (k=2) |           2 | 1.56616 | 2.02164 | 0.672209 |  2.35497 |

## 4. Análisis Estadístico de Grupos Naturales

### SEXO
- **ANOVA p-value:** 0.000000
- **Significativo:** Sí

### DENSIDAD
- **ANOVA p-value:** 0.000000
- **Significativo:** Sí

### TIPO DE CONSTRUCCIÓN
- **ANOVA p-value:** 0.000000
- **Significativo:** Sí

### SECTOR
- **ANOVA p-value:** 0.000000
- **Significativo:** Sí

## 5. Clustering Automático

### K-Means
- **K óptimo (Silhouette):** 2
- **Silhouette Score:** 0.238

### Hierarchical
- **K utilizado:** 2
- **Método:** Ward linkage

### DBSCAN
- **Clusters encontrados:** 5
- **Puntos de ruido:** 3

## 6. Recomendación Final


⚠️ **PRECAUCIÓN: Mejora marginal**

La mejora de **2.58%** es positiva pero marginal. Evaluar si el trade-off entre
complejidad y mejora es favorable para el caso de uso específico.

**Recomendación:** Usar modelo único a menos que la pequeña mejora sea crítica para el negocio.


## 7. Archivos Generados

- `comparacion_estrategias.png` - Gráficos comparativos de todas las estrategias
- `kmeans_metricas.png` - Análisis de K óptimo para K-Means
- `visualizacion_clusters.png` - Visualización PCA de los clusters
- `dendrograma.png` - Dendrograma del clustering jerárquico
- `comparacion_estrategias.csv` - Tabla comparativa en CSV
- `resultados_detallados.json` - Resultados completos en JSON
- `dataset_con_clusters.csv` - Dataset con asignación de clusters

## 8. Próximos Pasos Sugeridos

1. Validar la estrategia recomendada con datos nuevos
2. Analizar la estabilidad de los clusters en el tiempo
3. Considerar ensembles que combinen múltiples estrategias
4. Evaluar el impacto en producción con A/B testing
