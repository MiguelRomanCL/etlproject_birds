@echo off
echo ================================================================================
echo SISTEMA DE PREDICCIÓN - PRODUCCIÓN 01
echo ================================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado
    pause
    exit /b 1
)

echo Selecciona el modo de ejecución:
echo.
echo 1. Uso Simple (Recomendado para principiantes)
echo 2. Ejemplos Completos (Todos los ejemplos)
echo 3. Predicción desde CSV personalizado
echo.
set /p opcion="Opción (1-3): "

if "%opcion%"=="1" (
    echo.
    echo Ejecutando modo simple...
    python uso_simple.py
) else if "%opcion%"=="2" (
    echo.
    echo Ejecutando ejemplos completos...
    python predictor.py
) else if "%opcion%"=="3" (
    echo.
    set /p archivo="Ruta del archivo CSV: "
    python -c "from predictor import PredictorGanancia; p=PredictorGanancia(); p.predecir_lote('%archivo%')"
) else (
    echo Opción inválida
)

echo.
pause
