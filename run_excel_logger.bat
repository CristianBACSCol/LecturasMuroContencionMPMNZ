@echo off
setlocal
cd /d %~dp0\..
REM Activar entorno si aplica
REM call venv\Scripts\activate
python -m excel_logger.runner
endlocal

