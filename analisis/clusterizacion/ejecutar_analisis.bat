@echo off
echo ================================================================================
echo ANALISIS DE CLUSTERIZACION - TECNOANDINA
echo ================================================================================
echo.

echo Verificando instalacion de Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)
echo.

echo Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo Dependencias instaladas correctamente
echo.

echo ================================================================================
echo Ejecutando analisis exhaustivo de clusterizacion...
echo ================================================================================
echo.

python analisis_clusterizacion_avanzado.py

echo.
echo ================================================================================
echo ANALISIS COMPLETADO
echo ================================================================================
echo.
echo Los resultados se encuentran en esta carpeta:
echo   - comparacion_estrategias.png
echo   - kmeans_metricas.png
echo   - visualizacion_clusters.png
echo   - dendrograma.png
echo   - REPORTE_CLUSTERIZACION.md
echo   - comparacion_estrategias.csv
echo   - resultados_detallados.json
echo   - dataset_con_clusters.csv
echo.

pause
