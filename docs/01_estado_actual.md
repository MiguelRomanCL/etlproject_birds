# Estado actual del sistema de predicción avícola

## 1. Entry Points y Flujo Principal
- Script principal de cálculo: `ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py`.
- Lanzador Windows: `ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat` invoca directamente `python 04_proyeccion_ganancias.py` tras validar la existencia del CSV de entrada en `work_data`.【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L22-L59】
- Flujo detectado por dependencias de archivos (no automatizado):
  1. `01_preparacion_datos.py` genera `data/resumen_crianzas.pkl` y `data/resumen_alimento.pkl` a partir de múltiples archivos de origen SAP locales.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】
  2. `02_consolidacion_datos.py` toma los pkl previos, calcula edades y filtra, y produce `work_data/resumen_crianzas_para_modelo.{csv,xlsx}`.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L38】
  3. `03_inclusion_ventilacion_densidad.py` enriquece con datos de MySQL y calcula densidad, exportando `work_data/resumen_crianzas_para_proyeccion.{csv,xlsx}`.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L57】
  4. `04_proyeccion_ganancias.py` valida, transforma y proyecta usando el modelo 03, escribiendo `work_data/resumen_crianzas_con_proyeccion.csv`.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L437】
  5. Los scripts `compilado_01.py` y `compilado_02.py` (fuera del flujo principal) consumen `resumen_crianzas_con_proyeccion.csv` para generar reportes ampliados con silos y exportaciones Excel.【F:ejecucion_vigente/compilado/compilado_01.py†L16-L113】【F:ejecucion_vigente/compilado/compilado_02.py†L14-L79】

## 2. Inventario de Scripts (Análisis por Archivo)
| Script | Ubicación | Inputs leídos | Lógica principal | Outputs escritos | Librerías externas |
|---|---|---|---|---|---|
| 01_preparacion_datos.py | `ejecucion_vigente/crianzas_vigentes` | Archivos Excel/HTML locales bajo `C:\repositorio_data\crianza_web_pollos_vigentes` (cargado_pabellones, guias_alimento, mortalidad).【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L99】 | Extrae/normaliza sector y crianza desde nombres de archivo, resume carga y mortalidad, calcula kilogramos per cápita acumulados.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L17-L105】 | `../data/resumen_crianzas.pkl`, `../data/resumen_alimento.pkl`.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L107-L110】 | pandas, pkg_sap_agrosuper.resumen_documentos, tqdm, unicodedata, re, os |
| 02_consolidacion_datos.py | `ejecucion_vigente/crianzas_vigentes` | `../data/resumen_crianzas.pkl`, `../data/resumen_alimento.pkl`.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L19-L35】 | Calcula edad actual y objetivo, filtra crianzas con criterio ≥32 días, mergea alimentación a edad 30.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L36】 | `../work_data/resumen_crianzas_para_modelo.{xlsx,csv}`.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L37-L38】 | pandas, numpy, unicodedata, re |
| 03_inclusion_ventilacion_densidad.py | `ejecucion_vigente/crianzas_vigentes` | `../work_data/resumen_crianzas_para_modelo.csv`; tablas MySQL `maestrospabellones`, `maestrossectorescrianza`.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L49】 | Consulta MySQL con credenciales embebidas, enriquece con construcción/área/ventilación, calcula densidad y filtra edades 32-41 días, normaliza tipo de construcción nulo.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L53】 | `../work_data/resumen_crianzas_para_proyeccion.{xlsx,csv}`.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L55-L57】 | pandas, numpy, sqlalchemy, unicodedata, re, pymysql (via SQLAlchemy) |
| 04_proyeccion_ganancias.py | `ejecucion_vigente/crianzas_vigentes` | `../work_data/resumen_crianzas_para_proyeccion.csv`; modelo `analisis/modelo03/modelo_limpio_final` cargado con PyCaret.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L111】 | Validaciones de columnas/valores, limpieza de nulos, ingeniería de features (mes_sin/cos, razón alimento-densidad, categorías), predicción con modelo 03 y estadísticas de salida.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L172-L337】 | `../work_data/resumen_crianzas_con_proyeccion.csv`.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L316-L437】 | pandas, numpy, pycaret.regression, pathlib, warnings |

