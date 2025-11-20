# 📊 REPORTE DE ANÁLISIS Y MODELAMIENTO

**Fecha:** 2025-10-05 16:54:21  
**Objetivo:** Predecir `ganancia_promedio_gramos` usando las mejores técnicas de ML

---

## 1. Resumen Ejecutivo

### Dataset
- **Filas originales:** 6,294
- **Filas finales:** 6,294
- **Features originales:** 7
- **Features finales:** 12 (con feature engineering)

### Variables Analizadas

**Variables Originales:**
- `mes_carga`
- `edad_madres_dias`
- `peso_inicial_gramos`
- `sexo`
- `kilos_recibidos_percapita`
- `tipoConstruccion`
- `densidad_pollos_m2`

**Target:**
- `ganancia_promedio_gramos`

---

## 2. Análisis Exploratorio

### Variables Categóricas


**sexo:**
- HEMBRA: 3,444 (54.7%)
- MACHO: 2,850 (45.3%)

**tipoConstruccion:**
- Tradicional: 3,213 (51.0%)
- Black Out: 2,484 (39.5%)
- Transversal: 597 (9.5%)


### Correlaciones con Target

**Top 5 correlaciones:**

- `sexo`: 0.8442
- `kilos_recibidos_percapita`: 0.8267
- `peso_inicial_gramos`: 0.1355
- `edad_madres_dias`: 0.1031
- `mes_carga`: 0.0496


### ⚠️ Multicolinealidad Detectada

**Pares de features con correlación > 0.7:**

- `edad_madres_dias` <-> `peso_inicial_gramos`: 0.901
- `sexo` <-> `kilos_recibidos_percapita`: 0.825


### Análisis VIF

| Feature | VIF | Interpretación |
|---------|-----|----------------|
| peso_inicial_gramos | 256.66 | 🔴 Severa |
| kilos_recibidos_percapita | 91.28 | 🔴 Severa |
| edad_madres_dias | 51.02 | 🔴 Severa |
| densidad_pollos_m2 | 17.33 | 🔴 Severa |
| mes_carga | 4.28 | 🟢 OK |


---

## 3. Feature Engineering

Se crearon las siguientes features adicionales:

### Variables Cíclicas
- `mes_sin`: Componente seno del mes
- `mes_cos`: Componente coseno del mes

### Ratios y Derivadas
- `alimento_por_densidad`: kilos_recibidos / densidad
- `peso_inicial_por_densidad`: peso_inicial / densidad

### Categorizaciones
- `edad_madres_categoria`: Joven/Adulta/Madura/Vieja
- `densidad_categoria`: Baja/Media/Alta/Muy Alta

**Total features finales:** 12

---

## 4. Detección de Outliers

| Variable | Outliers | % del Total |
|----------|----------|-------------|
| mes_carga | 0 | 0.00% |
| edad_madres_dias | 37 | 0.59% |
| peso_inicial_gramos | 0 | 0.00% |
| kilos_recibidos_percapita | 0 | 0.00% |
| densidad_pollos_m2 | 981 | 15.59% |

---

## 5. Resultados del Modelamiento

### 🏆 Mejor Modelo: LGBMRegressor

**Métricas de Rendimiento:**
- **MAE:** 1.5307 gramos
- **RMSE:** 1.9960 gramos
- **R²:** 0.9022 (90.22% de varianza explicada)

### Interpretación

- El modelo predice con un error promedio de **±1.53 gramos**
- Explica el **90.2%** de la variabilidad en la ganancia


---

## 6. Archivos Generados

### 📊 Visualizaciones
1. `01_matriz_correlacion.png` - Matriz de correlación completa
2. `02_distribuciones.png` - Distribuciones de variables numéricas
3. `03_target_por_categoricas.png` - Target por variables categóricas
4. `04_top_correlaciones.png` - Scatter plots de top correlaciones
5. `05_vif_analysis.png` - Análisis de multicolinealidad (VIF)
6. `06_feature_importance.png` - Importancia de features
7. `07_predicciones_vs_real.png` - Predicciones vs valores reales
8. `08_analisis_residuos.png` - Análisis de residuos

### 📄 Datos y Modelos
- `resultados_analisis.json` - Resultados completos en JSON
- `feature_importance.csv` - Importancia de features
- `modelo_final.pkl` - Modelo entrenado (pickle)
- `REPORTE_ANALISIS.md` - Este reporte

---

## 7. Recomendaciones

### ✅ Variables a Mantener


### 🎯 Próximos Pasos

1. **Validación en producción:** Evaluar el modelo con datos nuevos
2. **Monitoreo continuo:** Tracking de MAE y R² en tiempo real
3. **Reentrenamiento periódico:** Actualizar modelo cada 1-3 meses
4. **A/B Testing:** Comparar predicciones con métodos actuales


---

## 8. Conclusiones

1. **Feature Engineering fue exitoso:** Se crearon 5 features adicionales que mejoran el modelo

2. **Multicolinealidad:** Se detectaron correlaciones altas entre algunas variables

3. **Outliers:** Se detectaron outliers en varias variables, pero PyCaret los maneja automáticamente

4. **Rendimiento del modelo:** MAE=1.53g, R²=90.22%

---

**Análisis completado exitosamente ✅**
