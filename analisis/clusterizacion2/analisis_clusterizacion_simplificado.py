"""
ANÁLISIS DE CLUSTERIZACIÓN SIMPLIFICADO
Solo considerando: Sexo, Densidad y Tipo de Construcción

OBJETIVO: Evaluar estrategias de clustering usando únicamente las 3 variables principales
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.stats import f_oneway
import warnings
from datetime import datetime
import json

warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("ANÁLISIS DE CLUSTERIZACIÓN SIMPLIFICADO")
print("Variables: Sexo, Densidad, Tipo de Construcción")
print("="*80)
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# 1. CARGA Y PREPARACIÓN
# ============================================================================
print("\n1. Cargando datos...")
df = pd.read_csv('../../work_data/resumen_crianzas_para_modelo2.csv')
print(f"   ✓ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

# Variables de interés
variables_clustering = ['sexo', 'densidad_pollos_m2', 'tipoConstruccion']
target = 'ganancia_promedio_gramos'

print(f"\n2. Variables para clustering:")
print(f"   • {', '.join(variables_clustering)}")
print(f"   • Target: {target}")

# Verificar datos faltantes
print(f"\n3. Verificando datos faltantes:")
for var in variables_clustering + [target]:
    missing = df[var].isna().sum()
    print(f"   • {var}: {missing} faltantes ({missing/len(df)*100:.1f}%)")

# Eliminar filas con valores faltantes en variables clave
df_clean = df[variables_clustering + [target]].dropna()
print(f"\n   ✓ Dataset limpio: {len(df_clean)} filas")

# ============================================================================
# 2. ANÁLISIS DESCRIPTIVO POR GRUPOS
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISIS POR GRUPOS NATURALES")
print("="*80)

def analizar_grupo(df, columna, nombre):
    """Analiza diferencias de ganancia por grupos"""
    print(f"\n   📊 {nombre}:")
    stats = df.groupby(columna)[target].agg(['count', 'mean', 'std', 'min', 'max'])
    print(stats.round(2))

    # ANOVA
    grupos = [df[df[columna] == cat][target].values for cat in df[columna].unique()]
    f_stat, p_value = f_oneway(*grupos)
    print(f"   ANOVA: F-statistic={f_stat:.4f}, p-value={p_value:.6f}")

    if p_value < 0.05:
        print(f"   ✓ Diferencias SIGNIFICATIVAS entre grupos (p < 0.05)")
    else:
        print(f"   ✗ No hay diferencias significativas (p >= 0.05)")

    return stats, f_stat, p_value

anova_results = {}
for var in variables_clustering:
    nombre = var.upper()
    stats, f_stat, p_value = analizar_grupo(df_clean, var, nombre)
    anova_results[var] = {'f_stat': f_stat, 'p_value': p_value}

# ============================================================================
# 3. PREPARACIÓN PARA CLUSTERING
# ============================================================================
print("\n" + "="*80)
print("3. PREPARACIÓN PARA CLUSTERING")
print("="*80)

# Codificar variables categóricas
df_encoded = df_clean.copy()
le_sexo = LabelEncoder()
le_tipo = LabelEncoder()

df_encoded['sexo_encoded'] = le_sexo.fit_transform(df_clean['sexo'])
df_encoded['tipo_encoded'] = le_tipo.fit_transform(df_clean['tipoConstruccion'])

# Features para clustering (solo las 3 variables)
X_clustering = df_encoded[['sexo_encoded', 'densidad_pollos_m2', 'tipo_encoded']].values

# Normalizar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clustering)

print(f"\n   ✓ Variables codificadas y normalizadas")
print(f"   • Shape de X: {X_scaled.shape}")

# ============================================================================
# 4. CLUSTERING AUTOMÁTICO
# ============================================================================
print("\n" + "="*80)
print("4. CLUSTERING AUTOMÁTICO (K-MEANS)")
print("="*80)

# Determinar K óptimo
k_range = range(2, 11)
inertias = []
silhouette_scores = []
davies_bouldin_scores = []

print("\n   Calculando métricas para diferentes K...")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, labels))
    davies_bouldin_scores.append(davies_bouldin_score(X_scaled, labels))

# K óptimo según Silhouette
k_opt_silhouette = k_range[np.argmax(silhouette_scores)]
k_opt_db = k_range[np.argmin(davies_bouldin_scores)]

print(f"\n   🔍 K-Means Clustering:")
print(f"   • K óptimo (Silhouette): {k_opt_silhouette} (score={max(silhouette_scores):.3f})")
print(f"   • K óptimo (Davies-Bouldin): {k_opt_db} (score={min(davies_bouldin_scores):.3f})")

# Aplicar K-Means con K óptimo (Silhouette)
kmeans_final = KMeans(n_clusters=k_opt_silhouette, random_state=42, n_init=10)
df_encoded['cluster_kmeans'] = kmeans_final.fit_predict(X_scaled)

print(f"\n   Distribución de clusters K-Means (K={k_opt_silhouette}):")
print(df_encoded['cluster_kmeans'].value_counts().sort_index())

# Hierarchical Clustering
print(f"\n   🔍 Hierarchical Clustering (K={k_opt_silhouette}):")
hierarchical = AgglomerativeClustering(n_clusters=k_opt_silhouette)
df_encoded['cluster_hierarchical'] = hierarchical.fit_predict(X_scaled)
print(df_encoded['cluster_hierarchical'].value_counts().sort_index())

# DBSCAN
print(f"\n   🔍 DBSCAN Clustering:")
dbscan = DBSCAN(eps=1.0, min_samples=10)
df_encoded['cluster_dbscan'] = dbscan.fit_predict(X_scaled)
n_clusters_dbscan = len(set(df_encoded['cluster_dbscan'])) - (1 if -1 in df_encoded['cluster_dbscan'] else 0)
n_noise = list(df_encoded['cluster_dbscan']).count(-1)
print(f"   • Clusters encontrados: {n_clusters_dbscan}")
print(f"   • Puntos de ruido: {n_noise}")

# ============================================================================
# 5. EVALUACIÓN DE ESTRATEGIAS
# ============================================================================
print("\n" + "="*80)
print("5. EVALUACIÓN DE ESTRATEGIAS DE MODELADO")
print("="*80)

def evaluar_estrategia(df, column, nombre_estrategia):
    """Evalúa una estrategia de modelado"""
    print(f"\n   📈 Evaluando: {nombre_estrategia}")
    print("   " + "-"*60)

    # Features para predicción (todas menos target)
    feature_cols = ['sexo_encoded', 'densidad_pollos_m2', 'tipo_encoded']
    X = df[feature_cols].values
    y = df[target].values

    if column is None:
        # Modelo único
        modelo = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        modelo.fit(X, y)
        y_pred = modelo.predict(X)

        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        r2 = r2_score(y, y_pred)

        # Cross-validation
        cv_scores = cross_val_score(modelo, X, y, cv=5,
                                     scoring='neg_mean_absolute_error', n_jobs=-1)
        cv_mae = -cv_scores.mean()

        print(f"   • Modelo Único:")
        print(f"     - MAE: {mae:.4f}")
        print(f"     - RMSE: {rmse:.4f}")
        print(f"     - R²: {r2:.4f}")
        print(f"     - CV MAE: {cv_mae:.4f} (±{cv_scores.std():.4f})")

        return {
            'estrategia': nombre_estrategia,
            'n_modelos': 1,
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'cv_mae': cv_mae
        }

    else:
        # Modelos separados por grupo
        grupos = df[column].unique()
        resultados_grupos = []

        for grupo in grupos:
            df_grupo = df[df[column] == grupo]
            if len(df_grupo) < 30:  # Mínimo 30 registros
                continue

            X_grupo = df_grupo[feature_cols].values
            y_grupo = df_grupo[target].values

            modelo = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            modelo.fit(X_grupo, y_grupo)
            y_pred = modelo.predict(X_grupo)

            mae = mean_absolute_error(y_grupo, y_pred)
            rmse = np.sqrt(mean_squared_error(y_grupo, y_pred))
            r2 = r2_score(y_grupo, y_pred)

            # Cross-validation (si hay suficientes datos)
            if len(df_grupo) >= 50:
                cv_scores = cross_val_score(modelo, X_grupo, y_grupo, cv=min(5, len(df_grupo)//10),
                                           scoring='neg_mean_absolute_error', n_jobs=-1)
                cv_mae = -cv_scores.mean()
            else:
                cv_mae = mae

            resultados_grupos.append({
                'grupo': grupo,
                'n': len(df_grupo),
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'cv_mae': cv_mae
            })

        # Promedios ponderados
        total_n = sum([r['n'] for r in resultados_grupos])
        mae_prom = sum([r['mae'] * r['n'] for r in resultados_grupos]) / total_n
        rmse_prom = sum([r['rmse'] * r['n'] for r in resultados_grupos]) / total_n
        r2_prom = sum([r['r2'] * r['n'] for r in resultados_grupos]) / total_n
        cv_mae_prom = sum([r['cv_mae'] * r['n'] for r in resultados_grupos]) / total_n

        print(f"   • {len(resultados_grupos)} Modelos Separados:")
        print(f"     - MAE promedio: {mae_prom:.4f}")
        print(f"     - RMSE promedio: {rmse_prom:.4f}")
        print(f"     - R² promedio: {r2_prom:.4f}")
        print(f"     - CV MAE promedio: {cv_mae_prom:.4f}")

        return {
            'estrategia': nombre_estrategia,
            'n_modelos': len(resultados_grupos),
            'mae': mae_prom,
            'rmse': rmse_prom,
            'r2': r2_prom,
            'cv_mae': cv_mae_prom,
            'detalle_grupos': resultados_grupos
        }

# Evaluar todas las estrategias
estrategias = []

# 1. Modelo único
estrategias.append(evaluar_estrategia(df_encoded, None, "1. MODELO ÚNICO (Baseline)"))

# 2. Por Sexo
estrategias.append(evaluar_estrategia(df_encoded, 'sexo', "2. MODELOS POR SEXO"))

# 3. Por Tipo Construcción
estrategias.append(evaluar_estrategia(df_encoded, 'tipoConstruccion', "3. MODELOS POR TIPO CONSTRUCCIÓN"))

# 4. Por K-Means
estrategias.append(evaluar_estrategia(df_encoded, 'cluster_kmeans', f"4. MODELOS POR K-MEANS (k={k_opt_silhouette})"))

# 5. Por Hierarchical
estrategias.append(evaluar_estrategia(df_encoded, 'cluster_hierarchical', f"5. MODELOS POR HIERARCHICAL (k={k_opt_silhouette})"))

# ============================================================================
# 6. RANKING Y RECOMENDACIÓN
# ============================================================================
print("\n" + "="*80)
print("6. RANKING DE ESTRATEGIAS")
print("="*80)

# Crear DataFrame de resultados
df_resultados = pd.DataFrame([{
    'Estrategia': e['estrategia'],
    'N_Modelos': e['n_modelos'],
    'MAE': e['mae'],
    'RMSE': e['rmse'],
    'R²': e['r2'],
    'CV_MAE': e['cv_mae']
} for e in estrategias])

# Ordenar por MAE (menor es mejor)
df_resultados = df_resultados.sort_values('MAE')

print("\n   📊 TABLA COMPARATIVA (ordenado por MAE):")
print(df_resultados.to_string(index=False))

# Mejor estrategia
mejor = df_resultados.iloc[0]
baseline = df_resultados[df_resultados['Estrategia'].str.contains('Baseline')].iloc[0]

mejora_pct = ((baseline['MAE'] - mejor['MAE']) / baseline['MAE']) * 100

print("\n" + "="*80)
print("7. RECOMENDACIÓN FINAL")
print("="*80)

print(f"\n   🏆 MEJOR ESTRATEGIA: {mejor['Estrategia']}")
print(f"   Métricas:")
print(f"   • MAE: {mejor['MAE']:.4f}")
print(f"   • RMSE: {mejor['RMSE']:.4f}")
print(f"   • R²: {mejor['R²']:.4f}")
print(f"   • Número de modelos: {int(mejor['N_Modelos'])}")

print(f"\n   📈 Mejora vs Baseline: {mejora_pct:.2f}%")

if mejora_pct > 5:
    print(f"\n   ✅ RECOMENDACIÓN: Implementar {mejor['Estrategia']}")
    print(f"      La mejora de {mejora_pct:.2f}% justifica la complejidad adicional.")
elif mejora_pct > 1:
    print(f"\n   ⚠️  PRECAUCIÓN: Mejora marginal de {mejora_pct:.2f}%")
    print(f"      Considerar si la complejidad adicional vale la pena.")
else:
    print(f"\n   ❌ RECOMENDACIÓN: Mantener MODELO ÚNICO")
    print(f"      Mejora de {mejora_pct:.2f}% no justifica complejidad.")

# ============================================================================
# 7. VISUALIZACIONES
# ============================================================================
print("\n" + "="*80)
print("8. GENERANDO VISUALIZACIONES")
print("="*80)

# 1. Comparación de estrategias
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# MAE
ax = axes[0, 0]
df_resultados.plot(x='Estrategia', y='MAE', kind='barh', ax=ax, legend=False, color='steelblue')
ax.set_title('MAE por Estrategia (menor es mejor)', fontsize=14, fontweight='bold')
ax.set_xlabel('MAE (gramos)')
ax.invert_yaxis()

# RMSE
ax = axes[0, 1]
df_resultados.plot(x='Estrategia', y='RMSE', kind='barh', ax=ax, legend=False, color='coral')
ax.set_title('RMSE por Estrategia (menor es mejor)', fontsize=14, fontweight='bold')
ax.set_xlabel('RMSE (gramos)')
ax.invert_yaxis()

# R²
ax = axes[1, 0]
df_resultados.plot(x='Estrategia', y='R²', kind='barh', ax=ax, legend=False, color='mediumseagreen')
ax.set_title('R² por Estrategia (mayor es mejor)', fontsize=14, fontweight='bold')
ax.set_xlabel('R² Score')
ax.invert_yaxis()

# CV MAE
ax = axes[1, 1]
df_resultados.plot(x='Estrategia', y='CV_MAE', kind='barh', ax=ax, legend=False, color='mediumpurple')
ax.set_title('CV MAE por Estrategia (menor es mejor)', fontsize=14, fontweight='bold')
ax.set_xlabel('CV MAE (gramos)')
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('comparacion_estrategias.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: comparacion_estrategias.png")

# 2. Métricas de K-Means
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Elbow curve
axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Número de Clusters (K)', fontsize=12)
axes[0].set_ylabel('Inercia', fontsize=12)
axes[0].set_title('Elbow Curve (Método del Codo)', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Silhouette
axes[1].plot(k_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[1].axvline(k_opt_silhouette, color='red', linestyle='--', label=f'Óptimo K={k_opt_silhouette}')
axes[1].set_xlabel('Número de Clusters (K)', fontsize=12)
axes[1].set_ylabel('Silhouette Score', fontsize=12)
axes[1].set_title('Silhouette Score vs K (mayor es mejor)', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Davies-Bouldin
axes[2].plot(k_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
axes[2].axvline(k_opt_db, color='blue', linestyle='--', label=f'Óptimo K={k_opt_db}')
axes[2].set_xlabel('Número de Clusters (K)', fontsize=12)
axes[2].set_ylabel('Davies-Bouldin Score', fontsize=12)
axes[2].set_title('Davies-Bouldin Score vs K (menor es mejor)', fontsize=14, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kmeans_metricas.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: kmeans_metricas.png")

# 3. Visualización de clusters (reducción a 2D con PCA)
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# K-Means clusters
scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1],
                          c=df_encoded['cluster_kmeans'],
                          cmap='viridis', alpha=0.6, s=30)
axes[0].set_title(f'K-Means Clusters (K={k_opt_silhouette})', fontsize=14, fontweight='bold')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
plt.colorbar(scatter, ax=axes[0], label='Cluster')

# Hierarchical clusters
scatter = axes[1].scatter(X_pca[:, 0], X_pca[:, 1],
                          c=df_encoded['cluster_hierarchical'],
                          cmap='plasma', alpha=0.6, s=30)
axes[1].set_title(f'Hierarchical Clusters (K={k_opt_silhouette})', fontsize=14, fontweight='bold')
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
plt.colorbar(scatter, ax=axes[1], label='Cluster')

# Por Sexo (referencia)
sexo_colors = {'HEMBRA': 0, 'MACHO': 1}
colors = [sexo_colors[s] for s in df_encoded['sexo']]
scatter = axes[2].scatter(X_pca[:, 0], X_pca[:, 1],
                          c=colors, cmap='coolwarm', alpha=0.6, s=30)
axes[2].set_title('Distribución por Sexo', fontsize=14, fontweight='bold')
axes[2].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[2].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
cbar = plt.colorbar(scatter, ax=axes[2], ticks=[0, 1])
cbar.set_ticklabels(['HEMBRA', 'MACHO'])

plt.tight_layout()
plt.savefig('visualizacion_clusters.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: visualizacion_clusters.png")

# 4. Dendrograma
linkage_matrix = linkage(X_scaled, method='ward')

plt.figure(figsize=(16, 8))
dendrogram(linkage_matrix, truncate_mode='lastp', p=30)
plt.title('Dendrograma - Clustering Jerárquico (últimas 30 fusiones)',
          fontsize=16, fontweight='bold')
plt.xlabel('Índice del Cluster o (tamaño del cluster)', fontsize=12)
plt.ylabel('Distancia', fontsize=12)
plt.tight_layout()
plt.savefig('dendrograma.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: dendrograma.png")

plt.close('all')

# ============================================================================
# 8. GUARDAR RESULTADOS
# ============================================================================
print("\n" + "="*80)
print("9. GUARDANDO RESULTADOS")
print("="*80)

# CSV
df_resultados.to_csv('comparacion_estrategias.csv', index=False)
print("   ✓ Guardado: comparacion_estrategias.csv")

# JSON detallado - Convertir NumPy types a tipos Python nativos
def convert_to_native(obj):
    """Convierte NumPy types a tipos Python nativos para JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_native(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(item) for item in obj]
    return obj

