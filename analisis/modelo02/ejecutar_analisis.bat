@echo off
echo ================================================================================
echo MODELO 02 - VERSION LIMPIA SIN MULTICOLINEALIDAD
echo ================================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip show pycaret >nul 2>&1
if errorlevel 1 (
    echo.
    echo Instalando PyCaret...
    pip install -r requirements.txt
)

echo.
echo [2/3] Ejecutando analisis del modelo limpio...
echo Tiempo estimado: 5-10 minutos
echo.

python analisis_modelamiento_limpio.py

if errorlevel 1 (
    echo.
    echo ERROR: El analisis fallo
    pause
    exit /b 1
)

echo.
echo [3/3] Analisis completado!
echo.
echo ================================================================================
echo ARCHIVOS GENERADOS:
echo ================================================================================
echo.
echo VISUALIZACIONES:
echo   - 01_matriz_correlacion_limpia.png
echo   - 02_distribuciones_limpias.png
echo   - 03_comparacion_vif.png (Comparacion Modelo 01 vs 02)
echo   - 04_top_correlaciones_limpias.png
echo   - 05_feature_importance_limpio.png
echo   - 06_predicciones_vs_real_limpio.png
echo   - 07_analisis_residuos_limpio.png
echo.
echo MODELO:
echo   - modelo_limpio_final.pkl
echo   - feature_importance_limpio.csv
echo.
echo REPORTES:
echo   - REPORTE_MODELO_LIMPIO.md (Revisar este primero!)
echo   - resultados_modelo_limpio.json
echo.
echo ================================================================================
echo.
pause
