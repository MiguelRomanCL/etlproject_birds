"""
ANÁLISIS EXHAUSTIVO DE CLUSTERIZACIÓN PARA MODELOS PREDICTIVOS
================================================================

Este script analiza si es conveniente crear modelos separados por clusters
en lugar de un modelo único para predecir ganancia_promedio_gramos.

Estrategias evaluadas:
1. Modelo único (baseline)
2. Modelos por sexo
3. Modelos por densidad_pollos_m2
4. Modelos por tipoConstruccion
5. Modelos por clusters de sectores
6. Clustering automático (K-Means, DBSCAN, Hierarchical)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')

# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Modelado
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

# Estadística
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform

# Otros
import json
from datetime import datetime
from pathlib import Path

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

DATA_PATH = r'C:\tecnoandina\f35_modelacion2\work_data\resumen_crianzas_para_modelo2.csv'
OUTPUT_DIR = Path(r'C:\tecnoandina\f35_modelacion2\analisis\clusterizacion')
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# ==============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==============================================================================

print("=" * 80)
print("ANÁLISIS EXHAUSTIVO DE CLUSTERIZACIÓN")
print("=" * 80)
print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("1. Cargando datos...")
df = pd.read_csv(DATA_PATH)
print(f"   ✓ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

# Preparar variables
features_numericas = ['mes_carga', 'edad_madres_dias', 'peso_inicial_gramos', 
                      'kilos_recibidos_percapita', 'densidad_pollos_m2']
features_categoricas = ['sexo', 'tipoConstruccion', 'nombre_sector_code']
target = 'ganancia_promedio_gramos'

# Codificar variables categóricas
df_encoded = df.copy()
le_dict = {}
for col in features_categoricas:
    le = LabelEncoder()
    df_encoded[f'{col}_encoded'] = le.fit_transform(df[col])
    le_dict[col] = le

print(f"\n2. Variables identificadas:")
print(f"   • Numéricas: {len(features_numericas)}")
print(f"   • Categóricas: {len(features_categoricas)}")
print(f"   • Target: {target}")

# ==============================================================================
# 2. ANÁLISIS EXPLORATORIO DE GRUPOS NATURALES
# ==============================================================================

print("\n" + "=" * 80)
print("2. ANÁLISIS DE GRUPOS NATURALES")
print("=" * 80)

def analizar_grupo(df, grupo_col, grupo_nombre):
    """Analiza estadísticas por grupo"""
    print(f"\n   📊 {grupo_nombre}:")
    
    grupos = df.groupby(grupo_col)[target].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    print(grupos.to_string())
    
    # ANOVA
    grupos_data = [group[target].values for name, group in df.groupby(grupo_col)]
    f_stat, p_value = stats.f_oneway(*grupos_data)
    
    print(f"\n   ANOVA: F-statistic={f_stat:.4f}, p-value={p_value:.6f}")
    if p_value < 0.05:
        print(f"   ✓ Diferencias SIGNIFICATIVAS entre grupos (p < 0.05)")
    else:
        print(f"   ✗ NO hay diferencias significativas (p >= 0.05)")
    
    return grupos, f_stat, p_value

# Analizar cada estrategia
resultados_grupos = {}

resultados_grupos['sexo'] = analizar_grupo(df, 'sexo', 'SEXO')
resultados_grupos['densidad'] = analizar_grupo(df, 'densidad_pollos_m2', 'DENSIDAD (pollos/m²)')
resultados_grupos['tipo_construccion'] = analizar_grupo(df, 'tipoConstruccion', 'TIPO DE CONSTRUCCIÓN')
resultados_grupos['sector'] = analizar_grupo(df, 'nombre_sector_code', 'SECTOR')

# ==============================================================================
# 3. CLUSTERING AUTOMÁTICO
# ==============================================================================

print("\n" + "=" * 80)
print("3. CLUSTERING AUTOMÁTICO (MÉTODOS AVANZADOS)")
print("=" * 80)

# Preparar datos para clustering
X_clustering = df_encoded[features_numericas + [f'{col}_encoded' for col in features_categoricas]].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clustering)

# 3.1 K-Means con búsqueda del K óptimo
print("\n   🔍 K-Means Clustering:")
inertias = []
silhouettes = []
davies_bouldin = []
calinski = []

k_range = range(2, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))
    davies_bouldin.append(davies_bouldin_score(X_scaled, labels))
    calinski.append(calinski_harabasz_score(X_scaled, labels))

# Encontrar K óptimo
optimal_k_silhouette = k_range[np.argmax(silhouettes)]
optimal_k_db = k_range[np.argmin(davies_bouldin)]

print(f"   • K óptimo (Silhouette): {optimal_k_silhouette} (score={max(silhouettes):.3f})")
print(f"   • K óptimo (Davies-Bouldin): {optimal_k_db} (score={min(davies_bouldin):.3f})")

# Aplicar K-Means con K óptimo
kmeans_final = KMeans(n_clusters=optimal_k_silhouette, random_state=RANDOM_STATE, n_init=10)
df['cluster_kmeans'] = kmeans_final.fit_predict(X_scaled)

print(f"\n   Distribución de clusters K-Means:")
print(df['cluster_kmeans'].value_counts().sort_index().to_string())

# 3.2 Clustering Jerárquico
print(f"\n   🔍 Hierarchical Clustering:")
linkage_matrix = linkage(X_scaled, method='ward')
hierarchical = AgglomerativeClustering(n_clusters=optimal_k_silhouette, linkage='ward')
df['cluster_hierarchical'] = hierarchical.fit_predict(X_scaled)

print(f"   Distribución de clusters Hierarchical:")
print(df['cluster_hierarchical'].value_counts().sort_index().to_string())

# 3.3 DBSCAN
print(f"\n   🔍 DBSCAN Clustering:")
dbscan = DBSCAN(eps=2.0, min_samples=5)
df['cluster_dbscan'] = dbscan.fit_predict(X_scaled)

n_clusters_dbscan = len(set(df['cluster_dbscan'])) - (1 if -1 in df['cluster_dbscan'] else 0)
n_noise = list(df['cluster_dbscan']).count(-1)

print(f"   • Clusters encontrados: {n_clusters_dbscan}")
print(f"   • Puntos de ruido: {n_noise}")

# ==============================================================================
# 4. MODELADO Y COMPARACIÓN DE ESTRATEGIAS
# ==============================================================================

print("\n" + "=" * 80)
print("4. EVALUACIÓN DE ESTRATEGIAS DE MODELADO")
print("=" * 80)

def evaluar_estrategia(df, estrategia_nombre, grupo_col=None, n_folds=5):
    """
    Evalua una estrategia de modelado (único o por clusters)
    """
    print(f"\n   📈 Evaluando: {estrategia_nombre}")
    print(f"   " + "-" * 60)
    
    # Preparar features
    X = df[features_numericas].copy()
    
    # Agregar variables categóricas codificadas
    for col in features_categoricas:
        X[f'{col}_encoded'] = df_encoded[f'{col}_encoded']
    
    y = df[target]
    
    resultados = {
        'estrategia': estrategia_nombre,
        'n_modelos': 1 if grupo_col is None else df[grupo_col].nunique(),
        'metricas': []
    }
    
    if grupo_col is None:
        # MODELO ÚNICO
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=RANDOM_STATE
        )
        
        # RandomForest
        rf = RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(rf, X, y, cv=n_folds, 
                                    scoring='neg_mean_absolute_error', n_jobs=-1)
        cv_mae = -cv_scores.mean()
        cv_std = cv_scores.std()
        
        resultados['metricas'].append({
            'grupo': 'ÚNICO',
            'n_samples_train': len(X_train),
            'n_samples_test': len(X_test),
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'cv_mae': cv_mae,
            'cv_std': cv_std
        })
        
        print(f"   • Modelo Único:")
        print(f"     - MAE: {mae:.4f}")
        print(f"     - RMSE: {rmse:.4f}")
        print(f"     - R²: {r2:.4f}")
        print(f"     - CV MAE: {cv_mae:.4f} (±{cv_std:.4f})")
        
    else:
        # MODELOS POR CLUSTER/GRUPO
        grupos = df[grupo_col].unique()
        
        maes = []
        rmses = []
        r2s = []
        cv_maes = []
        
        for grupo in sorted(grupos):
            if grupo == -1:  # Skip noise in DBSCAN
                continue
                
            df_grupo = df[df[grupo_col] == grupo].copy()
            
            if len(df_grupo) < 30:  # Skip grupos muy pequeños
                continue
            
            X_grupo = df_grupo[features_numericas].copy()
            for col in features_categoricas:
                X_grupo[f'{col}_encoded'] = df_encoded.loc[df_grupo.index, f'{col}_encoded']
            
            y_grupo = df_grupo[target]
            
            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X_grupo, y_grupo, test_size=0.2, random_state=RANDOM_STATE
            )
            
            # Modelo
            rf = RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            # CV solo si hay suficientes muestras
            if len(X_grupo) >= 50:
                cv_scores = cross_val_score(rf, X_grupo, y_grupo, cv=min(3, len(X_grupo)//10), 
                                          scoring='neg_mean_absolute_error', n_jobs=-1)
                cv_mae = -cv_scores.mean()
            else:
                cv_mae = mae
            
            maes.append(mae)
            rmses.append(rmse)
            r2s.append(r2)
            cv_maes.append(cv_mae)
            
            resultados['metricas'].append({
                'grupo': str(grupo),
                'n_samples_train': len(X_train),
                'n_samples_test': len(X_test),
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'cv_mae': cv_mae
            })
        
        # Resumen agregado
        mae_promedio = np.mean(maes)
        rmse_promedio = np.mean(rmses)
        r2_promedio = np.mean(r2s)
        cv_mae_promedio = np.mean(cv_maes)
        
        print(f"   • {len(grupos)} Modelos Separados:")
        print(f"     - MAE promedio: {mae_promedio:.4f}")
        print(f"     - RMSE promedio: {rmse_promedio:.4f}")
        print(f"     - R² promedio: {r2_promedio:.4f}")
        print(f"     - CV MAE promedio: {cv_mae_promedio:.4f}")
        
        resultados['mae_agregado'] = mae_promedio
        resultados['rmse_agregado'] = rmse_promedio
        resultados['r2_agregado'] = r2_promedio
        resultados['cv_mae_agregado'] = cv_mae_promedio
    
    return resultados

# Evaluar todas las estrategias
estrategias_resultados = []

# Baseline: Modelo único
estrategias_resultados.append(
    evaluar_estrategia(df, "1. MODELO ÚNICO (Baseline)", grupo_col=None)
)

# Por sexo
estrategias_resultados.append(
    evaluar_estrategia(df, "2. MODELOS POR SEXO", grupo_col='sexo')
)

# Por densidad
estrategias_resultados.append(
    evaluar_estrategia(df, "3. MODELOS POR DENSIDAD", grupo_col='densidad_pollos_m2')
)

# Por tipo construcción
estrategias_resultados.append(
    evaluar_estrategia(df, "4. MODELOS POR TIPO CONSTRUCCIÓN", grupo_col='tipoConstruccion')
)

# Por sector
estrategias_resultados.append(
    evaluar_estrategia(df, "5. MODELOS POR SECTOR", grupo_col='nombre_sector_code')
)

# Por K-Means
estrategias_resultados.append(
    evaluar_estrategia(df, f"6. MODELOS POR K-MEANS (k={optimal_k_silhouette})", 
                      grupo_col='cluster_kmeans')
)

# Por Hierarchical
estrategias_resultados.append(
    evaluar_estrategia(df, f"7. MODELOS POR HIERARCHICAL (k={optimal_k_silhouette})", 
                      grupo_col='cluster_hierarchical')
)

# ==============================================================================
# 5. COMPARACIÓN Y RANKING DE ESTRATEGIAS
# ==============================================================================

print("\n" + "=" * 80)
print("5. RANKING DE ESTRATEGIAS")
print("=" * 80)

# Crear tabla comparativa
comparacion = []
for resultado in estrategias_resultados:
    if resultado['n_modelos'] == 1:
        # Modelo único
        metricas = resultado['metricas'][0]
        comparacion.append({
            'Estrategia': resultado['estrategia'],
            'N_Modelos': resultado['n_modelos'],
            'MAE': metricas['mae'],
            'RMSE': metricas['rmse'],
            'R²': metricas['r2'],
            'CV_MAE': metricas['cv_mae']
        })
    else:
        # Modelos múltiples
        comparacion.append({
            'Estrategia': resultado['estrategia'],
            'N_Modelos': resultado['n_modelos'],
            'MAE': resultado['mae_agregado'],
            'RMSE': resultado['rmse_agregado'],
            'R²': resultado['r2_agregado'],
            'CV_MAE': resultado['cv_mae_agregado']
        })

df_comparacion = pd.DataFrame(comparacion)
df_comparacion = df_comparacion.sort_values('MAE')

print("\n   📊 TABLA COMPARATIVA (ordenado por MAE):\n")
print(df_comparacion.to_string(index=False))

# Determinar la mejor estrategia
mejor_estrategia = df_comparacion.iloc[0]

print("\n" + "=" * 80)
print("6. RECOMENDACIÓN FINAL")
print("=" * 80)

print(f"\n   🏆 MEJOR ESTRATEGIA: {mejor_estrategia['Estrategia']}")
print(f"\n   Métricas:")
print(f"   • MAE: {mejor_estrategia['MAE']:.4f}")
print(f"   • RMSE: {mejor_estrategia['RMSE']:.4f}")
print(f"   • R²: {mejor_estrategia['R²']:.4f}")
print(f"   • Número de modelos: {int(mejor_estrategia['N_Modelos'])}")

# Calcular mejora respecto al baseline
baseline_mae = df_comparacion[df_comparacion['Estrategia'].str.contains('ÚNICO')]['MAE'].values[0]
mejora_porcentual = ((baseline_mae - mejor_estrategia['MAE']) / baseline_mae) * 100

print(f"\n   📈 Mejora vs Baseline: {mejora_porcentual:.2f}%")

if mejora_porcentual > 5:
    print(f"\n   ✅ RECOMENDACIÓN: Usar clusterización ({mejor_estrategia['Estrategia']})")
    print(f"      La mejora de {mejora_porcentual:.2f}% justifica la complejidad adicional.")
elif mejora_porcentual > 0:
    print(f"\n   ⚠️  PRECAUCIÓN: Mejora marginal de {mejora_porcentual:.2f}%")
    print(f"      Considerar si la complejidad adicional vale la pena.")
else:
    print(f"\n   ❌ RECOMENDACIÓN: Mantener modelo único")
    print(f"      No hay mejora significativa con clusterización.")

# ==============================================================================
# 7. VISUALIZACIONES
# ==============================================================================

print("\n" + "=" * 80)
print("7. GENERANDO VISUALIZACIONES")
print("=" * 80)

# 7.1 Gráfico de comparación de estrategias
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# MAE
axes[0, 0].barh(df_comparacion['Estrategia'], df_comparacion['MAE'], color='steelblue')
axes[0, 0].set_xlabel('MAE')
axes[0, 0].set_title('Mean Absolute Error por Estrategia')
axes[0, 0].invert_yaxis()

# RMSE
axes[0, 1].barh(df_comparacion['Estrategia'], df_comparacion['RMSE'], color='coral')
axes[0, 1].set_xlabel('RMSE')
axes[0, 1].set_title('Root Mean Squared Error por Estrategia')
axes[0, 1].invert_yaxis()

# R²
axes[1, 0].barh(df_comparacion['Estrategia'], df_comparacion['R²'], color='seagreen')
axes[1, 0].set_xlabel('R²')
axes[1, 0].set_title('R² Score por Estrategia')
axes[1, 0].invert_yaxis()

# CV MAE
axes[1, 1].barh(df_comparacion['Estrategia'], df_comparacion['CV_MAE'], color='mediumpurple')
axes[1, 1].set_xlabel('CV MAE')
axes[1, 1].set_title('Cross-Validation MAE por Estrategia')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'comparacion_estrategias.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Guardado: comparacion_estrategias.png")

# 7.2 Elbow curve para K-Means
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.plot(k_range, inertias, 'bo-')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Curve - Inertia')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.plot(k_range, silhouettes, 'ro-')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score por K')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.plot(k_range, davies_bouldin, 'go-')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Davies-Bouldin Score')
plt.title('Davies-Bouldin Score por K')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'kmeans_metricas.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Guardado: kmeans_metricas.png")

# 7.3 PCA para visualizar clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(18, 6))

# K-Means
plt.subplot(1, 3, 1)
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster_kmeans'], 
                     cmap='viridis', alpha=0.6, s=30)
plt.colorbar(scatter)
plt.title(f'K-Means Clusters (k={optimal_k_silhouette})')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')

# Hierarchical
plt.subplot(1, 3, 2)
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster_hierarchical'], 
                     cmap='plasma', alpha=0.6, s=30)
plt.colorbar(scatter)
plt.title('Hierarchical Clusters')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')

# Por Sexo (categórico)
plt.subplot(1, 3, 3)
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_encoded['sexo_encoded'], 
                     cmap='coolwarm', alpha=0.6, s=30)
plt.colorbar(scatter, ticks=[0, 1], label=['HEMBRA', 'MACHO'])
plt.title('Distribución por Sexo')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'visualizacion_clusters.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Guardado: visualizacion_clusters.png")

# 7.4 Dendrograma para clustering jerárquico
plt.figure(figsize=(16, 8))
dendrogram(linkage_matrix, truncate_mode='lastp', p=30)
plt.title('Dendrograma - Clustering Jerárquico (últimas 30 fusiones)')
plt.xlabel('Índice de muestra o tamaño del cluster')
plt.ylabel('Distancia')
plt.savefig(OUTPUT_DIR / 'dendrograma.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Guardado: dendrograma.png")

# ==============================================================================
# 8. GUARDAR RESULTADOS
# ==============================================================================

print("\n" + "=" * 80)
print("8. GUARDANDO RESULTADOS")
print("=" * 80)

# Guardar tabla comparativa
df_comparacion.to_csv(OUTPUT_DIR / 'comparacion_estrategias.csv', index=False)
print(f"   ✓ Guardado: comparacion_estrategias.csv")

# Guardar resultados detallados en JSON
with open(OUTPUT_DIR / 'resultados_detallados.json', 'w') as f:
    json.dump(estrategias_resultados, f, indent=2)
print(f"   ✓ Guardado: resultados_detallados.json")

# Guardar dataset con clusters
df_clusters = df[['nombre_sector_code', 'nro_crianza', 'nro_pabellon', 
                  'sexo', 'tipoConstruccion', 'densidad_pollos_m2',
                  'cluster_kmeans', 'cluster_hierarchical', 'cluster_dbscan',
                  target]].copy()
df_clusters.to_csv(OUTPUT_DIR / 'dataset_con_clusters.csv', index=False)
print(f"   ✓ Guardado: dataset_con_clusters.csv")

# Crear reporte markdown
reporte = f"""# REPORTE: Análisis de Clusterización para Modelos Predictivos

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Resumen Ejecutivo

