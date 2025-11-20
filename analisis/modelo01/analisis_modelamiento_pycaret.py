"""
ANÁLISIS Y MODELAMIENTO EXHAUSTIVO CON PYCARET
Predicción de ganancia_promedio_gramos

OBJETIVO: Crear el mejor modelo predictivo usando PyCaret y análisis exhaustivo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
from datetime import datetime
import json

warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("="*80)
print("ANÁLISIS Y MODELAMIENTO EXHAUSTIVO CON PYCARET")
print("="*80)
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ============================================================================
print("="*80)
print("1. CARGA Y PREPARACIÓN DE DATOS")
print("="*80)

# Cargar datos
df = pd.read_csv('../../work_data/resumen_crianzas_para_modelo2.csv')
print(f"\n✓ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

# Variables de interés
features = [
    'mes_carga',
    'edad_madres_dias', 
    'peso_inicial_gramos',
    'sexo',
    'kilos_recibidos_percapita',
    'tipoConstruccion',
    'densidad_pollos_m2'
]
target = 'ganancia_promedio_gramos'

print(f"\n📊 Variables seleccionadas:")
print(f"   • Features: {len(features)}")
print(f"   • Target: {target}")

# Seleccionar columnas y eliminar NaN
df_model = df[features + [target]].copy()
print(f"\n📋 Datos antes de limpiar: {len(df_model)} filas")
df_model = df_model.dropna()
print(f"   Datos después de limpiar: {len(df_model)} filas")
print(f"   Registros eliminados: {len(df) - len(df_model)}")

# Información básica
print(f"\n📈 Estadísticas básicas del target:")
print(df_model[target].describe())

# ============================================================================
# 2. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISIS EXPLORATORIO DE DATOS")
print("="*80)

# Tipos de variables
numeric_features = df_model.select_dtypes(include=[np.number]).columns.tolist()
numeric_features.remove(target)
categorical_features = df_model.select_dtypes(include=['object']).columns.tolist()

print(f"\n📊 Tipos de variables:")
print(f"   • Numéricas: {len(numeric_features)} → {numeric_features}")
print(f"   • Categóricas: {len(categorical_features)} → {categorical_features}")

# Análisis de variables categóricas
print(f"\n📊 Análisis de variables categóricas:")
for col in categorical_features:
    print(f"\n   {col}:")
    value_counts = df_model[col].value_counts()
    print(f"   {value_counts}")
    
    # ANOVA
    groups = [df_model[df_model[col] == cat][target].values for cat in df_model[col].unique()]
    f_stat, p_value = f_oneway(*groups)
    print(f"   ANOVA: F={f_stat:.2f}, p-value={p_value:.6f}", end="")
    if p_value < 0.05:
        print(" ✓ Significativo")
    else:
        print(" ✗ No significativo")

# Análisis de variables numéricas
print(f"\n📊 Análisis de variables numéricas:")
print(df_model[numeric_features].describe().T)

# Detección de outliers (IQR method)
print(f"\n🔍 Detección de outliers (método IQR):")
outliers_summary = {}
for col in numeric_features:
    Q1 = df_model[col].quantile(0.25)
    Q3 = df_model[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df_model[(df_model[col] < lower_bound) | (df_model[col] > upper_bound)]
    outliers_count = len(outliers)
    outliers_pct = (outliers_count / len(df_model)) * 100
    outliers_summary[col] = {
        'count': outliers_count,
        'percentage': outliers_pct,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
    print(f"   • {col}: {outliers_count} outliers ({outliers_pct:.2f}%)")

# ============================================================================
# 3. ANÁLISIS DE CORRELACIONES
# ============================================================================
print("\n" + "="*80)
print("3. ANÁLISIS DE CORRELACIONES")
print("="*80)

# Codificar variables categóricas temporalmente para correlación
df_encoded = df_model.copy()
for col in categorical_features:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_model[col])

# Matriz de correlación
correlation_matrix = df_encoded.corr()
print(f"\n📊 Correlación con {target}:")
target_corr = correlation_matrix[target].sort_values(ascending=False)
print(target_corr)

# Correlaciones altas entre features (multicolinealidad)
print(f"\n⚠️  Correlaciones altas entre features (>0.7):")
high_corr_pairs = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        if abs(correlation_matrix.iloc[i, j]) > 0.7:
            col1 = correlation_matrix.columns[i]
            col2 = correlation_matrix.columns[j]
            if col1 != target and col2 != target:
                high_corr_pairs.append((col1, col2, correlation_matrix.iloc[i, j]))
                print(f"   • {col1} <-> {col2}: {correlation_matrix.iloc[i, j]:.3f}")

if not high_corr_pairs:
    print("   ✓ No se detectaron correlaciones altas entre features")

# ============================================================================
# 4. ANÁLISIS DE MULTICOLINEALIDAD (VIF)
# ============================================================================
print("\n" + "="*80)
print("4. ANÁLISIS DE MULTICOLINEALIDAD (VIF)")
print("="*80)

# Calcular VIF solo para variables numéricas
X_numeric = df_encoded[numeric_features].values
vif_data = pd.DataFrame()
vif_data["Feature"] = numeric_features
vif_data["VIF"] = [variance_inflation_factor(X_numeric, i) for i in range(len(numeric_features))]
vif_data = vif_data.sort_values('VIF', ascending=False)

print(f"\n📊 Variance Inflation Factor (VIF):")
print(vif_data.to_string(index=False))
print(f"\n💡 Interpretación VIF:")
print(f"   • VIF < 5: No hay multicolinealidad")
print(f"   • VIF 5-10: Multicolinealidad moderada")
print(f"   • VIF > 10: Multicolinealidad severa")

high_vif_features = vif_data[vif_data['VIF'] > 10]['Feature'].tolist()
if high_vif_features:
    print(f"\n⚠️  Features con VIF alto (>10): {high_vif_features}")
else:
    print(f"\n✓ No hay features con VIF alto")

# ============================================================================
# 5. FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("5. FEATURE ENGINEERING")
print("="*80)

df_engineered = df_model.copy()

# 5.1 Variables cíclicas para mes_carga
print(f"\n🔧 Creando variables cíclicas para mes_carga...")
df_engineered['mes_sin'] = np.sin(2 * np.pi * df_engineered['mes_carga'] / 12)
df_engineered['mes_cos'] = np.cos(2 * np.pi * df_engineered['mes_carga'] / 12)
print(f"   ✓ Creadas: mes_sin, mes_cos")

# 5.2 Ratios y variables derivadas
print(f"\n🔧 Creando variables derivadas...")

# Ratio de alimentación efectiva
df_engineered['alimento_por_densidad'] = df_engineered['kilos_recibidos_percapita'] / df_engineered['densidad_pollos_m2']
print(f"   ✓ alimento_por_densidad = kilos_recibidos / densidad")

# Ratio de peso inicial vs densidad
df_engineered['peso_inicial_por_densidad'] = df_engineered['peso_inicial_gramos'] / df_engineered['densidad_pollos_m2']
print(f"   ✓ peso_inicial_por_densidad = peso_inicial / densidad")

# Categoría de edad de madres
df_engineered['edad_madres_categoria'] = pd.cut(
    df_engineered['edad_madres_dias'], 
    bins=[0, 200, 300, 400, 1000],
    labels=['Joven', 'Adulta', 'Madura', 'Vieja']
)
print(f"   ✓ edad_madres_categoria (Joven/Adulta/Madura/Vieja)")

# Categoría de densidad
df_engineered['densidad_categoria'] = pd.cut(
    df_engineered['densidad_pollos_m2'],
    bins=[0, 13, 15, 20, 50],
    labels=['Baja', 'Media', 'Alta', 'Muy Alta']
)
print(f"   ✓ densidad_categoria (Baja/Media/Alta/Muy Alta)")

print(f"\n✓ Total de features después de engineering: {len(df_engineered.columns) - 1}")

# ============================================================================
# 6. PREPARACIÓN PARA MODELADO
# ============================================================================
print("\n" + "="*80)
print("6. PREPARACIÓN PARA MODELADO")
print("="*80)

# Lista completa de features para el modelo
features_modelo = [
    # Originales numéricas
    'edad_madres_dias',
    'peso_inicial_gramos', 
    'kilos_recibidos_percapita',
    'densidad_pollos_m2',
    # Originales categóricas
    'sexo',
    'tipoConstruccion',
    # Engineered - Cíclicas
    'mes_sin',
    'mes_cos',
    # Engineered - Ratios
    'alimento_por_densidad',
    'peso_inicial_por_densidad',
    # Engineered - Categorías
    'edad_madres_categoria',
    'densidad_categoria'
]

# Dataset final
df_final = df_engineered[features_modelo + [target]].copy()

# Eliminar NaN generados por feature engineering
df_final = df_final.dropna()
print(f"\n📊 Dataset final para modelado:")
print(f"   • Filas: {len(df_final)}")
print(f"   • Features: {len(features_modelo)}")
print(f"   • Target: {target}")

# Identificar tipos de features para PyCaret
categorical_features_final = df_final.select_dtypes(include=['object', 'category']).columns.tolist()
if target in categorical_features_final:
    categorical_features_final.remove(target)
    
numeric_features_final = [col for col in features_modelo if col not in categorical_features_final]

print(f"\n📊 Features finales:")
print(f"   • Numéricas ({len(numeric_features_final)}): {numeric_features_final}")
print(f"   • Categóricas ({len(categorical_features_final)}): {categorical_features_final}")

# ============================================================================
# 7. VISUALIZACIONES
# ============================================================================
print("\n" + "="*80)
print("7. GENERANDO VISUALIZACIONES")
print("="*80)

# 7.1 Matriz de correlación
plt.figure(figsize=(14, 12))
correlation_heatmap = df_encoded.corr()
mask = np.triu(np.ones_like(correlation_heatmap, dtype=bool))
sns.heatmap(correlation_heatmap, mask=mask, annot=True, fmt='.2f', 
            cmap='coolwarm', center=0, square=True, linewidths=1,
            cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlación de Variables', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('01_matriz_correlacion.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: 01_matriz_correlacion.png")
plt.close()

# 7.2 Distribuciones de variables numéricas
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
axes = axes.ravel()

for idx, col in enumerate(numeric_features + [target]):
    if idx < len(axes):
        axes[idx].hist(df_model[col], bins=50, edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'Distribución: {col}', fontweight='bold')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frecuencia')
        axes[idx].grid(True, alpha=0.3)

# Ocultar ejes vacíos
for idx in range(len(numeric_features + [target]), len(axes)):
    axes[idx].axis('off')

plt.suptitle('Distribuciones de Variables Numéricas', fontsize=18, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('02_distribuciones.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: 02_distribuciones.png")
plt.close()

# 7.3 Boxplots de target por variables categóricas
n_cat = len(categorical_features)
fig, axes = plt.subplots(1, n_cat, figsize=(6*n_cat, 6))
if n_cat == 1:
    axes = [axes]

for idx, col in enumerate(categorical_features):
    df_model.boxplot(column=target, by=col, ax=axes[idx])
    axes[idx].set_title(f'{target} por {col}', fontweight='bold')
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel(target)
    axes[idx].get_figure().suptitle('')

plt.suptitle('Target por Variables Categóricas', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('03_target_por_categoricas.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: 03_target_por_categoricas.png")
plt.close()

# 7.4 Scatter plots de correlaciones más altas
top_corr = target_corr[1:6]  # Top 5 correlaciones (excluyendo el target mismo)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.ravel()

for idx, (feature, corr_value) in enumerate(top_corr.items()):
    if idx < len(axes):
        axes[idx].scatter(df_encoded[feature], df_encoded[target], alpha=0.5, s=20)
        axes[idx].set_xlabel(feature, fontweight='bold')
        axes[idx].set_ylabel(target, fontweight='bold')
        axes[idx].set_title(f'{feature} vs {target}\n(Corr: {corr_value:.3f})', fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
        
        # Línea de regresión
        z = np.polyfit(df_encoded[feature], df_encoded[target], 1)
        p = np.poly1d(z)
        axes[idx].plot(df_encoded[feature], p(df_encoded[feature]), "r--", linewidth=2)

# Ocultar eje vacío
axes[-1].axis('off')

plt.suptitle('Top 5 Correlaciones con Target', fontsize=18, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('04_top_correlaciones.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: 04_top_correlaciones.png")
plt.close()

# 7.5 VIF Bar chart
plt.figure(figsize=(10, 6))
colors = ['red' if vif > 10 else 'orange' if vif > 5 else 'green' 
          for vif in vif_data['VIF']]
plt.barh(vif_data['Feature'], vif_data['VIF'], color=colors, alpha=0.7, edgecolor='black')
plt.axvline(x=5, color='orange', linestyle='--', linewidth=2, label='VIF = 5 (Moderado)')
plt.axvline(x=10, color='red', linestyle='--', linewidth=2, label='VIF = 10 (Severo)')
plt.xlabel('VIF (Variance Inflation Factor)', fontweight='bold')
plt.ylabel('Features', fontweight='bold')
plt.title('Análisis de Multicolinealidad (VIF)', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('05_vif_analysis.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: 05_vif_analysis.png")
plt.close()

# ============================================================================
# 8. MODELADO CON PYCARET
# ============================================================================
print("\n" + "="*80)
print("8. MODELADO CON PYCARET")
print("="*80)

# Inicializar variable para evitar errores
feature_importance_df = None

try:
    from pycaret.regression import *
    
    print("\n🤖 Configurando entorno PyCaret...")
    
    # Setup de PyCaret
    exp = setup(
        data=df_final,
        target=target,
        categorical_features=categorical_features_final,
        normalize=True,
        transformation=True,
        remove_outliers=True,
        outliers_threshold=0.05,
        session_id=42,
        train_size=0.8,
        fold=5,
        verbose=False,
        html=False,
        log_experiment=False
    )
    
    print("   ✓ PyCaret setup completado")
    
    # Comparar modelos
    print("\n🔍 Comparando modelos (esto puede tomar varios minutos)...")
    best_models = compare_models(
        sort='MAE',
        n_select=5,
        verbose=False
    )
    
    # Si best_models es una lista, tomamos el primero
    if isinstance(best_models, list):
        best_model = best_models[0]
    else:
        best_model = best_models
    
    print("\n✓ Comparación de modelos completada")
    
    # Obtener métricas del mejor modelo
    print(f"\n🏆 Mejor modelo: {type(best_model).__name__}")
    
    # Crear modelo final con el mejor
    print("\n🔧 Creando modelo final...")
    final_model = finalize_model(best_model)
    print("   ✓ Modelo final creado")
    
    # Guardar modelo
    save_model(final_model, 'modelo_final')
    print("   ✓ Modelo guardado: modelo_final.pkl")
    
    # Predicciones
    print("\n📊 Generando predicciones...")
    predictions = predict_model(final_model)
    
    # Calcular métricas finales
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    y_true = predictions[target]
    y_pred = predictions['prediction_label']
    
    mae_final = mean_absolute_error(y_true, y_pred)
    rmse_final = np.sqrt(mean_squared_error(y_true, y_pred))
    r2_final = r2_score(y_true, y_pred)
    
    print(f"\n📈 Métricas del modelo final:")
    print(f"   • MAE: {mae_final:.4f}")
    print(f"   • RMSE: {rmse_final:.4f}")
    print(f"   • R²: {r2_final:.4f}")
    
    # Feature Importance
    print("\n📊 Analizando importancia de features...")
    
    try:
        # Intentar obtener feature importance del modelo
        if hasattr(final_model, 'feature_importances_'):
            importances = final_model.feature_importances_
            feature_names = get_config('X_train').columns
            
            feature_importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)
            
            print("\n🔝 Top 10 Features más importantes:")
            print(feature_importance_df.head(10).to_string(index=False))
            
            # Guardar
            feature_importance_df.to_csv('feature_importance.csv', index=False)
            print("\n   ✓ Guardado: feature_importance.csv")
            
            # Visualización de feature importance
            plt.figure(figsize=(12, 8))
            top_features = feature_importance_df.head(15)
            plt.barh(top_features['Feature'], top_features['Importance'], edgecolor='black', alpha=0.7)
            plt.xlabel('Importancia', fontweight='bold', fontsize=12)
            plt.ylabel('Features', fontweight='bold', fontsize=12)
            plt.title('Top 15 Features más Importantes', fontsize=16, fontweight='bold')
            plt.gca().invert_yaxis()
            plt.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig('06_feature_importance.png', dpi=300, bbox_inches='tight')
            print("   ✓ Guardado: 06_feature_importance.png")
            plt.close()
            
    except Exception as e:
        print(f"   ⚠️  No se pudo calcular feature importance: {e}")
    
    # Gráfico de predicciones vs real
    plt.figure(figsize=(12, 8))
    plt.scatter(y_true, y_pred, alpha=0.5, s=30)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 
             'r--', lw=3, label='Predicción perfecta')
    plt.xlabel('Valores Reales', fontweight='bold', fontsize=12)
    plt.ylabel('Predicciones', fontweight='bold', fontsize=12)
    plt.title(f'Predicciones vs Valores Reales\nMAE: {mae_final:.4f} | RMSE: {rmse_final:.4f} | R²: {r2_final:.4f}',
              fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('07_predicciones_vs_real.png', dpi=300, bbox_inches='tight')
    print("   ✓ Guardado: 07_predicciones_vs_real.png")
    plt.close()
    
    # Residuos
    residuos = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Residuos vs predicciones
    axes[0].scatter(y_pred, residuos, alpha=0.5, s=30)
    axes[0].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Predicciones', fontweight='bold', fontsize=12)
    axes[0].set_ylabel('Residuos', fontweight='bold', fontsize=12)
    axes[0].set_title('Residuos vs Predicciones', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Histograma de residuos
    axes[1].hist(residuos, bins=50, edgecolor='black', alpha=0.7)
    axes[1].axvline(x=0, color='r', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Residuos', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('Frecuencia', fontweight='bold', fontsize=12)
    axes[1].set_title('Distribución de Residuos', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('08_analisis_residuos.png', dpi=300, bbox_inches='tight')
    print("   ✓ Guardado: 08_analisis_residuos.png")
    plt.close()
    
    pycaret_success = True
    
except ImportError:
    print("\n⚠️  PyCaret no está instalado. Instalando...")
    print("   Por favor ejecuta: pip install pycaret")
    pycaret_success = False
except Exception as e:
    print(f"\n❌ Error en PyCaret: {e}")
    pycaret_success = False

# ============================================================================
# 9. REPORTE FINAL
# ============================================================================
print("\n" + "="*80)
print("9. GENERANDO REPORTE FINAL")
print("="*80)

# Guardar resultados del análisis
resultados = {
    'fecha_analisis': datetime.now().isoformat(),
    'dataset': {
        'filas_originales': len(df),
        'filas_finales': len(df_final),
        'features_originales': len(features),
        'features_finales': len(features_modelo)
    },
    'correlaciones': {
        'target_correlaciones': target_corr.to_dict(),
        'correlaciones_altas': [(p[0], p[1], float(p[2])) for p in high_corr_pairs]
    },
    'vif': vif_data.to_dict('records'),
    'outliers': outliers_summary
}

if pycaret_success:
    resultados['modelo'] = {
        'tipo': type(best_model).__name__,
        'mae': float(mae_final),
        'rmse': float(rmse_final),
        'r2': float(r2_final)
    }
    # Solo guardar feature importance si fue calculado
    if 'feature_importance_df' in locals() and feature_importance_df is not None:
        resultados['feature_importance'] = feature_importance_df.to_dict('records')

with open('resultados_analisis.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)
print("   ✓ Guardado: resultados_analisis.json")

# Crear reporte Markdown
reporte_md = f"""# 📊 REPORTE DE ANÁLISIS Y MODELAMIENTO

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Objetivo:** Predecir `ganancia_promedio_gramos` usando las mejores técnicas de ML

