@echo off
echo ================================================================================
echo ANÁLISIS DE CLUSTERIZACIÓN SIMPLIFICADO
echo Variables: Sexo, Densidad, Tipo de Construcción
echo ================================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip install -q pandas numpy matplotlib seaborn scikit-learn scipy tabulate 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install pandas numpy matplotlib seaborn scikit-learn scipy tabulate
)

echo.
echo [2/3] Ejecutando análisis...
echo Este proceso tomará 2-5 minutos...
echo.

python analisis_clusterizacion_simplificado.py

if errorlevel 1 (
    echo.
    echo ERROR: El análisis falló
    pause
    exit /b 1
)

echo.
echo [3/3] Análisis completado exitosamente!
echo.
echo ================================================================================
echo ARCHIVOS GENERADOS:
echo ================================================================================
echo.
echo VISUALIZACIONES:
echo   - comparacion_estrategias.png
echo   - kmeans_metricas.png
echo   - visualizacion_clusters.png
echo   - dendrograma.png
echo.
echo DATOS:
echo   - comparacion_estrategias.csv
echo   - resultados_detallados.json
echo   - dataset_con_clusters.csv
echo.
echo REPORTE:
echo   - REPORTE_CLUSTERIZACION.md  (Revisar este primero!)
echo.
echo ================================================================================
echo.
pause
