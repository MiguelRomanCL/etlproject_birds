# 📊 Modelo 02 - Versión Limpia sin Multicolinealidad

## 📝 Descripción

Modelo simplificado que **elimina variables con multicolinealidad extrema** manteniendo solo las 5 variables clave para predicción de `ganancia_promedio_gramos`.

## 🎯 Objetivo

Crear un modelo **simple, robusto y sin multicolinealidad** que:
- ✅ Mantenga el rendimiento del Modelo 01
- ✅ Elimine VIF > 100 (multicolinealidad extrema)
- ✅ Use solo variables realmente necesarias
- ✅ Sea más fácil de interpretar y mantener

## 🔬 Diferencia con Modelo 01

### Modelo 01 (Original)
```
7 variables:
✓ mes_carga (VIF=4.28)
✓ edad_madres_dias (VIF=51.02) ← ELIMINADA
✓ peso_inicial_gramos (VIF=256.66) ← ELIMINADA
✓ sexo
✓ kilos_recibidos_percapita (VIF=91.28)
✓ tipoConstruccion
✓ densidad_pollos_m2 (VIF=17.33)

Resultado: R²=0.9022, MAE=1.53g
Problema: Multicolinealidad severa (VIF hasta 256!)
```

### Modelo 02 (Limpio)
```
5 variables:
✓ mes_carga
❌ edad_madres_dias (ELIMINADA - VIF=51, correlación=0.103)
❌ peso_inicial_gramos (ELIMINADA - VIF=256, correlación=0.135)
✓ sexo
✓ kilos_recibidos_percapita
✓ tipoConstruccion
✓ densidad_pollos_m2

Resultado: R²=?, MAE=? (se compara automáticamente)
Ventaja: VIF máximo < 10, sin multicolinealidad
```

## 📊 Variables Seleccionadas

### 1. **sexo** 
- Correlación con target: **0.844** ⭐
- Diferencia HEMBRA/MACHO: ~11 gramos
- ANOVA: p < 0.0001 (muy significativa)

### 2. **kilos_recibidos_percapita**
- Correlación con target: **0.827** ⭐
- Variable clave de alimentación
- Aunque tiene VIF alto, es predictor esencial

### 3. **densidad_pollos_m2**
- Correlación con target: **-0.195**
- Información única sobre espacio
- Afecta crecimiento y estrés

### 4. **tipoConstruccion**
- Correlación con target: **-0.330**
- Black Out > Transversal > Tradicional
- ANOVA: p < 0.0001

### 5. **mes_carga**
- Correlación con target: **0.050**
- VIF: **4.28** ✅ (bajo)
- Convertida a sin/cos (cíclica)

## ❌ Variables Eliminadas

### **edad_madres_dias**
- **Razón:** VIF=51 (multicolinealidad severa)
- Correlación con target: solo 0.103 (baja)
- Correlación con peso_inicial: 0.901 (redundante)
- **Conclusión:** No aporta información única

### **peso_inicial_gramos**
- **Razón:** VIF=256 (multicolinealidad EXTREMA)
- Correlación con target: solo 0.135 (baja directa)
- Su efecto ya está capturado por otras variables
- **Conclusión:** Completamente redundante

## 🚀 Ejecución

### Opción 1: Un Click
```
1. Navegar a: C:\tecnoandina\f35_modelacion2\analisis\modelo03\
2. Doble click: ejecutar_analisis.bat
3. Esperar: 5-10 minutos
4. Revisar: REPORTE_MODELO_LIMPIO.md
```

### Opción 2: Línea de Comandos
```bash
cd C:\tecnoandina\f35_modelacion2\analisis\modelo03
pip install -r requirements.txt
python analisis_modelamiento_limpio.py
```

### Opción 3: PyCharm/Jupyter
```python
%run C:\tecnoandina\f35_modelacion2\analisis\modelo03\analisis_modelamiento_limpio.py
```

## 📦 Requisitos

- Python 3.8+
- PyCaret 3.0+
- Pandas, NumPy, Scikit-learn
- Matplotlib, Seaborn
- Scipy, Statsmodels

```bash
pip install -r requirements.txt
```

## 📊 Archivos Generados

### Visualizaciones (7 PNG)
1. `01_matriz_correlacion_limpia.png`
2. `02_distribuciones_limpias.png`
3. `03_comparacion_vif.png` - ⭐ **Comparación Modelo 01 vs 02**
4. `04_top_correlaciones_limpias.png`
5. `05_feature_importance_limpio.png`
6. `06_predicciones_vs_real_limpio.png`
7. `07_analisis_residuos_limpio.png`

### Modelos y Datos
- `modelo_limpio_final.pkl` - Modelo entrenado
- `feature_importance_limpio.csv`
- `resultados_modelo_limpio.json`

### Reportes
- `REPORTE_MODELO_LIMPIO.md` - **Reporte ejecutivo con comparación**

## 🔍 Análisis Realizados

### 1. Análisis de Correlaciones
- Matriz completa de 5 variables
- Top correlaciones con target
- Detección de correlaciones entre features

### 2. Análisis VIF (Multicolinealidad)
- Cálculo de VIF para cada variable
- Comparación Modelo 01 vs Modelo 02
- Verificación de mejora

### 3. Feature Engineering
- Variables cíclicas: `mes_sin`, `mes_cos`
- Ratio: `alimento_por_densidad`
- Categoría: `densidad_categoria`

### 4. Modelado con PyCaret
- Comparación automática de modelos
- Selección del mejor algoritmo
- Optimización de hiperparámetros

### 5. Comparación con Modelo 01
- MAE: ¿Se mantiene el rendimiento?
- R²: ¿Cuánta varianza explica?
- **Trade-off:** Simplicidad vs Performance

## 📈 Interpretación de Resultados

