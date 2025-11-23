---
title: "02 – Arquitectura objetivo (v1)"
document_type: "arquitectura"
repo: "etlproject_birds"
created: "2025-11-22"
last_updated: "2025-11-22"
status: "v1-inicial"
confidence: "GREY"
notes: "Primera versión de arquitectura; define visión general centrada en modularidad ML sin implementación final."
---

# 02 – Arquitectura Objetivo (v1)

## Propósito
Establecer una arquitectura modular inicial para el repositorio, enfocada en organizar las funciones existentes sin reescribir la lógica. El objetivo es habilitar refactors progresivos, trazabilidad, colaboración IA y futura extensibilidad (modelos, pipelines, orquestación, deployments).

Esta versión define *dónde va cada cosa*, no *cómo se implementa* todavía.

---

## Principios base

1. **Separación clara de responsabilidades**
   - extracción vs transformación vs predicción vs persistencia.

2. **Modularidad**
   Cada módulo debe ser movible sin afectar los demás.

3. **Contratos explícitos**
   Entradas y salidas documentadas a nivel de módulo.

4. **Escalabilidad hacia ML**
   Debe permitir entrenamiento futuro, no solo inferencia.

5. **Compatibilidad con ejecución local y futura orquestación**
   `src/main.py` actúa como punto de entrada del pipeline.

---

## Estructura propuesta

```
src/
  main.py                 # entrypoint del flujo de predicción
  app/
    data/
      extractors/         # acceso a fuentes de datos (SQL/CSV/API)
      loaders/            # persistencia: datalake, CSV, parquet, DB
      processing/         # limpieza, normalización, merges
    ml/
      models/             # modelos predictivos e inferencia
      features/           # ingeniería de variables y cálculos derivados
    pipeline/             # orquestación de pasos y dependencias
    utils/                # helpers comunes (fecha, logs, validación)
```

---

## Rol de cada módulo

### `data/extractors/`
Responsable de obtener datos desde cualquier fuente (bases internas, endpoints, archivos, etc).  
No realiza cálculos ni genera features.

### `data/processing/`
Transforma datos crudos en tablas limpias y coherentes.

Ejemplos:
- merges entre fuentes
- imputaciones
- filtros
- casteo de tipos

### `data/loaders/`
Define cómo se exportan salidas:
- CSV / parquet
- datalake cliente
- bases operacionales

No incluye cálculos ni predicción.

### `ml/features/`
Encapsula reglas derivadas, cálculos de KPIs y columnas nuevas.

### `ml/models/`
Incluye wrappers de modelos, métodos `predict()` y eventualmente `fit()`.

### `pipeline/`
Secuencia de pasos que conectan módulos.  
Sirve como **contrato explícito** entre componentes, facilitando refactors futuros.

### `utils/`
Funciones de soporte no ligadas a lógica de negocio.

---

## Alcance de esta versión

Incluye:
- definición de estructura
- documentación de roles
- visión de modularización

No incluye aún:
- reubicación del código actual
- creación de tests
- diseño definitivo del pipeline
- contenedores o infraestructura

---

## Próximos pasos sugeridos

| Paso | Descripción | Resultado esperado |
|------|------------|-------------------|
| PR1 | Crear carpetas base sin mover lógica | Estructura vacía lista |
| PR2 | Extraer configuraciones hardcodeadas | `.env` + `settings.py` |
| PR3 | Mover funciones de extracción a `data/extractors` | Módulo inicial limpio |
| PR4 | Mover cálculos de features | Claridad entre datos y ML |
| PR5 | Crear primer pipeline (`pipeline/main_flow.py`) | Ejecución secuencial |
| PR6 | Agregar tests mínimos | Validación básica |

---

## Estado de madurez

| Módulo | Estado | Color |
|--------|--------|--------|
| extractors | Entendible pero sucio | GREY |
| processing | Lógica acoplada | BLACK |
| loaders | Parcial | GREY |
| features | Reglas implícitas | BLACK |
| models | Definido pero no modular | GREY |
| pipeline | Todavía no existe | BLACK |

Esta tabla evolucionará con cada PR.

---

_v1 lista. Modificar cuando mapeemos scripts reales._