## 3. Modelos y Artefactos
- Modelos `.pkl` localizados en `analisis/modelo01/modelo_final.pkl`, `analisis/modelo02/modelo_limpio_final.pkl`, `analisis/modelo03/modelo_limpio_final.pkl`.【F:analisis/modelo01/REPORTE_ANALISIS.md†L1-L15】【F:analisis/modelo03/README.md†L1-L14】
- Carga de modelo en ejecución: `load_model(str(MODELO_PATH))` donde `MODELO_PATH` apunta a `analisis/modelo03/modelo_limpio_final`.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L36-L408】
- Pickles intermedios generados: `data/resumen_crianzas.pkl` y `data/resumen_alimento.pkl` creados en el paso 01.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L107-L110】

## 4. Mapa de Datos (Inputs/Outputs)
| Archivo Generado | Script Creador | Ruta Destino | ¿Temporal o final? |
|---|---|---|---|
| `data/resumen_crianzas.pkl` | 01_preparacion_datos.py | `ejecucion_vigente/data` | Temporal para pipeline interno | 
| `data/resumen_alimento.pkl` | 01_preparacion_datos.py | `ejecucion_vigente/data` | Temporal para pipeline interno | 
| `work_data/resumen_crianzas_para_modelo.{csv,xlsx}` | 02_consolidacion_datos.py | `ejecucion_vigente/work_data` | Temporal/intermedio | 
| `work_data/resumen_crianzas_para_proyeccion.{csv,xlsx}` | 03_inclusion_ventilacion_densidad.py | `ejecucion_vigente/work_data` | Entrada directa a modelo | 
| `work_data/resumen_crianzas_con_proyeccion.csv` | 04_proyeccion_ganancias.py | `ejecucion_vigente/work_data` | Resultado principal para compilados | 
| `proyeccion_pollos_expandido.xlsx`, `proyeccion_pollos_*.xlsx` | compilado_01.py / compilado_02.py | `ejecucion_vigente/compilado` | Reportes derivados | 

## 5. Acoplamientos Críticos
- Rutas absolutas detectadas:
  - `C:\repositorio_data\crianza_web_pollos_vigentes` y subcarpetas de origen de datos.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L97】
  - `C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_para_proyeccion.csv` en docstring de entrada.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L7-L11】
  - `C:\tecnoandina\f35_modelacion2\ejecucion_vigente\work_data\resumen_crianzas_con_proyeccion.csv` en compilados.【F:ejecucion_vigente/compilado/compilado_01.py†L16-L17】【F:ejecucion_vigente/compilado/compilado_02.py†L14-L15】
  - `C:\repositorio_data\crianza_web_pollos_vigentes\info_general` (estado actual de pabellones).【F:ejecucion_vigente/compilado/compilado_01.py†L18-L23】
- Credenciales/IPs en código:
  - IP MySQL `10.195.6.14`, usuario `usuario_lectura`, contraseña `Agro.2025#Read` embebidos en `query_database`.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】

## 6. Problemas Estructurales
- **CRÍTICOS:**
  - Dependencia de rutas absolutas Windows y estructura de archivos externos; impide ejecución fuera de entorno original.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L99】
  - Credenciales y IP de base de datos hardcodeadas en texto claro.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L27】
  - Falta de orquestador: `ejecutar_proyeccion.bat` solo ejecuta el paso 04, dejando dependencias manuales para 01-03.【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L22-L59】