resultados_json = {
    'fecha_analisis': datetime.now().isoformat(),
    'variables_clustering': variables_clustering,
    'anova_results': convert_to_native(anova_results),
    'k_optimo_silhouette': int(k_opt_silhouette),
    'k_optimo_davies_bouldin': int(k_opt_db),
    'estrategias': convert_to_native(estrategias),
    'mejor_estrategia': mejor['Estrategia'],
    'mejora_porcentual': float(mejora_pct),
    'recomendacion': 'implementar' if mejora_pct > 5 else ('evaluar' if mejora_pct > 1 else 'mantener_unico')
}

with open('resultados_detallados.json', 'w', encoding='utf-8') as f:
    json.dump(resultados_json, f, indent=2, ensure_ascii=False)
print("   ✓ Guardado: resultados_detallados.json")

# Dataset con clusters
df_encoded.to_csv('dataset_con_clusters.csv', index=False)
print("   ✓ Guardado: dataset_con_clusters.csv")

# Reporte Markdown
reporte_md = f"""# 📊 REPORTE DE CLUSTERIZACIÓN SIMPLIFICADO

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Variables:** Sexo, Densidad (pollos/m²), Tipo de Construcción

---

## 1. Resumen Ejecutivo

Se evaluaron **{len(estrategias)} estrategias** de modelado para predecir `ganancia_promedio_gramos`:

- ✅ Modelo Único (Baseline)
- ✅ Modelos por Sexo
- ✅ Modelos por Tipo de Construcción  
- ✅ Modelos por K-Means Clustering
- ✅ Modelos por Hierarchical Clustering

---

## 2. Mejor Estrategia

🏆 **{mejor['Estrategia']}**

**Métricas:**
- MAE: **{mejor['MAE']:.4f}** gramos
- RMSE: **{mejor['RMSE']:.4f}** gramos
- R²: **{mejor['R²']:.4f}**
- Número de modelos: **{int(mejor['N_Modelos'])}**

**Mejora vs Baseline:** {mejora_pct:.2f}%

---

## 3. Tabla Comparativa

{df_resultados.to_markdown(index=False)}

---

## 4. Análisis Estadístico (ANOVA)

### Diferencias entre grupos:

**Sexo:**
- F-statistic: {anova_results['sexo']['f_stat']:.2f}
- p-value: {anova_results['sexo']['p_value']:.6f}
- Significativo: {'✅ Sí' if anova_results['sexo']['p_value'] < 0.05 else '❌ No'}

**Tipo de Construcción:**
- F-statistic: {anova_results['tipoConstruccion']['f_stat']:.2f}
- p-value: {anova_results['tipoConstruccion']['p_value']:.6f}
- Significativo: {'✅ Sí' if anova_results['tipoConstruccion']['p_value'] < 0.05 else '❌ No'}

---

## 5. Clustering Automático

### K-Means
- **K óptimo (Silhouette):** {k_opt_silhouette}
- **Silhouette Score:** {max(silhouette_scores):.3f}

### Hierarchical Clustering
- **K utilizado:** {k_opt_silhouette}
- **Método:** Ward linkage

### DBSCAN
- **Clusters encontrados:** {n_clusters_dbscan}
- **Puntos de ruido:** {n_noise}

---

## 6. Recomendación Final

"""

