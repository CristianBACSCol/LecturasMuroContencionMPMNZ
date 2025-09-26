import os
from dotenv import load_dotenv


load_dotenv()


def get_gateway_host() -> str:
    return os.getenv("HOST_GATE", "https://10.250.25.254")


def get_basic_auth_header() -> dict:
    # Usa la cabecera codificada tal como en el proyecto original
    # Se puede sustituir por variables de entorno si se desea mayor seguridad
    token = os.getenv("BASIC_TOKEN", "YWRtaW46d2FoN1BhaTl1")
    return {"Authorization": f"Basic {token}"}


def get_output_directory() -> str:
    # Directorio por defecto solicitado
    return os.getenv("OUTPUT_DIR", r"C:\\LecturasMuroContencion")


def get_timezone() -> str:
    # No forzamos tz; usaremos hora local del sistema Windows
    return os.getenv("TZ", "local")


def get_interval_hours() -> int:
    try:
        return int(os.getenv("INTERVAL_HOURS", "6"))
    except ValueError:
        return 6