### Escenario Ideal ✅
```
Modelo 02 MAE ≈ Modelo 01 MAE (diferencia < 0.1)

Conclusión: ¡Éxito total!
- Mismo rendimiento
- Sin multicolinealidad
- Más simple
→ Usar Modelo 02
```

### Escenario Aceptable ⚠️
```
Modelo 02 MAE > Modelo 01 MAE (diferencia 0.1-0.3)

Conclusión: Trade-off razonable
- Pérdida menor en performance
- Gran ganancia en robustez
- Modelo más interpretable
→ Evaluar prioridades
```

### Escenario Crítico 🔴
```
Modelo 02 MAE >> Modelo 01 MAE (diferencia > 0.3)

Conclusión: Variables eliminadas eran importantes
- Considerar mantener una de ellas
- O usar Modelo 01 con precaución
→ Revisar estrategia
```

## 🎯 Ventajas del Modelo Limpio

### ✅ **Robustez**
- Sin multicolinealidad extrema
- Menos sensible a cambios en datos
- Mejor generalización

### ✅ **Simplicidad**
- Solo 5 variables vs 7
- Más fácil de entender
- Más fácil de mantener

### ✅ **Interpretabilidad**
- Cada variable aporta información única
- No hay redundancia
- Coeficientes/importancias más confiables

### ✅ **Eficiencia**
- Menos features = más rápido
- Menos datos necesarios
- Deployment más simple

## ⚠️ Consideraciones

### Multicolinealidad Residual
- `kilos_recibidos_percapita` aún tiene VIF alto
- **Razón:** Es predictor clave (correlación 0.827)
- **Decisión:** Mantener por su importancia

### Performance vs Simplicidad
- Posible pérdida menor en MAE
- **Trade-off:** Aceptable por robustez
- **Resultado:** Depende de prioridades del negocio

## 📊 Métricas Esperadas

### Si VIF se reduce exitosamente:
```
VIF Máximo Modelo 01: 256.66
VIF Máximo Modelo 02: < 20 (idealmente < 10)

Reducción: > 90%
```

### Performance (estimado):
```
Modelo 01: MAE=1.53g, R²=0.9022
Modelo 02: MAE=1.5-1.8g, R²=0.85-0.90

Pérdida aceptable: < 10% en métricas
```

## 🚀 Deployment

### Usar Modelo 02 si:
1. ✅ MAE diferencia < 0.1g vs Modelo 01
2. ✅ Priorizas robustez y simplicidad
3. ✅ Quieres modelo fácil de mantener
4. ✅ VIF se reduce significativamente

### Usar Modelo 01 si:
1. ⚠️ MAE diferencia > 0.3g vs Modelo 02
2. ⚠️ Cada 0.1g de precisión es crítico
3. ⚠️ Puedes manejar multicolinealidad
4. ⚠️ Tienes expertise en interpretación

## 📝 Próximos Pasos

1. **Ejecutar análisis**
   ```bash
   ejecutar_analisis.bat
   ```

2. **Revisar REPORTE_MODELO_LIMPIO.md**
   - Ver comparación con Modelo 01
   - Analizar VIF mejorado
   - Leer recomendación final

3. **Analizar visualizaciones**
   - Especialmente `03_comparacion_vif.png`
   - Ver `06_predicciones_vs_real_limpio.png`

4. **Tomar decisión**
   - ¿Usar Modelo 01 o Modelo 02?
   - Basarse en métricas objetivas
   - Considerar contexto del negocio

## ❓ Preguntas Frecuentes

**P: ¿Por qué eliminar variables si el Modelo 01 funciona bien?**  
R: Multicolinealidad alta (VIF=256) causa:
- Inestabilidad en producción
- Dificultad para interpretar
- Riesgo de overfitting
- Problemas con datos nuevos

**P: ¿Por qué mantener kilos_recibidos si tiene VIF alto?**  
R: Porque:
- Correlación muy alta con target (0.827)
- Es variable de negocio clave (alimentación)
- Su VIF es por correlación con sexo (normal)
- Aporta información única crítica

**P: ¿El modelo será peor sin edad_madres y peso_inicial?**  
R: Probablemente NO porque:
- Su correlación con target es baja (0.10 y 0.13)
- Su VIF es altísimo (redundantes)
- Su información ya está en otras variables
- El test lo confirmará

**P: ¿Cómo sé si funcionó?**  
R: Compara en el reporte:
- Si MAE diferencia < 0.1g → Éxito
- Si VIF máximo < 10 → Multicolinealidad eliminada
- Si R² > 0.85 → Rendimiento excelente

## 📚 Referencias

- [Multicolinealidad (VIF)](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html)
- [Feature Selection](https://scikit-learn.org/stable/modules/feature_selection.html)
- [PyCaret Documentation](https://pycaret.gitbook.io/)

## 🎓 Lecciones Aprendidas

### Del Análisis Modelo 01:
1. VIF=256 es **extremadamente** alto
2. Correlación alta entre edad_madres y peso_inicial (0.901)
3. Estas variables tienen baja correlación directa con target
4. LightGBM maneja multicolinealidad, pero no es ideal

### Estrategia Modelo 02:
1. Eliminar variables redundantes (VIF > 50)
2. Priorizar variables con correlación alta con target
3. Mantener variables de negocio clave
4. Verificar que performance no se degrade

---

**¡Listo para ejecutar y comparar!** 🚀

```bash
cd C:\tecnoandina\f35_modelacion2\analisis\modelo03
ejecutar_analisis.bat
```

**Duración:** 5-10 minutos  
**Output:** Comparación completa Modelo 01 vs Modelo 02

---

**Última actualización:** 2025-10-05  
**Versión:** 1.0  
**Proyecto:** F35 Modelación - Modelo Limpio
