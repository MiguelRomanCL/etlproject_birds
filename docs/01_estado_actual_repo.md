# PR0 — Estado actual del repositorio

## 1. Entry point y flujo principal
- ENTRYPOINT actual (manual/Windows): `ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py` y el wrapper `ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat`. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L1-L38】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L1-L59】
- Secuencia real del pipeline (ejecución manual 01 → 02 → 03 → 04):
  1. `ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py` lee extractos SAP desde `C:\repositorio_data\crianza_web_pollos_vigentes` y genera `ejecucion_vigente/data/resumen_crianzas.pkl` y `ejecucion_vigente/data/resumen_alimento.pkl`. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】
  2. `ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py` calcula edad y filtra crianzas, cruza con alimento a día 30 y escribe `ejecucion_vigente/work_data/resumen_crianzas_para_modelo.(xlsx|csv)`. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L38】
  3. `ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py` enriquece con maestros MySQL (credenciales embebidas), calcula densidad y exporta `ejecucion_vigente/work_data/resumen_crianzas_para_proyeccion.(xlsx|csv)`. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L57】
  4. `ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py` valida y transforma, carga el modelo PyCaret 03 y produce `ejecucion_vigente/work_data/resumen_crianzas_con_proyeccion.csv`. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L424】

## 2. Descripción por script (crianzas_vigentes)
### `01_preparacion_datos.py`
- Ruta: `ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py`.
- Inputs: archivos SAP en Windows `C:\\repositorio_data\\crianza_web_pollos_vigentes` (subcarpetas `cargado_pabellones`, `guias_alimento`, `mortalidad`, etc.). 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L109】
- Transformación: resume carga de pabellones, mortalidad y guías de alimento; estandariza nombres; calcula stock y kilos per cápita. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L40-L105】
- Outputs: pickles `ejecucion_vigente/data/resumen_crianzas.pkl` y `ejecucion_vigente/data/resumen_alimento.pkl`. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L107-L110】
- Dependencias externas: lecturas de archivos SAP en rutas absolutas de Windows.

### `02_consolidacion_datos.py`
- Ruta: `ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py`.
- Inputs: pickles generados en el paso 01 (`../data/resumen_crianzas.pkl`, `../data/resumen_alimento.pkl`). 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L19-L35】
- Transformación: calcula mes/año de carga y edad, filtra crianzas con edad media ≥32 días y cruza con alimentación en `EDAD_PROYECCION=30`. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L35】
- Outputs: `ejecucion_vigente/work_data/resumen_crianzas_para_modelo.xlsx` y `.csv`. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L37-L38】
- Dependencias externas: ninguna adicional (usa pandas/numpy).

### `03_inclusion_ventilacion_densidad.py`
- Ruta: `ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py`.
- Inputs: `../work_data/resumen_crianzas_para_modelo.csv` del paso 2 y tablas MySQL `maestrospabellones` y `maestrossectorescrianza` (credenciales embebidas). 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L49】
- Transformación: agrega ventilación/tipo/área, calcula densidad por m², rellena tipo de construcción faltante y filtra edades 32–41. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L37-L51】
- Outputs: `ejecucion_vigente/work_data/resumen_crianzas_para_proyeccion.xlsx` y `.csv`. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L56-L57】
- Dependencias externas: base MySQL `ta_ags_pollos` vía SQLAlchemy/PyMySQL, credenciales hardcodeadas (`usuario_lectura` / `Agro.2025#Read`, host `10.195.6.14`). 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】

### `04_proyeccion_ganancias.py`
- Ruta: `ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py`.
- Inputs: `../work_data/resumen_crianzas_para_proyeccion.csv` generado en el paso 3. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L37】
- Transformación: validaciones de columnas/rangos, mapeo de sexo, limpieza de nulos, feature engineering (seno/coseno mes, ratios), y filtrado de sectores específicos antes de predecir. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L88-L425】
- Outputs: CSV final `ejecucion_vigente/work_data/resumen_crianzas_con_proyeccion.csv` con columna `ganancia_proyectada`. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L33-L34】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L316-L327】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L422-L436】
- Dependencias externas: modelo PyCaret cargado desde `analisis/modelo03/modelo_limpio_final`; ejecución en Windows documentada en comentarios de cabecera. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L1-L38】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L405-L408】

### `ejecutar_proyeccion.bat`
- Ruta: `ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat`.
- Propósito: comprobación de Python, verificación de `work_data/resumen_crianzas_para_proyeccion.csv`, ejecución de `04_proyeccion_ganancias.py` y reporte del resultado `work_data/resumen_crianzas_con_proyeccion.csv`. 【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L1-L59】