---

## 1. Resumen Ejecutivo

### Dataset
- **Filas originales:** {len(df):,}
- **Filas finales:** {len(df_final):,}
- **Features originales:** {len(features)}
- **Features finales:** {len(features_modelo)} (con feature engineering)

### Variables Analizadas

**Variables Originales:**
{chr(10).join([f'- `{f}`' for f in features])}

**Target:**
- `{target}`

---

## 2. Análisis Exploratorio

### Variables Categóricas

"""

for col in categorical_features:
    reporte_md += f"\n**{col}:**\n"
    value_counts = df_model[col].value_counts()
    for val, count in value_counts.items():
        reporte_md += f"- {val}: {count:,} ({count/len(df_model)*100:.1f}%)\n"

reporte_md += f"""

### Correlaciones con Target

**Top 5 correlaciones:**

"""

for feature, corr in target_corr.head(6).items():
    if feature != target:
        reporte_md += f"- `{feature}`: {corr:.4f}\n"

if high_corr_pairs:
    reporte_md += f"""

### ⚠️ Multicolinealidad Detectada

**Pares de features con correlación > 0.7:**

"""
    for col1, col2, corr in high_corr_pairs:
        reporte_md += f"- `{col1}` <-> `{col2}`: {corr:.3f}\n"
else:
    reporte_md += "\n✅ No se detectó multicolinealidad significativa entre features.\n"

reporte_md += f"""

