@echo off
echo ================================================================================
echo ANÁLISIS Y MODELAMIENTO EXHAUSTIVO CON PYCARET
echo ================================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo [1/4] Verificando dependencias...
pip show pycaret >nul 2>&1
if errorlevel 1 (
    echo.
    echo PyCaret no está instalado. Instalando dependencias (esto puede tomar varios minutos)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
) else (
    echo Dependencias OK
)

echo.
echo [2/4] Verificando otras librerías...
pip install -q pandas numpy matplotlib seaborn scipy statsmodels scikit-learn 2>nul

echo.
echo [3/4] Ejecutando análisis...
echo NOTA: Este proceso puede tomar 10-20 minutos dependiendo del hardware
echo.

python analisis_modelamiento_pycaret.py

if errorlevel 1 (
    echo.
    echo ERROR: El análisis falló
    pause
    exit /b 1
)

echo.
echo [4/4] Análisis completado exitosamente!
echo.
echo ================================================================================
echo ARCHIVOS GENERADOS:
echo ================================================================================
echo.
echo VISUALIZACIONES:
echo   - 01_matriz_correlacion.png
echo   - 02_distribuciones.png
echo   - 03_target_por_categoricas.png
echo   - 04_top_correlaciones.png
echo   - 05_vif_analysis.png
echo   - 06_feature_importance.png
echo   - 07_predicciones_vs_real.png
echo   - 08_analisis_residuos.png
echo.
echo DATOS Y MODELOS:
echo   - resultados_analisis.json
echo   - feature_importance.csv
echo   - modelo_final.pkl
echo.
echo REPORTE:
echo   - REPORTE_ANALISIS.md  (Revisar este primero!)
echo.
echo ================================================================================
echo.
pause
