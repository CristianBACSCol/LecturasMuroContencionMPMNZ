import csv
import os
import re
from typing import Dict


def load_name_mapping(csv_path: str = "excel_logger/nombres_map.csv") -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    # Resolver ruta absoluta relativa a este archivo para evitar CWDs distintos
    base_dir = os.path.dirname(__file__)
    abs_path = csv_path if os.path.isabs(csv_path) else os.path.join(base_dir, os.path.basename(csv_path))
    if not os.path.exists(abs_path):
        return mapping
    try:
        with open(abs_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                raw_key = (row.get("Dataloger") or "")
                # Normalizar: quitar espacios y cualquier carácter no dígito/índice
                key = re.sub(r"\s+", "", raw_key.strip())
                value = (row.get("Nombre") or "").strip()
                if key:
                    mapping[key] = value
    except Exception:
        return mapping
    return mapping