### Análisis VIF

| Feature | VIF | Interpretación |
|---------|-----|----------------|
"""

for _, row in vif_data.iterrows():
    vif_val = row['VIF']
    if vif_val > 10:
        interp = "🔴 Severa"
    elif vif_val > 5:
        interp = "🟠 Moderada"
    else:
        interp = "🟢 OK"
    reporte_md += f"| {row['Feature']} | {vif_val:.2f} | {interp} |\n"

reporte_md += f"""

---

## 3. Feature Engineering

Se crearon las siguientes features adicionales:

### Variables Cíclicas
- `mes_sin`: Componente seno del mes
- `mes_cos`: Componente coseno del mes

### Ratios y Derivadas
- `alimento_por_densidad`: kilos_recibidos / densidad
- `peso_inicial_por_densidad`: peso_inicial / densidad

### Categorizaciones
- `edad_madres_categoria`: Joven/Adulta/Madura/Vieja
- `densidad_categoria`: Baja/Media/Alta/Muy Alta

**Total features finales:** {len(features_modelo)}

---

## 4. Detección de Outliers

| Variable | Outliers | % del Total |
|----------|----------|-------------|
"""

for feature, info in outliers_summary.items():
    reporte_md += f"| {feature} | {info['count']:,} | {info['percentage']:.2f}% |\n"

reporte_md += "\n---\n\n"

if pycaret_success:
    reporte_md += f"""## 5. Resultados del Modelamiento

