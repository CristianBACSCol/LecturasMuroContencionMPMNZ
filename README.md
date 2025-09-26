# LecturasMuroContencionMPMNZ

Captura lecturas del gateway y las guarda en un Excel mensual en `C:\LecturasMuroContencion`. Solo registra equipos definidos en `excel_logger/nombres_map.csv`. La carpeta de salida se crea automáticamente si no existe.

## Variables (.env en la raíz)
```
HOST_GATE=https://10.250.25.254
BASIC_TOKEN=REEMPLAZA_ESTE_TOKEN_BASE64
# OUTPUT_DIR=C:\LecturasMuroContencion
INTERVAL_HOURS=6
```

## Instalación y compilación (Windows, PowerShell)
1) Crear venv
```
python -m venv venv
```
2) Activar venv
```
.\venv\Scripts\Activate.ps1
```
3) Instalar dependencias
```
pip install -r requirements.txt
```
4) Compilar EXE sin ventana (desde `excel_logger/`)
```
cd excel_logger
pyinstaller --noconfirm --clean --noconsole --name LecturasMuroContencionMPMNZ --paths . --paths .. --add-data "nombres_map.csv;excel_logger" --collect-all openpyxl .\runner.py
```
Resultado: `excel_logger\dist\LecturasMuroContencionMPMNZ\LecturasMuroContencionMPMNZ.exe`.

## Ejecutar en segundo plano
- Manual (oculto) desde PowerShell:
```
Start-Process -WindowStyle Hidden -FilePath "C:\ruta\LecturasMuroContencionMPMNZ.exe"
```
- Servicio Windows (recomendado, inicia sin sesión):
```
# Copia la carpeta dist a C:\LecturasMuroContencionMPMNZ
# Crea C:\LecturasMuroContencion si no existe
# Instala NSSM en C:\nssm\nssm.exe
C:\nssm\nssm.exe install LecturasMuroContencionMPMNZ C:\LecturasMuroContencionMPMNZ\LecturasMuroContencionMPMNZ.exe
C:\nssm\nssm.exe set LecturasMuroContencionMPMNZ AppDirectory C:\LecturasMuroContencionMPMNZ
C:\nssm\nssm.exe set LecturasMuroContencionMPMNZ Start SERVICE_AUTO_START
C:\nssm\nssm.exe set LecturasMuroContencionMPMNZ AppStdout C:\LecturasMuroContencionMPMNZ\logs\service.out.log
C:\nssm\nssm.exe set LecturasMuroContencionMPMNZ AppStderr C:\LecturasMuroContencionMPMNZ\logs\service.err.log
sc start LecturasMuroContencionMPMNZ
```
Desinstalar:
```
sc stop LecturasMuroContencionMPMNZ
C:\nssm\nssm.exe remove LecturasMuroContencionMPMNZ confirm
```

## Notas
- PyInstaller es una herramienta de build, no está en `requirements.txt`.
- Si ejecutas el EXE desde una consola visible y luego cierras esa ventana, el proceso terminará. Usa `Start-Process -WindowStyle Hidden` o instálalo como servicio para ejecutarlo oculto.