Este análisis evalúa si es conveniente crear modelos separados por clusters en lugar de un modelo único
para predecir `ganancia_promedio_gramos`.

### Estrategias Evaluadas:
1. Modelo Único (Baseline)
2. Modelos por Sexo
3. Modelos por Densidad
4. Modelos por Tipo de Construcción
5. Modelos por Sector
6. Modelos por K-Means Clustering
7. Modelos por Hierarchical Clustering

## 2. Mejor Estrategia Identificada

**{mejor_estrategia['Estrategia']}**

- **MAE:** {mejor_estrategia['MAE']:.4f}
- **RMSE:** {mejor_estrategia['RMSE']:.4f}
- **R²:** {mejor_estrategia['R²']:.4f}
- **Número de Modelos:** {int(mejor_estrategia['N_Modelos'])}

### Mejora vs Baseline: {mejora_porcentual:.2f}%

## 3. Tabla Comparativa Completa

{df_comparacion.to_markdown(index=False)}

## 4. Análisis Estadístico de Grupos Naturales

### SEXO
- **ANOVA p-value:** {resultados_grupos['sexo'][2]:.6f}
- **Significativo:** {'Sí' if resultados_grupos['sexo'][2] < 0.05 else 'No'}

### DENSIDAD
- **ANOVA p-value:** {resultados_grupos['densidad'][2]:.6f}
- **Significativo:** {'Sí' if resultados_grupos['densidad'][2] < 0.05 else 'No'}

