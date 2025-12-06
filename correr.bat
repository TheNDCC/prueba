@echo off
REM Cambiar a la carpeta del proyecto (opcional)
cd /d "C:\Users\Nelson\Documents\repositorio\prueba"

REM Activar entorno virtual
call .env\Scripts\activate.bat

REM Ejecutar el programa
python prueba.py

REM Esperar para ver mensajes antes de cerrar
pause