- **RECOMENDADOS:**
  - Variables mágicas de filtrado de edades y densidad sin configuración externa.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L35】【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L49-L53】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L390-L398】
  - Repetición de utilidades `uniformar_strings` en varios scripts sin módulo compartido.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L9-L14】【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L7-L13】
  - Falta de manejo de errores/logging estructurado; print statements y raises genéricos.
- **OPCIONALES:**
  - Uso de `tqdm` importado pero no utilizado.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L2-L7】
  - Datos de ejemplo y reportes binarios mezclados en repositorio (`work_data`, imágenes de análisis).【F:analisis/modelo03/01_matriz_correlacion_limpia.png†L1-L1】

## 7. Resumen Ejecutivo
El pipeline actual es manual y frágil: depende de rutas absolutas y credenciales embebidas, carece de orquestación para los pasos 01-03 y mezcla lógica de ETL, consulta a bases, validación y predicción en scripts monolíticos. Los artefactos intermedios no tienen control de versiones ni validaciones consistentes, lo que limita la reproducibilidad y portabilidad del sistema.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L110】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L362-L437】

## 8. Árbol del Repositorio Relevante
```
ejecucion_vigente/
  crianzas_vigentes/
    01_preparacion_datos.py      # ETL inicial desde archivos SAP locales
    02_consolidacion_datos.py    # Cálculo de edades y merge alimentación
    03_inclusion_ventilacion_densidad.py # Enriquecimiento MySQL y densidad
    04_proyeccion_ganancias.py   # Validación y proyección con modelo 03
    ejecutar_proyeccion.bat      # Ejecuta solo el paso 04
  compilado/
    compilado_01.py              # Proyecciones extendidas, integra silos
    compilado_02.py              # Variante simplificada de compilado
  work_data/                     # CSV/XLSX intermedios y finales
analisis/
  modelo01|02|03/                # Artefactos de análisis y modelos .pkl
produccion/
  produccion01|produccion03/     # Scripts de predictor legados
```

## 9. Tabla Input → Transformación → Output (Nivel Función)
| Script | Input Exacto | Columnas Clave Usadas | Transformaciones (Lógica de negocio) | Output Exacto | Riesgos Detectados |
|---|---|---|---|---|---|
| 01_preparacion_datos.py | Excel/HTML en `cargado_pabellones`, `guias_alimento`, `mortalidad` bajo `C:\repositorio_data\...`.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L32-L97】 | `nombre_sector`, `nro_crianza`, `Fecha Guía`, `Cantidad Total`, `F.Guía`, `Edad`, `Cantidad` | Parseo de nombres de archivo para claves, normalización de strings, agrupación de mortalidad y alimento, cálculo de kilos per cápita acumulados.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L17-L105】 | `data/resumen_crianzas.pkl`, `data/resumen_alimento.pkl` | Rutas absolutas, sin validación de estructura de archivo, try/except silenciosos que omiten datos.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L46-L75】 |
| 02_consolidacion_datos.py | `data/resumen_crianzas.pkl`, `data/resumen_alimento.pkl`.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L19-L35】 | `Fecha Guía Inicio/Fin`, `Edad`, `nombre_sector_code`, `nro_crianza` | Cálculo de edad actual, filtrado de crianzas con edad media ≥32, merge de alimento a día 30 (ceil).【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L36】 | `work_data/resumen_crianzas_para_modelo.{csv,xlsx}` | Uso de fecha actual dinámica, criterio fijo 32 días, posible pérdida por merge left con Edad ceil.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L36】 |
| 03_inclusion_ventilacion_densidad.py | `work_data/resumen_crianzas_para_modelo.csv`; consultas MySQL con credenciales fijas.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L48】 | `nombre_sector_code`, `Pabellón`, `Cantidad Total`, `areaUtil`, `tipoConstruccion`, `edad_actual` | Merge con maestros de pabellones y sectores, cálculo de densidad (cantidad/area), imputación de tipo de construcción nulo a “Black Out”, filtro de edad 32-41 días.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L37-L53】 | `work_data/resumen_crianzas_para_proyeccion.{csv,xlsx}` | Credenciales expuestas; dependencia de base externa; no maneja errores de conexión; densidad puede ser NaN si areaUtil nula.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L53】 |
| 04_proyeccion_ganancias.py | `work_data/resumen_crianzas_para_proyeccion.csv`; modelo PyCaret en `analisis/modelo03/modelo_limpio_final`.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L32-L408】 | `mes_carga`, `sexo`, `kilos_recibidos_percapita`, `tipoConstruccion`, `densidad_pollos_m2` | Validación de columnas y valores, eliminación de nulos, mapeo `Sexo→sexo`, creación de features cíclicos y categorización de densidad, predicción y estadísticos finales.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L88-L337】 | `work_data/resumen_crianzas_con_proyeccion.csv` | Valores hardcodeados (sustituye “Sin Información” por “Black Out”, densidad negativa a 14.5), dependencias PyCaret; exclusión manual de sectores DON WILSON/EL CARMEN.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L377-L398】 |

