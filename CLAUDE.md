# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a poultry farming data modeling project (`f35_modelacion2`) for Tecnoandina, focused on predicting **ganancia_promedio_gramos** (average weight gain in grams) for poultry breeding operations. The project includes advanced clustering analysis to determine whether specialized models per cluster outperform a single global model.

## Environment Setup

**Virtual Environment:**
- Python virtual environment is located in `.venv/`
- Activate with: `.venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Unix)

**Root Dependencies** (requirements.txt):
```bash
scipy
matplotlib
scikit-learn
```

**Install root dependencies:**
```bash
pip install -r requirements.txt
```

## Project Structure

```
f35_modelacion2/
├── .venv/              # Python virtual environment (git-ignored)
├── data/               # Raw data directory (empty)
├── work_data/          # Working datasets (git-ignored)
│   └── resumen_crianzas_para_modelo2.csv/xlsx
├── analisis/           # Analysis modules
│   ├── clusterizacion/     # Clustering analysis (full version)
│   ├── clusterizacion2/    # Simplified clustering analysis
│   └── modelo01/           # PyCaret modeling (has dependency conflicts)
└── requirements.txt    # Root dependencies
```

## Data

**Location:** `work_data/resumen_crianzas_para_modelo2.csv` / `.xlsx`

**Target Variable:** `ganancia_promedio_gramos` (average weight gain in grams)

**Features:**
- **Identifiers:** nombre_sector_code, nro_crianza, nro_pabellon
- **Temporal:** mes_carga, edad_madres_dias, edad_proyeccion_dias
- **Performance:** peso_inicial_gramos, kilos_recibidos_percapita
- **Categorical:** sexo (HEMBRA/MACHO), tipoConstruccion (Tradicional/Transversal/Black Out)
- **Operational:** densidad_pollos_m2

## Clustering Analysis Module

**Location:** `analisis/clusterizacion/`

### Purpose
Determines if creating separate models per cluster improves predictions vs. a single global model.

### Quick Start (Windows)
```bash
cd analisis/clusterizacion
# Double-click or run:
ejecutar_analisis.bat
```

### Manual Execution
```bash
cd analisis/clusterizacion
pip install -r requirements.txt
python analisis_clusterizacion_avanzado.py
```

### Strategies Evaluated
1. **Modelo Único** - Single baseline model
2. **Por Sexo** - Separate models for HEMBRA/MACHO
3. **Por Densidad** - Models per density level (pollos/m²)
4. **Por Tipo Construcción** - Models per construction type
5. **Por Sector** - Models per geographical sector
6. **K-Means** - Automatic clustering (optimal K)
7. **Hierarchical** - Hierarchical clustering
8. **DBSCAN** - Density-based clustering

### Key Files

**Documentation:**
- `README.md` - Complete technical documentation
- `GUIA_RAPIDA.md` - Quick start guide with decision criteria
- `INDICE.md` - File index and navigation

**Scripts:**
- `analisis_clusterizacion_avanzado.py` - Main analysis script (3-10 min runtime)
- `ejecutar_analisis.bat` - Windows batch automation
- `requirements.txt` - Analysis-specific dependencies

**Generated Outputs:**
- `REPORTE_CLUSTERIZACION.md` - Executive report with recommendations
- `comparacion_estrategias.png` - Visual comparison (MAE, RMSE, R², CV MAE)
- `kmeans_metricas.png` - K-Means optimization metrics
- `visualizacion_clusters.png` - PCA cluster visualization
- `dendrograma.png` - Hierarchical dendrogram
- `comparacion_estrategias.csv` - Comparative table
- `resultados_detallados.json` - Detailed results in JSON
- `dataset_con_clusters.csv` - Dataset with cluster assignments

### Key Metrics

**Model Performance:**
- **MAE** (Mean Absolute Error) - Primary metric, lower is better
- **RMSE** (Root Mean Squared Error) - Penalizes large errors
- **R²** - Variance explained (higher is better)
- **CV MAE** - Cross-validated MAE (5-fold)

**Clustering Quality:**
- **Silhouette Score** - Cluster separation (-1 to 1, >0.5 is good)
- **Davies-Bouldin** - Intra/inter cluster ratio (lower is better)
- **Calinski-Harabasz** - Variance ratio (higher is better)
- **ANOVA p-value** - Statistical significance (<0.05 indicates significant differences)

### Decision Criteria

**✅ Use Clustering if:**
- Improvement > 5% vs baseline
- ANOVA p-value < 0.05 (significant differences)
- Silhouette Score > 0.5 (well-defined clusters)

**⚠️ Evaluate Trade-off if:**
- Improvement 1-5% (marginal benefit)
- High operational complexity
- Limited maintenance resources

**❌ Maintain Single Model if:**
- Improvement < 1% or negative
- ANOVA p-value > 0.05 (no significant differences)
- Silhouette < 0.3 (poorly defined clusters)

## Development Workflow

### Running Clustering Analysis
```bash
# Windows - automated
cd analisis/clusterizacion
ejecutar_analisis.bat

