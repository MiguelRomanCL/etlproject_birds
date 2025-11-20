# 📊 Proyección de Ganancias - Crianzas Vigentes

Script para proyectar ganancias de crianzas vigentes usando el **Modelo 03** (datos hasta día 30).

---

## 🎯 Propósito

Este script toma el archivo de crianzas vigentes y proyecta la ganancia esperada al final de la crianza usando el Modelo 03 entrenado.

---

## 📂 Archivos

### Entrada
```
C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_para_proyeccion.csv
```

**Columnas requeridas:**
- `mes_carga` - Mes de carga (1-12)
- `Sexo` - MACHO o HEMBRA (se mapea automáticamente a minúsculas)
- `kilos_recibidos_percapita` - Kilos de alimento por pollo (hasta día 30)
- `tipoConstruccion` - Tradicional, Black Out, o Transversal
- `densidad_pollos_m2` - Pollos por metro cuadrado

### Salida
```
C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_con_proyeccion.csv
```

**Columnas originales + columna nueva:**
- `ganancia_proyectada` - Ganancia proyectada en gramos

---

## 🚀 Cómo Ejecutar

### Opción 1: Doble Click (Más Fácil)
```
1. Navegar a: C:\tecnoandina\f35_modelacion2\ejecucion_vigente\crianzas_vigentes\
2. Doble click en: ejecutar_proyeccion.bat
3. Ver resultados en pantalla
```

### Opción 2: Línea de Comandos
```bash
cd C:\tecnoandina\f35_modelacion2\ejecucion_vigente\crianzas_vigentes
python 04_proyeccion_ganancias.py
```

### Opción 3: Desde Python/Jupyter
```python
%run C:\tecnoandina\f35_modelacion2\ejecucion_vigente\crianzas_vigentes\04_proyeccion_ganancias.py
```

---

## 📊 Proceso del Script

El script realiza los siguientes pasos:

1. ✅ **Validación de archivo** - Verifica que exista el CSV de entrada
2. ✅ **Carga de datos** - Lee el CSV
3. ✅ **Mapeo de columnas** - Ajusta nombres (ej: "Sexo" → "sexo")
4. ✅ **Validación de columnas** - Verifica que estén todas las requeridas
5. ✅ **Estadísticas de entrada** - Muestra resumen del dataset
6. ✅ **Carga del modelo** - Inicializa el Modelo 03
7. ✅ **Proyección** - Calcula ganancia_proyectada para cada registro
8. ✅ **Agregar columna** - Añade ganancia_proyectada al dataframe
9. ✅ **Estadísticas de proyección** - Muestra resumen de resultados
10. ✅ **Guardar resultado** - Exporta CSV con proyecciones

---

## 📈 Salida del Script

### Ejemplo de output en consola:

```
================================================================================
🚀 PROYECCIÓN DE GANANCIAS - MODELO 03
================================================================================

Modelo: Producción 03 (datos hasta día 30)
Fecha: 2025-10-06 15:30:45

✓ Archivo encontrado: resumen_crianzas_para_proyeccion.csv

📂 Cargando datos desde: C:\...\resumen_crianzas_para_proyeccion.csv
   ✓ Datos cargados: 156 registros
   ✓ Columnas: 19

🔄 Mapeando nombres de columnas...
   ✓ Columnas mapeadas:
      • Sexo → sexo

🔍 Validando columnas requeridas...
   ✓ Todas las columnas requeridas están presentes:
      • mes_carga
      • sexo
      • kilos_recibidos_percapita
      • tipoConstruccion
      • densidad_pollos_m2

📊 Estadísticas del dataset:
   • Total de registros: 156
   • Crianzas únicas: 12
   • Pabellones únicos: 156
   • Sectores únicos: 10

   📍 Distribución por sexo:
      • HEMBRA: 78 (50.0%)
      • MACHO: 78 (50.0%)

   🏗️  Distribución por tipo de construcción:
      • Black Out: 120 (76.9%)
      • Tradicional: 24 (15.4%)
      • Transversal: 12 (7.7%)

   📈 Rango de alimento (kg/pollo):
      • Mínimo: 2.45 kg
      • Máximo: 3.85 kg
      • Promedio: 3.12 kg

🤖 Cargando Modelo 03 (30 días de alimentación)...
   ✓ Modelo cargado exitosamente

🤖 Realizando proyección con Modelo 03...
   ✓ Proyección completada para 156 registros

📝 Agregando columna de proyección...
   ✓ Columna 'ganancia_proyectada' agregada

📊 Estadísticas de proyección:
   • Ganancia promedio proyectada: 66.45 gramos
   • Desviación estándar: 5.32 gramos
   • Mínimo: 58.20 gramos
   • Máximo: 74.80 gramos
   • Mediana: 65.90 gramos

   🐔 Ganancia proyectada por sexo:
      • MACHO: 72.15 ± 2.34 gramos
      • HEMBRA: 60.75 ± 2.18 gramos

   🏗️  Ganancia proyectada por tipo de construcción:
      • Black Out: 68.45 ± 4.21 gramos
      • Tradicional: 62.58 ± 5.12 gramos
      • Transversal: 66.21 ± 5.43 gramos

📋 Primeros 10 registros con proyección:
========================================================================================================================
nombre_sector  nro_crianza  Pabellón  sexo    kilos_recibidos_percapita  tipoConstruccion  densidad_pollos_m2  ganancia_proyectada
BOSQUE VIEJO   226          1         HEMBRA  2.76                       Black Out         16.00               60.45
BOSQUE VIEJO   226          2         HEMBRA  2.76                       Black Out         18.00               59.82
...

💾 Guardando resultado en: resumen_crianzas_con_proyeccion.csv
   ✓ Archivo guardado exitosamente
   📍 Ruta completa: C:\...\resumen_crianzas_con_proyeccion.csv

================================================================================
✅ PROYECCIÓN COMPLETADA EXITOSAMENTE
================================================================================

📊 Resumen:
   • Registros procesados: 156
   • Ganancia promedio proyectada: 66.45g
   • Archivo de salida: resumen_crianzas_con_proyeccion.csv
```