if mejora_pct > 5:
    reporte_md += f"""✅ **IMPLEMENTAR {mejor['Estrategia']}**

La mejora de **{mejora_pct:.2f}%** justifica la implementación de modelos separados.

**Próximos pasos:**
1. Entrenar modelos específicos por {mejor['Estrategia'].split('POR ')[-1].lower()}
2. Implementar sistema de enrutamiento de predicciones
3. Monitorear rendimiento en producción
"""
elif mejora_pct > 1:
    reporte_md += f"""⚠️ **EVALUAR TRADE-OFF**

La mejora de **{mejora_pct:.2f}%** es marginal. 

**Considerar:**
- Costo operacional de mantener {int(mejor['N_Modelos'])} modelos
- Complejidad de implementación
- Beneficio de {mejora_pct:.2f}% en MAE

**Recomendación:** Realizar análisis costo/beneficio antes de implementar.
"""
else:
    reporte_md += f"""❌ **MANTENER MODELO ÚNICO**

La mejora de **{mejora_pct:.2f}%** NO justifica la complejidad adicional.

**Razones:**
- El modelo único ya tiene excelente rendimiento (R²={baseline['R²']:.4f})
- Simplicidad operacional
- Fácil mantenimiento y actualización

**Recomendación:** Enfocar esfuerzos en feature engineering del modelo único.
"""