## 10. Catálogo de Funciones Internas
| Archivo | Función | Propósito | ¿Es Pura? | ¿Candidata a mover a...? |
|---|---|---|---|---|
| 01_preparacion_datos.py | `uniformar_strings` | Normalizar strings removiendo acentos y símbolos.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L9-L14】 | Sí | Utils de texto |
| 01_preparacion_datos.py | `split_filename` | Extraer sector y crianza desde nombre de archivo por categoría.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L17-L29】 | Sí | Utils de parsing de archivos |
| 02_consolidacion_datos.py | `uniformar_strings` | Misma normalización de strings (duplicada).【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L7-L13】 | Sí | Utils de texto |
| 03_inclusion_ventilacion_densidad.py | `uniformar_strings` | Normalización de texto (tercera copia).【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L8-L13】 | Sí | Utils de texto |
| 03_inclusion_ventilacion_densidad.py | `query_database` | Ejecutar consultas MySQL con credenciales embebidas.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L29】 | No (efectos de E/S y credenciales) | Capa de acceso a datos con configuración externa |
| 04_proyeccion_ganancias.py | `validar_archivo_existe`, `cargar_datos`, `mapear_columnas`, `limpiar_datos_nulos`, `validar_columnas_requeridas`, `validar_valores`, `mostrar_estadisticas_input`, `preparar_features`, `realizar_proyeccion`, `agregar_columna_proyeccion`, `mostrar_estadisticas_proyeccion`, `guardar_resultado`, `mostrar_ejemplos`, `main` | Utilidades de validación, feature engineering, proyección y reporte. Varias producen salida por consola y accesos a disco/modelo.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L68-L466】 | Mixto (solo `preparar_features` es pura) | Separar en módulos de validación, features y orquestación |

## 11. Hardcoding y Reglas de Negocio
| Parámetro/Regla | Valor en Código | Archivo:Línea | Sugerencia de Parametrización |
|---|---|---|---|
| Ruta base de datos de origen | `C:\repositorio_data\crianza_web_pollos_vigentes` | 01_preparacion_datos.py:L32 | Variables de entorno o config YAML |
| Regenerar datos | `REGENERAR_DATOS = True` | 01_preparacion_datos.py:L32 | Flag configurable por CLI/env |
| Edad de proyección | `EDAD_PROYECCION = 30` | 02_consolidacion_datos.py:L16 | Configurable en archivo de parámetros |
| Filtro de edad criterio | `edad_criterio_proyeccion >= 32` | 02_consolidacion_datos.py:L28-L30 | Configurable y documentado |
| Filtro de edad 32-41 días | `(edad_actual >= 32) & (<=41)` | 03_inclusion_ventilacion_densidad.py:L48-L50 | Parametrizar rangos y justificar |
| Imputación tipo construcción | `np.where(isna, 'Black Out')` | 03_inclusion_ventilacion_densidad.py:L51-L52 | Configurable por catálogo externo |
| Reemplazo densidad negativa | `densidad_pollos_m2 < 0 → 14.5` | 04_proyeccion_ganancias.py:L396-L398 | Configuración o validación temprana |
| Exclusión de sectores | Filtra `['DON WILSON', 'EL CARMEN']` | 04_proyeccion_ganancias.py:L377 | Listado configurable |
| Rangos válidos | `mes_carga 1-12`, `kilos_recibidos_percapita 1-6`, `densidad_pollos_m2 9-50` | 04_proyeccion_ganancias.py:L57-L61 | Archivo de validaciones parametrizable |

