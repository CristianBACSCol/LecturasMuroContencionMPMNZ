import logging
import time
from datetime import datetime
from typing import List, Dict
import os
import sys
import re

import requests

# Permitir ejecución directa desde la carpeta excel_logger
_CURRENT_DIR = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from app.api.provider import dataLoggers
from app.api.loads import data_quest

try:
    # Cuando se ejecuta como paquete: python -m excel_logger.runner
    from .config import get_gateway_host, get_basic_auth_header, get_output_directory, get_interval_hours
    from .excel_writer import get_excel_path, append_rows
    from .logger import configure_logging
    from .name_mapping import load_name_mapping
except ImportError:
    # Cuando se ejecuta directamente: python runner.py
    from excel_logger.config import get_gateway_host, get_basic_auth_header, get_output_directory, get_interval_hours
    from excel_logger.excel_writer import get_excel_path, append_rows
    from excel_logger.logger import configure_logging
    from excel_logger.name_mapping import load_name_mapping


def to_numeric(value: float | int) -> float:
    try:
        return round(float(value), 3)
    except Exception:
        return 0.0


def format_timestamp(dt: datetime) -> datetime:
    # Para que Excel lo reconozca como fecha, escribimos datetime nativo;
    # en el escritor aplicamos el number_format "yyyy/mm/dd hh:mm".
    return dt


def build_rows(now: datetime, host: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    mapping = load_name_mapping()
    for item in dataLoggers:
        path = item["path"].replace("${host}", host) if "${host}" in item["path"] else item["path"]
        try:
            info = data_quest(path)
            if len(item["instance"]) == 1:
                value = info["value"][0]["value"] if info["value"] else 0
                name_value = f"{info['name']}"
                datalogger_key = name_value.replace(" ", "")
                # Omitir si no está en el mapa
                if datalogger_key not in mapping:
                    continue
                rows.append(
                    {
                        "Fecha": format_timestamp(now),
                        "Dataloger": datalogger_key,
                        "Nombre": mapping.get(datalogger_key, ""),
                        "Lectura": to_numeric(value),
                    }
                )
            else:
                for index, instance in enumerate(item["instance"]):
                    name = f"{info['name']} {index}"
                    try:
                        value = info["value"][index]["value"]
                    except Exception:
                        value = 0
                    datalogger_key = name.replace(" ", "")
                    # Omitir si no está en el mapa
                    if datalogger_key not in mapping:
                        continue
                    rows.append(
                        {
                            "Fecha": format_timestamp(now),
                            "Dataloger": datalogger_key,
                            "Nombre": mapping.get(datalogger_key, ""),
                            "Lectura": to_numeric(value),
                        }
                    )
        except Exception as exc:
            logging.error("Fallo al obtener lectura de %s: %s", path, exc)
            # Registrar 0 por cada instancia configurada
            if len(item["instance"]) == 1:
                # Derivar nodeId desde la URL para coincidir con el mapeo
                m = re.search(r"/nodes/(\d+)", path)
                datalogger_key = m.group(1) if m else path.replace(" ", "")
                # Omitir si no está en el mapa
                if datalogger_key not in mapping:
                    continue
                nombre = mapping.get(datalogger_key, "")
                lectura = "Fallo"
                rows.append(
                    {
                        "Fecha": format_timestamp(now),
                        "Dataloger": datalogger_key,
                        "Nombre": nombre,
                        "Lectura": lectura,
                    }
                )
            else:
                for index, instance in enumerate(item["instance"]):
                    # Derivar clave compuesta nodeId+index
                    m = re.search(r"/nodes/(\d+)", path)
                    base_id = m.group(1) if m else path
                    datalogger_key = f"{base_id}{index}"
                    # Omitir si no está en el mapa
                    if datalogger_key not in mapping:
                        continue
                    nombre = mapping.get(datalogger_key, "")
                    lectura = "Fallo"
                    rows.append(
                        {
                            "Fecha": format_timestamp(now),
                            "Dataloger": datalogger_key,
                            "Nombre": nombre,
                            "Lectura": lectura,
                        }
                    )
    return rows


def run_forever() -> None:
    configure_logging()
    host = get_gateway_host()
    headers = get_basic_auth_header()
    output_dir = get_output_directory()
    interval_hours = get_interval_hours()

    logging.info("Iniciando logger mensual hacia %s, intervalo %s h", host, interval_hours)

    # Nota: data_quest ya usa headers y verify False internamente
    while True:
        start = time.time()
        now = datetime.now()
        try:
            rows = build_rows(now, host)
            excel_path = get_excel_path(output_dir, now)
            append_rows(excel_path, rows)
            logging.info("Guardadas %s lecturas en %s", len(rows), excel_path)
        except Exception as exc:
            logging.exception("Error en el ciclo de captura: %s", exc)

        elapsed = time.time() - start
        sleep_seconds = max(1, int(interval_hours * 3600 - elapsed))
        logging.info("Durmiento %s segundos", sleep_seconds)
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    run_forever()


