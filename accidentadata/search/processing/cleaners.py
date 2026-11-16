"""Módulo de limpieza y normalización básica para datos de accidentalidad vial.

Provee funciones puras y reutilizables para transformar textos, fechas,
números y códigos geográficos procedentes de fuentes abiertas.
"""

from datetime import date, datetime
import re
from typing import Any, Optional

# Valores que en fuentes abiertas representan ausencia de datos
NULL_STRINGS = {
    "",
    "null",
    "none",
    "nan",
    "n/a",
    "na",
    "nd",
    "no aplica",
    "no reporta",
    "no reportado",
    "sin informacion",
    "sin información",
    "sin dato",
    "sin datos",
    "desconocido",
    "por establecer",
    "-",
    "—",
}


def clean_text(value: Any, default: str = "") -> str:
    """Limpia cadenas de texto: elimina espacios sobrantes y detecta valores nulos."""
    if value is None:
        return default

    text = str(value).strip()
    # Colapsar espacios múltiples internos
    text = re.sub(r"\s+", " ", text)

    if text.lower() in NULL_STRINGS:
        return default

    return text


def clean_name(value: Any, default: str = "") -> str:
    """Limpia y estandariza nombres propios, municipios y departamentos en mayúsculas.

    Elimina sufijos comunes de las fuentes de la Policía Nacional como '(CT)' (Cabecera y Total).
    """
    text = clean_text(value, default=default)
    if not text or text == default:
        return default

    # Eliminar sufijos como '(CT)'
    text = re.sub(r"\s*\(\s*CT\s*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()

    return text.upper()


def clean_int(
    value: Any,
    default: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
) -> Optional[int]:
    """Convierte de forma segura un valor a entero, validando rangos."""
    if value is None:
        return default

    if isinstance(value, (int, float)):
        try:
            num = int(value)
        except (ValueError, OverflowError):
            return default
    else:
        text = str(value).strip()
        if not text or text.lower() in NULL_STRINGS:
            return default
        try:
            # Soportar floats en string como "2024.0"
            num = int(float(text))
        except (ValueError, OverflowError):
            return default

    if min_val is not None and num < min_val:
        return default
    if max_val is not None and num > max_val:
        return default

    return num


def clean_date_str(value: Any) -> Optional[str]:
    """Normaliza diversos formatos de fecha a estándar ISO (AAAA-MM-DD o AAAA-MM).

    Formatos soportados:
    - MM/AAAA (RUNT vehículos): retorna 'AAAA-MM'
    - DD/MM/AAAA (Policía homicidios): retorna 'AAAA-MM-DD'
    - AAAA-MM-DDTHH:MM:SS.sss (Policía lesiones ISO): retorna 'AAAA-MM-DD'
    - AAAA-MM-DD: retorna 'AAAA-MM-DD'
    """
    if value is None:
        return None

    text = str(value).strip()
    if not text or text.lower() in NULL_STRINGS:
        return None

    # Formato ISO con hora: 2026-09-30T00:00:00.000
    if "T" in text:
        text = text.split("T")[0].strip()

    # Formato AAAA-MM-DD
    iso_match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", text)
    if iso_match:
        y, m, d = int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3))
        try:
            val_date = date(y, m, d)
            return val_date.isoformat()
        except ValueError:
            return None

    # Formato DD/MM/AAAA
    dmy_match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", text)
    if dmy_match:
        d, m, y = int(dmy_match.group(1)), int(dmy_match.group(2)), int(dmy_match.group(3))
        try:
            val_date = date(y, m, d)
            return val_date.isoformat()
        except ValueError:
            return None

    # Formato MM/AAAA (usado por el RUNT)
    my_match = re.match(r"^(\d{1,2})/(\d{4})$", text)
    if my_match:
        m, y = int(my_match.group(1)), int(my_match.group(2))
        if 1 <= m <= 12 and 1900 <= y <= 2100:
            return f"{y:04d}-{m:02d}"
        return None

    return None


def extract_date_parts(date_iso: Optional[str]) -> dict:
    """Extrae año, mes y día de una fecha ISO normalizada ('AAAA-MM-DD' o 'AAAA-MM')."""
    parts = {"anio": None, "mes": None, "dia": None}
    if not date_iso:
        return parts

    tokens = date_iso.split("-")
    if len(tokens) >= 2:
        try:
            parts["anio"] = int(tokens[0])
            parts["mes"] = int(tokens[1])
        except ValueError:
            pass
    if len(tokens) >= 3:
        try:
            parts["dia"] = int(tokens[2])
        except ValueError:
            pass

    return parts


def clean_dane_code(value: Any, expected_digits: int = 5) -> str:
    """Estandariza códigos DANE y DIVIPOLA a número fijo de dígitos con ceros a la izquierda.

    - Para departamento (expected_digits=2): retorna ej. '05', '76'.
    - Para municipio DIVIPOLA (expected_digits=5): retorna ej. '05001', '76001'.
    - Si llega un código DANE de 8 dígitos (ej. '19130000'):
      extrae los primeros 5 dígitos ('19130') para municipio o los 2 primeros ('19') para depto.
    """
    if value is None:
        return ""

    raw = str(value).strip()
    # Eliminar posibles decimales si venía como float tipo "76001.0"
    if "." in raw:
        raw = raw.split(".")[0]

    # Dejar solo dígitos
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return ""

    # Si es un código DANE de 8 dígitos de la DIJIN (ej. 19130000):
    if len(digits) == 8:
        if expected_digits == 2:
            return digits[:2]
        if expected_digits == 5:
            return digits[:5]

    # Rellenar con ceros a la izquierda si tiene menos dígitos
    if len(digits) <= expected_digits:
        return digits.zfill(expected_digits)

    # Si tiene más dígitos que lo esperado, tomar el prefijo
    return digits[:expected_digits]