# Manual - all platforms
cd analisis/clusterizacion
pip install -r requirements.txt
python analisis_clusterizacion_avanzado.py
```

### Interpreting Results
1. Review `REPORTE_CLUSTERIZACION.md` for executive summary
2. Check improvement percentage vs baseline
3. Examine `comparacion_estrategias.png` for visual comparison
4. Follow decision criteria based on metrics

### Modifying Analysis Parameters

**K-Means range** (analisis_clusterizacion_avanzado.py:138):
```python
k_range = range(2, 15)  # Test K from 2 to 14
```

**DBSCAN parameters** (analisis_clusterizacion_avanzado.py:208):
```python
dbscan = DBSCAN(eps=3.0, min_samples=10)
```

**Prediction model** (analisis_clusterizacion_avanzado.py:275):
```python
rf = RandomForestRegressor(n_estimators=100, random_state=42)
```

## Simplified Clustering Analysis Module

**Location:** `analisis/clusterizacion2/`

A simplified version that focuses only on the 3 main variables: Sexo, Densidad (pollos/m²), and Tipo de Construcción.

### Running Simplified Analysis
```bash
cd analisis/clusterizacion2
pip install -r requirements.txt  # If exists
python analisis_clusterizacion_simplificado.py
```

## PyCaret Modeling Module (⚠️ Dependency Conflicts)

**Location:** `analisis/modelo01/`

**⚠️ IMPORTANT:** PyCaret has strict version requirements that conflict with other modules:
- Requires: numpy<1.27, pandas<2.2.0, scipy<=1.11.4, matplotlib<3.8.0
- Downgrades: numpy 2.3→1.26, pandas 2.3→2.1, scipy 1.16→1.11, matplotlib 3.10→3.7

**Recommendation:** Use a separate virtual environment for PyCaret-based analysis.

### Running PyCaret Analysis (Isolated Environment)
```bash
# Create isolated environment
python -m venv .venv_pycaret
.venv_pycaret\Scripts\activate  # Windows
pip install pycaret
cd analisis/modelo01
python analisis_modelamiento_pycaret.py
```

### Files in modelo01
- `analisis_modelamiento_pycaret.py` - Main PyCaret modeling script
- `README.md` - Documentation
- `GUIA_RAPIDA.md` - Quick start guide
- `requirements.txt` - Dependencies (conflicts with main venv)

## Common Commands

**Install root dependencies:**
```bash
pip install -r requirements.txt
```

**Run clustering analysis (full):**
```bash
cd analisis/clusterizacion
pip install -r requirements.txt
python analisis_clusterizacion_avanzado.py
# Or: ejecutar_analisis.bat (Windows)
```

**Run clustering analysis (simplified):**
```bash
cd analisis/clusterizacion2
python analisis_clusterizacion_simplificado.py
```

**View results:**
```bash
# Clustering reports
code analisis/clusterizacion/REPORTE_CLUSTERIZACION.md
code analisis/clusterizacion2/REPORTE_CLUSTERIZACION.md

# PyCaret report (if run)
code analisis/modelo01/REPORTE_ANALISIS.md
```

## Troubleshooting

### PyCaret Dependency Conflicts

**Problem:** Installing PyCaret downgrades numpy, pandas, scipy, matplotlib to older versions incompatible with other analysis scripts.

**Solution 1 - Isolated Environment (Recommended):**
```bash
# Create separate venv for PyCaret
python -m venv .venv_pycaret
.venv_pycaret\Scripts\activate
pip install pycaret
python analisis/modelo01/analisis_modelamiento_pycaret.py
```

**Solution 2 - Reinstall After PyCaret:**
```bash
# After running PyCaret analysis, reinstall newer versions
pip install --upgrade numpy pandas scipy matplotlib scikit-learn
```

**Solution 3 - Use Clustering Analysis Instead:**
The clustering analysis modules (`clusterizacion/` and `clusterizacion2/`) provide comprehensive model comparison without PyCaret dependency conflicts.

### JSON Serialization Errors (NumPy Types)

Both `clusterizacion2/analisis_clusterizacion_simplificado.py` and similar scripts have been fixed to convert NumPy types (int32, int64, float64) to Python native types before JSON serialization using a `convert_to_native()` helper function.
