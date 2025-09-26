# Excel Logger mensual

## Configuración

Crear un archivo `.env` en la raíz del proyecto (o variables del sistema):

```
HOST_GATE=https://10.250.25.254
BASIC_TOKEN=YWRtaW46d2FoN1BhaTl1
OUTPUT_DIR=output
INTERVAL_HOURS=6
```

## Ejecutar

- Instalar dependencias (opcional si ya existen en tu entorno):
```
pip install -r excel_logger/requirements.txt
```

- Lanzar:
```
python -m excel_logger.runner
```

Genera archivos mensuales como `LecturasMuroContencionMarzo2025.xlsx` con columnas: Fecha / Dataloger / Nombre / Lectura.

## Compilar a EXE (offline)

Compila en una sola línea desde `excel_logger/` (PowerShell):
```
pyinstaller --noconfirm --clean --name LecturasMuroContencion --paths . --paths .. --add-data "nombres_map.csv;excel_logger" --collect-all openpyxl .\runner.py
```
Genera `dist/LecturasMuroContencion/LecturasMuroContencion.exe`.

2) Copia a la máquina offline el directorio `dist/LecturasMuroContencion/` completo. Puedes llevar también tu `.env` (opcional) para HOST y ruta de salida.

3) En la máquina destino, crea/edita `excel_logger/nombres_map.csv` según tu inventario y ejecuta `excel_logger.exe`. Los Excel se guardarán en `output/` junto al ejecutable (o en `OUTPUT_DIR` si está configurado).

## Variables de entorno (.env ejemplo)

Crea un archivo `.env` en la raíz del proyecto con variables opcionales:

```
# Dirección del gateway LoadSensing
HOST_GATE=https://10.250.25.254

# Token Basic (Base64 usuario:clave). Ejemplo de placeholder, remplázalo si aplica
BASIC_TOKEN=REEMPLAZA_ESTE_TOKEN_BASE64

# Carpeta de salida (por defecto: C:\LecturasMuroContencion)
# OUTPUT_DIR=C:\LecturasMuroContencion

# Intervalo de captura en horas
INTERVAL_HOURS=6
```

## Instalar dependencias en entorno virtual (Windows)

1) Abre PowerShell en la raíz del proyecto
2) Crea y activa entorno virtual:
```
python -m venv venv
.\venvin\\activate  # PowerShell puede requerir: .\venv\Scripts\Activate.ps1
```
3) Instala dependencias mínimas:
```
pip install -r excel_logger\requirements.txt
```
4) Ejecuta en modo desarrollo:
```
python -m excel_logger.runner
```

## Ejecutar como Servicio de Windows (Opción recomendada con NSSM)

Esta opción arranca automáticamente SIN iniciar sesión.

1) Descarga NSSM (Non-Sucking Service Manager) y copia `nssm.exe` a `C:\nssm\nssm.exe`
2) Compila el ejecutable (sección “Compilar a EXE”) → tendrás `dist\excel_logger\excel_logger.exe`
3) Copia el folder `dist\excel_logger\` a `C:\excel_logger\`
4) Crea la carpeta de lecturas si no existe: `C:\LecturasMuroContencion`
5) Instala el servicio (PowerShell como Administrador):
```
C:\nssm\nssm.exe install ExcelLogger C:\excel_logger\excel_logger.exe
C:\nssm\nssm.exe set ExcelLogger AppDirectory C:\excel_logger
C:\nssm\nssm.exe set ExcelLogger Start SERVICE_AUTO_START
C:\nssm\nssm.exe set ExcelLogger AppStdout C:\excel_logger\logs\service.out.log
C:\nssm\nssm.exe set ExcelLogger AppStderr C:\excel_logger\logs\service.err.log
C:\nssm\nssm.exe set ExcelLogger AppRotateFiles 1
C:\nssm\nssm.exe set ExcelLogger AppRotateOnline 1
```
6) Inicia y verifica:
```
sc start ExcelLogger
sc qc ExcelLogger
```
7) (Opcional) Configura recuperación ante fallos para reiniciar automáticamente:
```
sc failure ExcelLogger reset= 0 actions= restart/60000
```
8) Para desinstalar el servicio:
```
sc stop ExcelLogger
C:\nssm\nssm.exe remove ExcelLogger confirm
```

Notas:
- El servicio corre por defecto como LocalSystem. Si necesitas escribir en recursos de red, cambia la cuenta del servicio en `services.msc` → pestaña “Iniciar sesión”.
- El ejecutable registra logs en `C:\excel_logger\logs\`.
- Asegura permisos de escritura en `C:\LecturasMuroContencion` para la cuenta del servicio.

