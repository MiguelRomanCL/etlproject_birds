@echo off
echo ================================================================================
echo PROYECCIÓN DE GANANCIAS - MODELO 03
echo ================================================================================
echo.
echo Este script proyecta ganancias para crianzas vigentes usando el Modelo 03
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo Python detectado: 
python --version
echo.

REM Verificar que existe el archivo de entrada
set INPUT_FILE=..\work_data\resumen_crianzas_para_proyeccion.csv
if not exist "%INPUT_FILE%" (
    echo ERROR: No se encuentra el archivo de entrada
    echo Buscando: %INPUT_FILE%
    echo.
    echo Por favor verifica que el archivo exista en la carpeta work_data
    pause
    exit /b 1
)

echo Archivo de entrada encontrado: %INPUT_FILE%
echo.

REM Ejecutar script
echo Ejecutando proyeccion...
echo.
python 04_proyeccion_ganancias.py

REM Verificar resultado
if errorlevel 1 (
    echo.
    echo ================================================================================
    echo ERROR: La proyeccion fallo
    echo ================================================================================
    echo.
    echo Revisa los mensajes de error arriba para mas detalles
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo EXITO: Proyeccion completada
    echo ================================================================================
    echo.
    echo El archivo con proyecciones fue guardado en:
    echo ..\work_data\resumen_crianzas_con_proyeccion.csv
)

echo.
pause
