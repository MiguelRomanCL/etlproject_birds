---
origen: "Codex"
fecha: "2025-11-22"
rama_origen: "codex/generate-technical-audit-report-for-legacy-code"
documento_relacionado: "../01_estado_actual.md"
proposito: "Generar auditoría técnica inicial del repositorio monolítico"
estado: "vigente"
---
**Actúa como un Arquitecto de Software Senior especializado en Refactoring de Legacy Code.**

Tu objetivo es realizar una **Auditoría Técnica Profunda** de todo el repositorio actual. Necesito que generes el contenido para un archivo llamado `docs/01_estado_actual.md`.

**CONTEXTO:**
Este repositorio es un sistema "legacy" de predicción avícola. Está desordenado, tiene alto acoplamiento, rutas hardcodeadas y lógica mezclada. Queremos refactorizarlo a una arquitectura modular, pero antes necesitamos una radiografía exacta de lo que existe.

**INSTRUCCIONES DE EJECUCIÓN:**

1. Escanea recursivamente las carpetas: `ejecucion_vigente/`, `produccion/`, `analisis/`, `compilado/`.
2. No inventes nada. Si una función es confusa, márcala como "REQUIERE REVISIÓN".
3. Genera un reporte en Markdown que contenga **EXACTAMENTE** las siguientes 13 secciones. Sé exhaustivo.

---

### ESTRUCTURA DEL REPORTE A GENERAR (`docs/01_estado_actual.md`):

**1. Entry Points y Flujo Principal**

- Identifica el script `04_proyeccion_ganancias.py` y el `.bat`.
- Describe la secuencia de ejecución real detectada (quién llama a quién o el orden lógico 01->02->03->04).

**2. Inventario de Scripts (Análisis por Archivo)**

- Analiza `01_preparacion_datos.py`, `02_consolidacion_datos.py`, `03_inclusion_ventilacion_densidad.py`, `04_proyeccion_ganancias.py`.
- Para cada uno detalla: Ubicación, Rutas que lee (Inputs), Lógica principal, Rutas que escribe (Outputs) y Librerías externas que usa.

**3. Modelos y Artefactos**

- Localiza dónde están los `.pkl` de modelos (ej: `analisis/modelo03/...`).
- Identifica en qué línea de código se cargan (`load_model`, `pickle.load`).

**4. Mapa de Datos (Inputs/Outputs)**

- Crea una tabla con: Archivo Generado | Script Creador | Ruta Destino | ¿Es temporal o final?

**5. Acoplamientos Críticos**

- Lista explícita de rutas absolutas detectadas (ej: `C:\...`).
- Lista de credenciales o IPs detectadas en el código.

**6. Problemas Estructurales**

- Clasifícalos en: CRÍTICOS (impiden ejecución en otro PC), RECOMENDADOS (malas prácticas), OPCIONALES.

**7. Resumen Ejecutivo**

- Breve conclusión del estado de salud del repo.

**8. Árbol del Repositorio Relevante**

- Genera un árbol de texto del directorio.
- Añade comentarios al lado de los archivos clave explicando qué hacen (ej: `predictor.py # Clase duplicada de predicción`).

**9. Tabla Input → Transformación → Output (Nivel Función)**

- Esta es la sección más importante. Para cada script principal, crea una tabla:
- | Script | Input Exacto (Tablas/Archivos) | Columnas Clave Usadas | Transformaciones (Lógica de negocio) | Output Exacto | Riesgos Detectados |

**10. Catálogo de Funciones Internas**

- Lista todas las funciones `def` encontradas en los scripts.
- | Archivo | Función | Propósito | ¿Es Pura? | ¿Candidata a mover a...? (Extract/Transform/Utils) |

**11. Hardcoding y Reglas de Negocio**

- Escanea el código buscando "números mágicos" (ej: `if edad > 30`, `densidad = 14.5`).
- | Parámetro/Regla | Valor en Código | Archivo:Línea | Sugerencia de Parametrización |

**12. Dependencias Cruzadas (Lineaje de Datos)**

- Explica cómo fluyen los datos. Ej: "El script 01 crea la columna 'edad', el script 02 la filtra, el script 03 la usa para unir con 'densidad'".

**13. Hallazgos para el Refactor**

- Lista priorizada de qué debemos atacar primero basándote en la evidencia anterior.

---

**FORMATO DE SALIDA:**
Devuélveme **únicamente** el bloque de código Markdown listo para ser guardado en `docs/01_estado_actual.md`.

# P2

### Registro de Mejora de Prompt: Auditoría Técnica

**Diferencias clave**

- **Unificación:** La versión nueva consolida las instrucciones iniciales y la "extensión" posterior en un solo bloque coherente, eliminando la necesidad de que la IA concatene contextos previos.
- **Rol Específico:** Define explícitamente el rol de "Arquitecto de Software Senior", elevando el estándar del lenguaje técnico esperado.
- **Estructura de Salida:** Pasa de pedir "listas" o "descripciones" (versión antigua) a exigir **tablas comparativas** específicas (Inputs/Outputs, Funciones, Hardcoding) y formatos estrictos.
- **Profundidad de Escaneo:** La nueva versión ordena explícitamente un escaneo recursivo y la detección de "Lineaje de Datos" (flujo de información entre scripts), algo ausente en la primera iteración.

**Por qué es mejor**

- **Reducción de Alucinaciones:** Al exigir evidencias específicas (número de línea, archivo exacto) y tablas, fuerza a la IA a verificar el código en lugar de generar resúmenes genéricos.
- **Accionabilidad:** La salida estructurada en tablas permite identificar patrones de refactorización (ej. funciones duplicadas) de un vistazo, facilitando la creación del plan de migración.
- **Exhaustividad:** Resuelve el problema de la fragmentación de instrucciones, asegurando que ninguna sección crítica (como los parámetros hardcodeados) se omita por "olvido" del contexto anterior.

**Riesgos o Tradeoffs**

- **Longitud de Respuesta:** La nueva versión solicitará una salida muy extensa. Existe el riesgo de que la respuesta se corte si el modelo tiene un límite de tokens de salida bajo.
- **Rigidez:** Si el repositorio no tiene cierta estructura (ej. no tiene modelos), la IA podría forzar explicaciones vacías para cumplir con las 13 secciones obligatorias.

**Recomendación finalAdoptar la nueva versión tal cual.** La estructura rígida es necesaria dado el estado "desordenado" del repositorio. La ganancia en precisión técnica supera el riesgo de longitud (el cual se soluciona pidiendo a la IA que continúe si se corta).