## 12. Dependencias Cruzadas (Lineaje de Datos)
- Paso 01 crea columnas claves `nombre_sector_code`, `nro_crianza`, `Pabellón`, `Cantidad Total`, fechas y `kilos_recibidos_percapita`; estos sirven como llaves y métricas base para merges posteriores.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L64-L105】
- Paso 02 calcula `edad_actual`, `edad_proyeccion_dias`=30 y filtra por `edad_criterio_proyeccion`; además agrega `mes_carga` y `anio_carga` para estacionalidad, preparando la coincidencia con alimentación por edad.【F:ejecucion_vigente/crianzas_vigentes/02_consolidacion_datos.py†L16-L36】
- Paso 03 une con `maestrospabellones` para añadir `tipoConstruccion`, `areaUtil`, calcula `densidad_pollos_m2` (Cantidad Total / área) y filtra por edad 32-41; agrega zona geográfica desde `maestrossectorescrianza`.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L53】
- Paso 04 mapea `Sexo→sexo`, valida campos clave (`mes_carga`, `sexo`, `kilos_recibidos_percapita`, `tipoConstruccion`, `densidad_pollos_m2`), aplica features cíclicos y calcula `ganancia_proyectada` que luego es consumida por compilados para proyecciones por día/edad.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L88-L337】【F:ejecucion_vigente/compilado/compilado_01.py†L16-L113】

## 13. Hallazgos para el Refactor
1. **Externalizar configuración y credenciales**: mover rutas absolutas, IPs y rangos de validación a archivos de configuración o variables de entorno; centralizar conexión a MySQL.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L16-L53】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L390-L398】
2. **Modularizar utilidades**: extraer `uniformar_strings`, parsing de filenames y validadores a un paquete compartido para evitar duplicación y facilitar pruebas.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L9-L29】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L68-L209】
3. **Orquestación reproducible**: crear un runner (CLI/Makefile/Airflow) que ejecute secuencialmente 01→02→03→04 y gestione dependencias de entrada/salida, reemplazando el .bat actual que solo cubre el último paso.【F:ejecucion_vigente/crianzas_vigentes/ejecutar_proyeccion.bat†L22-L59】
4. **Separar lógica de negocio y E/S**: aislar lectura de fuentes (SAP, MySQL), transformaciones y modelado en capas; permitir pruebas unitarias puras para cálculos como densidad y features de proyección.【F:ejecucion_vigente/crianzas_vigentes/03_inclusion_ventilacion_densidad.py†L32-L53】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L234-L337】
5. **Validaciones consistentes y logging estructurado**: reemplazar prints por un logger configurable; capturar errores de conexión y formatos de archivo para evitar pérdidas silenciosas de datos.【F:ejecucion_vigente/crianzas_vigentes/01_preparacion_datos.py†L46-L75】【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L439-L457】
6. **Control de artefactos y versionado de modelos**: documentar versiones de `modelo_limpio_final.pkl`, mover artefactos grandes fuera del repo o a storage versionado, y parametrizar la ruta de modelo consumido por el paso 04.【F:ejecucion_vigente/crianzas_vigentes/04_proyeccion_ganancias.py†L36-L408】
