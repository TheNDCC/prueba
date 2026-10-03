@echo off
title Procesador PedidosYa - Pollos KM9
cd /d "%~dp0"

if exist peya.exe (
    start "" peya.exe
) else (
    echo.
    echo No se encontro peya.exe en esta carpeta.
    echo.
    echo Si tiene el codigo fuente, ejecute build.bat para compilarlo.
    echo Si tiene peya.exe, asegurese de que esta en la misma carpeta
    echo que correr.bat.
    echo.
)