---

## 🔍 Validaciones

El script valida automáticamente:

### Columnas Requeridas
- ✅ Verifica que existan las 5 variables del Modelo 03
- ✅ Mapea nombres diferentes (ej: "Sexo" → "sexo")
- ❌ Error si falta alguna columna

### Valores Válidos
- ✅ `sexo`: Solo MACHO o HEMBRA
- ✅ `tipoConstruccion`: Solo Tradicional, Black Out, o Transversal
- ✅ `mes_carga`: Entre 1 y 12
- ✅ `kilos_recibidos_percapita`: Entre 2.0 y 5.0 kg
- ✅ `densidad_pollos_m2`: Entre 9.0 y 50.0 pollos/m²

---

## ⚠️ Notas Importantes

### 1. Datos hasta Día 30
El Modelo 03 usa **alimento acumulado hasta día 30**, no hasta día 32.

Asegúrate que `kilos_recibidos_percapita` refleje esto.

### 2. Precisión del Modelo
- **MAE:** 1.55 gramos
- **R²:** 0.895 (89.5%)
- **MAPE:** 2.36%

Las predicciones pueden tener un error de ±1.55g en promedio.

### 3. Variables No Usadas
El modelo NO usa:
- ❌ `edad_madres_dias` (eliminada por multicolinealidad)
- ❌ `peso_inicial_gramos` (eliminada por multicolinealidad)
- ❌ `mortalidad_porcentual` (no disponible al momento de predicción)

### 4. Diferencias en Nombres de Columnas
El script mapea automáticamente:
- `Sexo` → `sexo`

Si tu CSV tiene otros nombres, edita el `MAPEO_COLUMNAS` en el script.

---

## 🐛 Solución de Problemas

### Error: "Archivo no encontrado"
```
❌ Error: Archivo no encontrado
   No se encontró el archivo de entrada:
   C:\...\resumen_crianzas_para_proyeccion.csv
```

**Solución:** Verifica que el archivo exista en la ruta correcta.

### Error: "Falta la variable requerida"
```
❌ Error de validación: Falta la variable requerida: sexo
```

**Solución:** 
1. Verifica que el CSV tenga la columna `Sexo` o `sexo`
2. Si tiene otro nombre, agrégalo al `MAPEO_COLUMNAS`

### Error: "Valores inválidos"
```
❌ Error de validación: Valores inválidos en sexo: {'M', 'F'}
```

**Solución:** 
- El modelo espera: `MACHO` o `HEMBRA`
- Transforma tus datos antes de ejecutar el script

### Error: "Fuera de rango"
```
❌ Error de validación: kilos_recibidos_percapita fuera de rango [2.0, 5.0]
```

**Solución:** 
- Verifica que los datos estén en unidades correctas
- Valores fuera de rango pueden indicar error en los datos

---

## 📝 Personalización

### Cambiar rutas de archivos

Edita las constantes en el script:

```python
INPUT_FILE = SCRIPT_DIR.parent / 'work_data' / 'resumen_crianzas_para_proyeccion.csv'
OUTPUT_FILE = SCRIPT_DIR.parent / 'work_data' / 'resumen_crianzas_con_proyeccion.csv'
```

### Agregar más mapeos de columnas

```python
MAPEO_COLUMNAS = {
    'Sexo': 'sexo',
    'TipoConstruccion': 'tipoConstruccion',  # Ejemplo adicional
    'Densidad': 'densidad_pollos_m2'          # Ejemplo adicional
}
```

### Mostrar más/menos ejemplos

Cambia el parámetro `n` en la llamada:

```python
mostrar_ejemplos(df_resultado, n=20)  # Mostrar 20 en vez de 10
```

---

## 📚 Recursos Relacionados

- **Modelo 03:** `../../analisis/modelo03/`
- **Predictor:** `../../produccion/produccion03/predictor.py`
- **Documentación Modelo:** `../../produccion/produccion03/README.md`
- **Ejemplos:** `../../produccion/produccion03/EJEMPLOS.md`

---

## 📞 Soporte

### Preguntas Frecuentes

**P: ¿Por qué usa Modelo 03 y no Modelo 01?**  
R: Modelo 03 usa datos hasta día 30 (vs día 32), permitiendo predicción 2 días antes con prácticamente la misma precisión.

**P: ¿Puedo usar este script con datos de día 32?**  
R: Sí, pero deberías usar el script equivalente con Modelo 01 para máxima precisión.

**P: ¿Qué hago si faltan columnas?**  
R: Agrega las columnas faltantes al CSV o ajusta el `MAPEO_COLUMNAS` si tienen otros nombres.

**P: ¿El archivo de salida sobrescribe el original?**  
R: No, se crea un archivo nuevo: `resumen_crianzas_con_proyeccion.csv`

---

**Última actualización:** 2025-10-06  
**Versión:** 1.0  
**Proyecto:** F35 Modelación - Ejecución Vigente
