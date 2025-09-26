@echo off
setlocal
REM Construir ejecutable standalone con PyInstaller
cd /d %~dp0\..

REM Instalar PyInstaller en el entorno actual
python -m pip install --upgrade pip | cat
python -m pip install pyinstaller==6.10.0 | cat

REM Limpiar builds previas
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Empaquetar runner como consola, incluir archivo de nombres
pyinstaller --noconfirm ^
  --clean ^
  --name LecturasMuroContencion ^
  --paths . ^
  --add-data "excel_logger\\nombres_map.csv;excel_logger" ^
  --collect-all openpyxl ^
  excel_logger\\runner.py

echo.
echo Build finalizado. Ejecutable en dist\\LecturasMuroContencion\\LecturasMuroContencion.exe
endlocal

