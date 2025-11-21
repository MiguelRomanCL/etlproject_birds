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

## 8. Árbol completo del repositorio
```
repo/
├── analisis/
│   ├── modelo01/analisis_modelamiento_pycaret.py
│   ├── modelo02/analisis_modelamiento_limpio.py
│   ├── modelo03/analisis_modelamiento_limpio.py
│   ├── clusterizacion/analisis_clusterizacion_avanzado.py
│   └── clusterizacion2/analisis_clusterizacion_simplificado.py
├── docs/01_estado_actual_repo.md
├── ejecucion_vigente/
│   ├── crianza_vigentes/ [no hay .py]
│   ├── crianzas_vigentes/
│   │   ├── 01_preparacion_datos.py
│   │   ├── 02_consolidacion_datos.py
│   │   ├── 03_inclusion_ventilacion_densidad.py
│   │   ├── 04_proyeccion_ganancias.py
│   │   └── ejecutar_proyeccion.bat
│   ├── crianzas_vigentes_oficial/ (réplica de 01–04)
│   └── compilado/
│       ├── compilado_01.py  ← genera proyecciones extendidas
│       └── compilado_02.py  ← variante no llamada en flujo principal
├── produccion/
│   ├── produccion01/
│   │   ├── predictor.py
│   │   └── uso_simple.py
│   └── produccion03/
│       ├── predictor.py     ← usa modelo03 con interfaz de clase
│       └── uso_simple.py
├── requirements.txt
└── work_data/ (datos de trabajo versionados en repo)
```
Archivos con lógica relevante fuera del flujo 01–04:
- `ejecucion_vigente/compilado/compilado_01.py` genera proyecciones por pabellón a futuro usando `resumen_crianzas_con_proyeccion.csv`. 【F:ejecucion_vigente/compilado/compilado_01.py†L17-L163】
- `produccion/produccion03/predictor.py` expone clase para predecir con Modelo03 (misma lógica de features). 【F:produccion/produccion03/predictor.py†L1-L199】
- Scripts en `analisis/` contienen notebooks/experimentos de entrenamiento (no llamados en flujo, pero referencian modelos). 【F:analisis/modelo03/analisis_modelamiento_limpio.py†L1-L20】

## 9. Tabla detallada Input → Transformación → Output por script
| Script | Inputs exactos | Columnas esperadas | Transformaciones | Output(s) | Riesgos |
| --- | --- | --- | --- | --- | --- |
| `01_preparacion_datos.py` | SAP en `C:\\repositorio_data\\crianza_web_pollos_vigentes` (`cargado_pabellones/*.xlsx`, `mortalidad/*.xls`, `guias_alimento/*.xls`) | Guías: `Fecha Guía`, `Cantidad Total`, `Sexo`; Mortalidad: `Fecha Movimiento`, `Cantidad`, `Edad`; Alimento: `F.Guía`, `Kilos` | Limpia encodings, agrupa por sector/crianza, calcula stock y `kilos_recibidos_percapita`, uniforma strings. | `data/resumen_crianzas.pkl`, `data/resumen_alimento.pkl` | Dependencia a rutas Windows; fallas silenciosas por archivos faltantes; sin control de schema. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】 |
| `02_consolidacion_datos.py` | Pickles del paso 01 | `Fecha Guía Inicio`, `Fecha Guía Fin`, `Edad`, `kilos_recibidos_percapita` | Calcula `mes_carga`, `anio_carga`, `edad_actual`, fija `edad_proyeccion_dias=30`, filtra `edad_criterio_proyeccion>=32`, mergea alimento por edad redondeada. | `work_data/resumen_crianzas_para_modelo.(csv|xlsx)` | Cálculo de edad usa `today()` (no reproducible); riesgo de NaN en merge; constante de proyección fija. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L38】 |
| `03_inclusion_ventilacion_densidad.py` | CSV del paso 2; tablas MySQL `maestrospabellones`, `maestrossectorescrianza` | Datos previos + columnas `nombreSector`, `numero`, `tipoConstruccion`, `areaUtil`, `sistemaVentilacion`, `zonaGeografica` | Consulta MySQL con credenciales embebidas, uniforma strings, mergea atributos, calcula `densidad_pollos_m2`, rellena `tipoConstruccion`, filtra `edad_actual 32–41`. | `work_data/resumen_crianzas_para_proyeccion.(csv|xlsx)` | Credenciales hardcodeadas; dependencia a red/SSL; drops que eliminan columnas base; imputaciones fijas. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L57】 |
| `04_proyeccion_ganancias.py` | CSV del paso 3 | Variables requeridas `mes_carga`, `sexo`, `kilos_recibidos_percapita`, `tipoConstruccion`, `densidad_pollos_m2`; mapeo `Sexo→sexo` | Validación de columnas/valores/rangos, limpieza de nulos, reemplazo de `Sin Información` y densidad<0, feature engineering (mes_sin/cos, ratios), filtrado de sectores y predicción PyCaret. | `work_data/resumen_crianzas_con_proyeccion.csv` | Dependencia a modelo externo; validaciones detienen flujo; parámetros mágicos; exclusión de sectores (`DON WILSON`, `EL CARMEN`). 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L425】 |
| `compilado/compilado_01.py` | `work_data/resumen_crianzas_con_proyeccion.csv`; archivos estado en `C:\\repositorio_data\\crianza_web_pollos_vigentes\\info_general/*.xlsx`; proyecciones oficiales en `C:\\tecnoandina\\f35\data\proyecciones_oficiales` | Columnas de status (`Edad Proy.`, `Pab.`, `Sexo`, etc.) y `ganancia_proyectada` | Filtra edades 32–41, genera series futuras por pabellón, integra proyecciones “con silos”, exporta a Excel expandido y formateado. | `compilado/proyeccion_pollos_expandido.xlsx`, `compilado/proyeccion_pollos_YYYYMMDD.xlsx` | Más rutas Windows, supuestos sobre archivos externos, multiplicación directa de ganancia*edad (riesgo de lógica duplicada). 【F:ejecucion_vigente/compilado/compilado_01.py†L17-L163】 |
| `produccion/produccion03/predictor.py` | DataFrames o CSV con variables requeridas | Variables listas para modelo | Encapsula validación, feature engineering y predicción en clase `PredictorGanancia`. | CSV con `_predicciones_modelo03.csv` (opcional) | Ruta de modelo relativa fija; rangos distintos (kilos 2–5); lógica duplicada respecto a 04. 【F:produccion/produccion03/predictor.py†L25-L198】 |