### TIPO DE CONSTRUCCIÓN
- **ANOVA p-value:** {resultados_grupos['tipo_construccion'][2]:.6f}
- **Significativo:** {'Sí' if resultados_grupos['tipo_construccion'][2] < 0.05 else 'No'}

### SECTOR
- **ANOVA p-value:** {resultados_grupos['sector'][2]:.6f}
- **Significativo:** {'Sí' if resultados_grupos['sector'][2] < 0.05 else 'No'}

## 5. Clustering Automático

### K-Means
- **K óptimo (Silhouette):** {optimal_k_silhouette}
- **Silhouette Score:** {max(silhouettes):.3f}

### Hierarchical
- **K utilizado:** {optimal_k_silhouette}
- **Método:** Ward linkage

### DBSCAN
- **Clusters encontrados:** {n_clusters_dbscan}
- **Puntos de ruido:** {n_noise}

## 6. Recomendación Final

"""

if mejora_porcentual > 5:
    reporte += f"""
✅ **RECOMENDACIÓN: Usar clusterización**

La estrategia **{mejor_estrategia['Estrategia']}** muestra una mejora significativa de **{mejora_porcentual:.2f}%** 
respecto al modelo único. Esta mejora justifica la complejidad adicional de mantener múltiples modelos.

**Ventajas:**
- Mayor precisión en las predicciones
- Captura mejor las características específicas de cada grupo
- Menor error absoluto promedio