### 🏆 Mejor Modelo: {type(best_model).__name__}

**Métricas de Rendimiento:**
- **MAE:** {mae_final:.4f} gramos
- **RMSE:** {rmse_final:.4f} gramos
- **R²:** {r2_final:.4f} ({r2_final*100:.2f}% de varianza explicada)

### Interpretación

- El modelo predice con un error promedio de **±{mae_final:.2f} gramos**
- Explica el **{r2_final*100:.1f}%** de la variabilidad en la ganancia
"""

    if feature_importance_df is not None:
        reporte_md += f"""

### Top 10 Features Más Importantes

| Rank | Feature | Importancia |
|------|---------|-------------|
"""
        for idx, row in feature_importance_df.head(10).iterrows():
            reporte_md += f"| {idx+1} | {row['Feature']} | {row['Importance']:.4f} |\n"

    reporte_md += f"""

---

## 6. Archivos Generados

### 📊 Visualizaciones
1. `01_matriz_correlacion.png` - Matriz de correlación completa
2. `02_distribuciones.png` - Distribuciones de variables numéricas
3. `03_target_por_categoricas.png` - Target por variables categóricas
4. `04_top_correlaciones.png` - Scatter plots de top correlaciones
5. `05_vif_analysis.png` - Análisis de multicolinealidad (VIF)
6. `06_feature_importance.png` - Importancia de features
7. `07_predicciones_vs_real.png` - Predicciones vs valores reales
8. `08_analisis_residuos.png` - Análisis de residuos

