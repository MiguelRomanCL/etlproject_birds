---
generated_from_prompt: "./prompts/02_plan_refactor_incremental.md"
origen: "Gemini"
estado: "borrador"
contexto: "Basado en auditoría Codex ya integrada en dev"
---

# 02 – Plan Maestro de Refactorización Incremental

## 1. Visión y Objetivos
El objetivo de este refactor no es reescribir la lógica de negocio (que ya funciona), sino **reorganizarla** para garantizar:
1.  **Seguridad:** Eliminar credenciales y rutas absolutas del código fuente.
2.  **Modularidad:** Que el cambio en una regla de negocio (ej. edad de proyección) no requiera tocar 4 archivos distintos.
3.  **Escalabilidad:** Facilitar la integración futura de nuevos modelos o fuentes de datos.
4.  **Portabilidad:** Permitir que el proyecto se ejecute en cualquier máquina (Windows/Linux/Docker) sin depender de `C:\`.

## 2. Estrategia de Ejecución
Trabajaremos bajo el principio de **"Refactorización Segura"**:
* **Atomicidad:** Cada PR ataca una capa específica del problema.
* **Paridad Funcional:** El sistema debe seguir produciendo los mismos números que antes del refactor.
* **Valor Inmediato:** Cada paso debe dejar el repositorio en un estado mejor que el anterior.

---

## 3. Roadmap de PRs (Hoja de Ruta)

### 🏗️ PR 1: Cimientos y Estructura (Infraestructura)
**Objetivo:** Preparar el esqueleto del nuevo hogar para el código sin mover nada aún.
* **Cambios:**
    * Crear árbol de directorios vacío: `src/data`, `src/ml`, `src/pipeline`, `src/utils`.
    * Añadir `.gitignore` robusto (ignorar `__pycache__`, `.env`, `work_data/`).
    * Crear `requirements.txt` real basado en los imports detectados (pandas, sqlalchemy, pycaret, etc.).
* **Valor Ganado:** El proyecto ya parece profesional. Se establece el orden visual inmediato.

### 🔐 PR 2: Desintoxicación y Configuración (Safety First)
**Objetivo:** Extraer todo lo que impide que el código corra en otra máquina (Hardcoding).
* **Cambios:**
    * Implementar `src/config.py` usando `python-dotenv`.
    * Crear `.env.example` documentando las variables requeridas.
    * **Migración:**
        * Rutas `C:\repositorio_data\...` → Variables `RAW_DATA_PATH`.
        * Credenciales MySQL (`Agro.2025#Read`) → Variables `DB_USER`, `DB_PASS`.
        * Parámetros Mágicos (`EDAD_PROYECCION=30`, `DENSIDAD_DEFAULT=14.5`) → Constantes en `config.py`.
    * Actualizar scripts vigentes (`01` a `04`) para leer de `config.py` en lugar de texto plano.
* **Valor Ganado:** Seguridad inmediata. El código se vuelve portable. Se elimina el riesgo de filtrar contraseñas.

### 🛠️ PR 3: Utilidades Compartidas (DRY - Don't Repeat Yourself)
**Objetivo:** Eliminar código duplicado detectado en la auditoría.
* **Cambios:**
    * Mover `uniformar_strings` (repetida en 3 scripts) a `src/utils/text_ops.py`.
    * Mover `split_filename` a `src/utils/file_ops.py`.
    * Refactorizar scripts `01`, `02`, `03` para importar estas funciones.
* **Valor Ganado:** Reducción de deuda técnica. Si hay que mejorar la limpieza de texto, se hace en un solo lugar.

### 📥 PR 4: Capa de Extracción (Data Extractors)
**Objetivo:** Centralizar el "cómo obtengo los datos" separándolo del "qué hago con ellos".
* **Cambios:**
    * Crear `src/data/extractors/sap_reader.py`: Mover lógica de lectura de Excel de `01_preparacion_datos.py`.
    * Crear `src/data/extractors/db_client.py`: Mover lógica de conexión MySQL y queries de `03_inclusion...py`.
* **Valor Ganado:** Claridad total sobre las fuentes de datos. Se facilita el testeo (podemos simular la BD sin conectarnos a la real).

### ⚙️ PR 5: Transformación y Limpieza (Data Processing)
**Objetivo:** Aislar la lógica de negocio y limpieza de datos.
* **Cambios:**
    * Crear `src/data/transform/cleaners.py`: Lógica de imputación (Black Out, Densidad 14.5).
    * Crear `src/data/transform/mergers.py`: Lógica de cruce de tablas (Mortalidad, Alimento).
    * Refactorizar `02_consolidacion_datos.py` para usar estos módulos.
* **Valor Ganado:** La lógica de negocio se vuelve explícita y testeable. Se separa "limpiar" de "calcular".

### 🧠 PR 6: Inteligencia y Predicción (ML Layer)
**Objetivo:** Encapsular el modelo como un servicio, no como un script suelto.
* **Cambios:**
    * Crear clase `Predictor` en `src/ml/inference.py`.
    * Mover validaciones de rangos (feature engineering) de `04_proyeccion_ganancias.py` a `src/ml/features.py`.
    * Hacer que la carga del `.pkl` sea configurable.
* **Valor Ganado:** Control total sobre el modelo. Prepara el terreno para exponer el modelo como API o librería.

### 🚀 PR 7: El Nuevo Cerebro (Pipeline & Entrypoint)
**Objetivo:** Reemplazar el `.bat` y los scripts manuales por un orquestador pythonico.
* **Cambios:**
    * Crear `src/pipeline/main_flow.py`: Función que llama secuencialmente a Extract → Transform → Predict.
    * Crear `main.py` (CLI): Punto de entrada único (`python main.py --run-all`).
* **Valor Ganado:** Ejecución en un solo comando. Independencia del sistema operativo (Adiós `.bat`).

---

## 4. Estado de Progreso Visual

| PR | Módulo | Estado | Valor para el Negocio |
| :--- | :--- | :--- | :--- |
| **01** | **Estructura** | ⬜ Pendiente | Organización profesional visible. |
| **02** | **Config (Hardcoding)** | ⬜ Pendiente | **Seguridad y Portabilidad.** (Crítico) |
| **03** | **Utils (Duplicados)** | ⬜ Pendiente | Mantenibilidad y limpieza. |
| **04** | **Extractors (Inputs)** | ⬜ Pendiente | Control de fuentes de datos. |
| **05** | **Transform (Lógica)** | ⬜ Pendiente | Reglas de negocio claras. |
| **06** | **ML (Modelos)** | ⬜ Pendiente | Estandarización de predicciones. |
| **07** | **Pipeline (Orquestación)**| ⬜ Pendiente | Automatización robusta. |