# LecturasMuroContencion

Sistema que captura lecturas del gateway y las almacena en un Excel mensual en C:\LecturasMuroContencion. Solo escribe equipos presentes en `excel_logger/nombres_map.csv`. La carpeta de salida se crea automáticamente si no existe.

## Variables de entorno (.env)

Crear `.env` en la raíz (opcional):
```
# Dirección del gateway LoadSensing
HOST_GATE=https://10.250.25.254

# Token Basic (Base64 usuario:clave) — placeholder
BASIC_TOKEN=REEMPLAZA_ESTE_TOKEN_BASE64

# Carpeta de salida (por defecto: C:\LecturasMuroContencion)
# OUTPUT_DIR=C:\LecturasMuroContencion

# Intervalo de captura en horas
INTERVAL_HOURS=6
```

## Pasos (Windows, PowerShell)

1) Crear entorno virtual en la raíz del repo:
```
python -m venv venv
```

2) Activar entorno virtual:
```
.\venv\Scripts\Activate.ps1
```

3) Instalar dependencias:
```
pip install -r excel_logger\requirements.txt
```

4) Compilar EXE sin consola (oculto) desde `excel_logger/`:
```
cd excel_logger
pyinstaller --noconfirm --clean --noconsole --name LecturasMuroContencion --paths . --paths .. --add-data "nombres_map.csv;excel_logger" --collect-all openpyxl .\runner.py
```
Genera `dist\LecturasMuroContencion\LecturasMuroContencion.exe`.

## Servicio de Windows (NSSM)

1) Copia `dist\LecturasMuroContencion\` a `C:\excel_logger\`
2) Crea `C:\LecturasMuroContencion` (si no existe)
3) Instala NSSM en `C:\nssm\nssm.exe`
4) Instala el servicio (Administrador):
```
C:\nssm\nssm.exe install LecturasMuroContencion C:\excel_logger\LecturasMuroContencion.exe
C:\nssm\nssm.exe set LecturasMuroContencion AppDirectory C:\excel_logger
C:\nssm\nssm.exe set LecturasMuroContencion Start SERVICE_AUTO_START
C:\nssm\nssm.exe set LecturasMuroContencion AppStdout C:\excel_logger\logs\service.out.log
C:\nssm\nssm.exe set LecturasMuroContencion AppStderr C:\excel_logger\logs\service.err.log
```
5) Iniciar y verificar:
```
sc start LecturasMuroContencion
sc qc LecturasMuroContencion
```
6) Recuperación ante fallos (opcional):
```
sc failure LecturasMuroContencion reset= 0 actions= restart/60000
```
7) Desinstalar:
```
sc stop LecturasMuroContencion
C:\nssm\nssm.exe remove LecturasMuroContencion confirm
```