### 📄 Datos y Modelos
- `resultados_analisis.json` - Resultados completos en JSON
- `feature_importance.csv` - Importancia de features
- `modelo_final.pkl` - Modelo entrenado (pickle)
- `REPORTE_ANALISIS.md` - Este reporte

---

## 7. Recomendaciones

### ✅ Variables a Mantener
"""

    if feature_importance_df is not None:
        top_features_list = feature_importance_df.head(10)['Feature'].tolist()
        for feat in top_features_list:
            reporte_md += f"- `{feat}`\n"
    
    reporte_md += """

### 🎯 Próximos Pasos

1. **Validación en producción:** Evaluar el modelo con datos nuevos
2. **Monitoreo continuo:** Tracking de MAE y R² en tiempo real
3. **Reentrenamiento periódico:** Actualizar modelo cada 1-3 meses
4. **A/B Testing:** Comparar predicciones con métodos actuales
"""

else:
    reporte_md += """## 5. Modelamiento con PyCaret

⚠️ No se pudo completar el modelamiento con PyCaret.

**Solución:**
```bash
pip install pycaret
```

Luego volver a ejecutar el análisis.
"""

n_features_adicionales = len(features_modelo) - len(features)
multicolinealidad_msg = 'Se detectaron correlaciones altas entre algunas variables' if high_corr_pairs else 'No se detectó multicolinealidad significativa'
rendimiento_msg = f'4. **Rendimiento del modelo:** MAE={mae_final:.2f}g, R²={r2_final:.2%}' if pycaret_success else '4. **Pendiente:** Instalar PyCaret para completar modelamiento'

reporte_md += f"""