## 10. Catalogación de funciones internas
- `01_preparacion_datos.py`: `uniformar_strings` (normaliza texto) y `split_filename` (parsea nombres de archivo); resto en cuerpo principal carga SAP y genera pickles. Candidatas: utilidades de limpieza → `extract/`, lógica de parsing/aggregation → `transform/`. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L9-L110】
- `02_consolidacion_datos.py`: `uniformar_strings` duplicada; cuerpo principal calcula edades y merges. Candidata a `transform/` (cálculo de edad y merge con alimento); utilidades de string a `shared/utils.py`. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L7-L38】
- `03_inclusion_ventilacion_densidad.py`: `uniformar_strings`, `query_database`; luego merge de maestros y cálculo de densidad. `query_database` debería ir a `extract/db.py`; densidad y filtros a `transform/enriquecimiento.py`. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L8-L57】
- `04_proyeccion_ganancias.py`: utilidades `validar_archivo_existe`, `cargar_datos`, `mapear_columnas`, `limpiar_datos_nulos`, `validar_columnas_requeridas`, `validar_valores`, `mostrar_estadisticas_input`, `preparar_features`, `realizar_proyeccion`, `agregar_columna_proyeccion`, `mostrar_estadisticas_proyeccion`, `guardar_resultado`, `mostrar_ejemplos`, `main`. Candidatas: validaciones y features → `transform/validation.py`; `realizar_proyeccion` y carga de modelo → `predict/service.py`; CLI → `src/main.py`. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L466】
- `compilado_01.py`: `uniformar_strings`; resto procedural para expansión de proyecciones; lógica de series futuras candidata a módulo `predict/postprocess.py`. 【F:ejecucion_vigente/compilado/compilado_01.py†L9-L163】
- `produccion/produccion03/predictor.py`: métodos `validar_input`, `preparar_features`, `predecir`, `predecir_lote`, `estadisticas_prediccion`; duplican lógica de 04 pero orientada a clase; mover a `predict/api.py` compartido. 【F:produccion/produccion03/predictor.py†L19-L199】