**Consideraciones:**
- Requiere mantener {int(mejor_estrategia['N_Modelos'])} modelos separados
- Mayor complejidad en el despliegue y mantenimiento
"""
elif mejora_porcentual > 0:
    reporte += f"""
⚠️ **PRECAUCIÓN: Mejora marginal**

La mejora de **{mejora_porcentual:.2f}%** es positiva pero marginal. Evaluar si el trade-off entre
complejidad y mejora es favorable para el caso de uso específico.

**Recomendación:** Usar modelo único a menos que la pequeña mejora sea crítica para el negocio.
"""
else:
    reporte += f"""
❌ **RECOMENDACIÓN: Mantener modelo único**

No se observa mejora significativa con la clusterización. El modelo único es la mejor opción
por su simplicidad y facilidad de mantenimiento.
"""

reporte += """

## 7. Archivos Generados

- `comparacion_estrategias.png` - Gráficos comparativos de todas las estrategias
- `kmeans_metricas.png` - Análisis de K óptimo para K-Means
- `visualizacion_clusters.png` - Visualización PCA de los clusters
- `dendrograma.png` - Dendrograma del clustering jerárquico
- `comparacion_estrategias.csv` - Tabla comparativa en CSV
- `resultados_detallados.json` - Resultados completos en JSON
- `dataset_con_clusters.csv` - Dataset con asignación de clusters

## 8. Próximos Pasos Sugeridos

1. Validar la estrategia recomendada con datos nuevos
2. Analizar la estabilidad de los clusters en el tiempo
3. Considerar ensembles que combinen múltiples estrategias
4. Evaluar el impacto en producción con A/B testing
"""

with open(OUTPUT_DIR / 'REPORTE_CLUSTERIZACION.md', 'w', encoding='utf-8') as f:
    f.write(reporte)
    
print(f"   ✓ Guardado: REPORTE_CLUSTERIZACION.md")

print("\n" + "=" * 80)
print("✅ ANÁLISIS COMPLETADO")
print("=" * 80)
print(f"\nResultados guardados en: {OUTPUT_DIR}")
print("\nArchivos generados:")
print("  • comparacion_estrategias.png")
print("  • kmeans_metricas.png")
print("  • visualizacion_clusters.png")
print("  • dendrograma.png")
print("  • comparacion_estrategias.csv")
print("  • resultados_detallados.json")
print("  • dataset_con_clusters.csv")
print("  • REPORTE_CLUSTERIZACION.md")

print("\n" + "=" * 80)