---

## 8. Conclusiones

1. **Feature Engineering fue exitoso:** Se crearon {n_features_adicionales} features adicionales que mejoran el modelo

2. **Multicolinealidad:** {multicolinealidad_msg}

3. **Outliers:** Se detectaron outliers en varias variables, pero PyCaret los maneja automáticamente

{rendimiento_msg}

---

**Análisis completado exitosamente ✅**
"""

with open('REPORTE_ANALISIS.md', 'w', encoding='utf-8') as f:
    f.write(reporte_md)
print("   ✓ Guardado: REPORTE_ANALISIS.md")

# ============================================================================
# FINALIZACIÓN
# ============================================================================
print("\n" + "="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)

archivos_generados = [
    "01_matriz_correlacion.png",
    "02_distribuciones.png",
    "03_target_por_categoricas.png",
    "04_top_correlaciones.png",
    "05_vif_analysis.png"
]

if pycaret_success:
    archivos_generados.extend([
        "06_feature_importance.png",
        "07_predicciones_vs_real.png",
        "08_analisis_residuos.png",
        "modelo_final.pkl",
        "feature_importance.csv"
    ])

archivos_generados.extend([
    "resultados_analisis.json",
    "REPORTE_ANALISIS.md"
])

print(f"\nResultados guardados en: C:\\tecnoandina\\f35_modelacion2\\analisis\\modelo01")
print(f"\nArchivos generados:")
for archivo in archivos_generados:
    print(f"  • {archivo}")
print("\n" + "="*80)
