@echo off
title Compilar peya.exe - Pollos KM9
cd /d "%~dp0"

echo ===========================================
echo  Compilando peya.exe con PyInstaller
echo ===========================================
echo.

where py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado en PATH.
    echo Instale Python 3.12+ desde https://python.org
    echo y marque "Add python.exe to PATH" durante la instalacion.
    pause
    exit /b 1
)

if not exist .venv\Scripts\activate.bat (
    echo Creando entorno virtual...
    py -m venv .venv
    if errorlevel 1 (
        echo ERROR: no se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: fallo la instalacion de dependencias.
    pause
    exit /b 1
)

echo.
echo Compilando peya.exe (esto puede tardar varios minutos)...
echo.
pyinstaller build_peya.spec --clean
if errorlevel 1 (
    echo.
    echo ERROR: fallo la compilacion. Revise los mensajes arriba.
    pause
    exit /b 1
)

echo.
echo ===========================================
if exist dist\peya.exe (
    echo  EXITO: dist\peya.exe generado correctamente
    echo ===========================================
    echo.
    echo Puede copiar dist\peya.exe a cualquier PC Windows.
    echo Doble clic para abrir. No requiere Python instalado.
) else (
    echo  ERROR: dist\peya.exe no encontrado
    echo ===========================================
)
echo.
pause