## 3. Modelos y artefactos
- Modelo activo: `analisis/modelo03/modelo_limpio_final.pkl`, cargado por `pycaret.regression.load_model` desde ruta `analisis/modelo03/modelo_limpio_final` (sin extensión en la llamada). 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L36-L408】【300485†L1-L5】
- Modelos presentes pero no usados en el flujo de crianzas vigentes: `analisis/modelo02/modelo_limpio_final.pkl` y `analisis/modelo01/modelo_final.pkl` (otros entrenamientos históricos). 【a06d78†L1-L5】【bde7fa†L1-L4】

## 4. Outputs y rutas de datos
- Intermedios (pickles):
  - `ejecucion_vigente/data/resumen_crianzas.pkl` y `ejecucion_vigente/data/resumen_alimento.pkl` generados por 01. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L107-L110】
- Datasets de trabajo:
  - `ejecucion_vigente/work_data/resumen_crianzas_para_modelo.(xlsx|csv)` generados por 02. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L37-L38】
  - `ejecucion_vigente/work_data/resumen_crianzas_para_proyeccion.(xlsx|csv)` generados por 03. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L57】
- Output final:
  - `ejecucion_vigente/work_data/resumen_crianzas_con_proyeccion.csv` generado por 04 y validado por el batch. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L33-L34】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L22-L58】
- Compilados posteriores (pabellón): scripts `ejecucion_vigente/compilado/compilado_01.py` producen `proyeccion_pollos_expandido.xlsx` y variantes `proyeccion_pollos_YYYYMMDD.xlsx` en la misma carpeta. 【F:ejecucion_vigente/compilado/compilado_01.py†L17-L162】

## 5. Acoplamientos y dependencias ocultas
- ⚠ Rutas absolutas de Windows para insumos SAP (`base_path = C:\\repositorio_data\\crianza_web_pollos_vigentes`). 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L109】
- ⚠ Credenciales MySQL hardcodeadas (`usuario_lectura` / `Agro.2025#Read`, host `10.195.6.14`) dentro de la función de conexión. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】
- ⚠ Dependencia Windows y batch para orquestación (`ejecutar_proyeccion.bat` y rutas comentadas en 04). 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L1-L13】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L1-L59】
- ⚠ Lógica de negocio mezclada con I/O y constantes mágicas (EDAD_PROYECCION=30, imputaciones de tipo construcción y densidad). 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L35】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L390-L399】
- ⚠ Librerías usadas pero no declaradas en `requirements.txt` (ej.: `pycaret`, `sqlalchemy`, `pymysql`, `tqdm`). 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L23-L24】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L3-L27】【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L1-L7】【F:requirements.txt†L1-L26】

## 6. Problemas estructurales
**CRÍTICOS**
- Ausencia de punto de entrada único; ejecución depende de scripts sueltos y batch de Windows. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L1-L38】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L1-L59】
- Configuración sensible embebida (rutas absolutas y credenciales) sin `.env` ni parametrización. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L109】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】

**RECOMENDADOS**
- Logging disperso (prints, `logs.log` plano) sin esquema estructurado. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L365-L457】
- Validaciones y reglas de negocio codificadas inline, difíciles de reutilizar o probar. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L372-L424】
- Dependencias de librerías no reflejadas en `requirements.txt`. 【F:requirements.txt†L1-L26】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L18-L24】

**OPCIONALES**
- Outputs intermedios y finales versionados directamente en el repo (`work_data`, `compilado/`) sin control de sobrescritura. 【F:ejecucion_vigente/compilado/compilado_01.py†L16-L162】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L57】

## 7. Resumen ejecutivo técnico
El flujo actual se ejecuta manualmente desde Windows, disparando `04_proyeccion_ganancias.py` o su wrapper `.bat`, luego de preparar insumos con los scripts 01–03 en `ejecucion_vigente/crianzas_vigentes`. Cada etapa depende de rutas y credenciales hardcodeadas, produce archivos intermedios en `ejecucion_vigente/data` y `work_data`, y finalmente agrega `ganancia_proyectada` usando un modelo PyCaret cargado desde `analisis/modelo03/modelo_limpio_final`. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L424】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L22-L58】

El repositorio muestra alto acoplamiento (rutas absolutas, credenciales, lógica y parámetros mezclados con I/O) y carece de un punto de entrada unificado o configuración externa. Este documento funciona como radiografía del estado presente para orientar el refactor posterior hacia una arquitectura modular, configurable y portable. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L57】【F:requirements.txt†L1-L26】