reporte_md += f"""

---

## 7. Archivos Generados

- 📊 `comparacion_estrategias.png` - Gráficos comparativos
- 📈 `kmeans_metricas.png` - Métricas de clustering
- 🔍 `visualizacion_clusters.png` - PCA de clusters
- 🌳 `dendrograma.png` - Clustering jerárquico
- 📁 `comparacion_estrategias.csv` - Tabla de resultados
- 📋 `resultados_detallados.json` - Resultados completos
- 💾 `dataset_con_clusters.csv` - Dataset con clusters asignados

---

## 8. Próximos Pasos

1. Revisar visualizaciones generadas
2. {'Implementar estrategia recomendada' if mejora_pct > 5 else 'Evaluar costo/beneficio' if mejora_pct > 1 else 'Optimizar modelo único'}
3. Validar resultados en conjunto de validación independiente
4. {'Preparar deployment de modelos múltiples' if mejora_pct > 5 else 'Mantener pipeline actual'}

---

**Análisis completado exitosamente ✅**
"""

with open('REPORTE_CLUSTERIZACION.md', 'w', encoding='utf-8') as f:
    f.write(reporte_md)
print("   ✓ Guardado: REPORTE_CLUSTERIZACION.md")

# ============================================================================
# FINALIZACIÓN
# ============================================================================
print("\n" + "="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)
print(f"Resultados guardados en: C:\\tecnoandina\\f35_modelacion2\\analisis\\clusterizacion2")
print("\nArchivos generados:")
print("  • comparacion_estrategias.png")
print("  • kmeans_metricas.png")
print("  • visualizacion_clusters.png")
print("  • dendrograma.png")
print("  • comparacion_estrategias.csv")
print("  • resultados_detallados.json")
print("  • dataset_con_clusters.csv")
print("  • REPORTE_CLUSTERIZACION.md")
print("="*80)