## 11. Parámetros, constantes y reglas de negocio hardcodeados
| Nombre | Valor | Ubicación | Razón | Sugerencia de parametrización |
| --- | --- | --- | --- | --- |
| `EDAD_PROYECCION` | 30 días | `02_consolidacion_datos.py` línea 16 | Punto de corte para alimentar Modelo03 | Variable de entorno o config YAML para permitir otros horizontes. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L25】 |
| Filtro edad actual | ≥32 días (y ≤41 en paso 3) | `02_consolidacion_datos.py` línea 30; `03_inclusion_ventilacion_densidad.py` línea 49 | Limitar crianzas aptas para proyección | Parametrizar rango en config y aplicar en un solo módulo. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L49-L51】 |
| Imputación densidad negativa | Reemplazo por 14.5 | `04_proyeccion_ganancias.py` líneas 396-398 | Ajuste de calidad de datos previo a validación | Configurable por ambiente o reglas de negocio centralizadas. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L390-L399】 |
| Imputación tipo construcción | `Sin Información` → `Black Out` | `04_proyeccion_ganancias.py` líneas 390-395 | Normalizar categórica antes de validar | Configurable/mapeable en archivo de lookups. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L390-L395】 |
| Rango densidad | 9.0–50.0 | `04_proyeccion_ganancias.py` líneas 57-61 | Umbral de validación del modelo | Llevar a configuración compartida con predictor de producción. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L52-L61】 |
| Rango alimento per cápita | 1.0–6.0 | `04_proyeccion_ganancias.py` líneas 57-60 | Validación numérica previa a predicción | Configurable según versión de modelo. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L57-L60】 |
| Exclusión de sectores | `DON WILSON`, `EL CARMEN` | `04_proyeccion_ganancias.py` línea 377 | Limpieza manual de sectores | Parametrizar lista de exclusión en config/tabla. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L375-L378】 |
| Mapeo sexo | `MAPEO_COLUMNAS = {"Sexo": "sexo"}` y valores válidos HEMBRA/MACHO | `04_proyeccion_ganancias.py` líneas 48-55 | Alinear columnas con modelo | Centralizar mapeos en capa de ingestión. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L48-L55】 |
| Filtros de compilado | Excluye sectores (`alhue`, `don wilson`, `el carmen`, `la punta`) y edades 32–41 | `compilado_01.py` líneas 45-61 | Ajuste para reportes de pabellón | Llevar a config de reportes y reutilizar lógica de filtros. 【F:ejecucion_vigente/compilado/compilado_01.py†L45-L61】 |

## 12. Dependencias cruzadas entre scripts
- `01_preparacion_datos.py` crea `nombre_sector_code`, `nro_crianza`, `Edad`, `kilos_recibidos_percapita` usados en merges posteriores. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L63-L105】
- `02_consolidacion_datos.py` depende de `Fecha Guía Inicio/Fin` y agrega `edad_actual`, `edad_proyeccion_dias`, `edad_criterio_proyeccion` que usa `03` para filtrar; además mantiene `Cantidad Total` y `Pabellón`. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L19-L38】
- `03_inclusion_ventilacion_densidad.py` agrega `tipoConstruccion`, `densidad_pollos_m2`, `zonaGeografica`; estos campos son requeridos/validados en `04_proyeccion_ganancias.py` (`VARIABLES_REQUERIDAS`, rangos). 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L51】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L39-L61】
- `04_proyeccion_ganancias.py` produce `ganancia_proyectada` consumida por `compilado_01.py` para generar proyecciones diarias por pabellón. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L281-L425】【F:ejecucion_vigente/compilado/compilado_01.py†L68-L90】
- `produccion/produccion03/predictor.py` reutiliza misma lógica de features de 04, por lo que cualquier cambio en validaciones/features debe sincronizarse para evitar divergencias en lote vs. producción. 【F:produccion/produccion03/predictor.py†L36-L119】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L234-L255】

## 13. Hallazgos importantes para refactor
1) Credenciales y rutas embebidas en múltiples scripts (`C:\\\\repositorio_data\\...`, host `10.195.6.14`, usuario `usuario_lectura`). Riesgo alto de filtración y falta de portabilidad. 【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】【F:ejecucion_vigente/compilado/compilado_01.py†L17-L32】
2) Duplicación de lógica de features/validaciones entre `04_proyeccion_ganancias.py` y `produccion/produccion03/predictor.py`, lo que generará drift si se actualiza solo uno. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L234-L320】【F:produccion/produccion03/predictor.py†L36-L119】
3) Filtros y reglas de negocio distribuidos (edades, exclusión de sectores, imputaciones) sin configuración central, dificultando pruebas parametrizadas. 【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L38】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L375-L399】
4) Dependencia fuerte a Windows (rutas absolutas, `.bat`, paths a `C:\tecnoandina\...`) impide ejecución en entornos Linux/Docker actuales. 【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L1-L13】【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L1-L59】【F:ejecucion_vigente/compilado/compilado_01.py†L17-L126】
5) Datos versionados en repo (`work_data`, `compilado/*.xlsx`) sobrescritos en cada ejecución, sin aislamiento por run ni limpieza automática. 【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L56-L57】【F:ejecucion_vigente/compilado/compilado_01.py†L126-L163】
