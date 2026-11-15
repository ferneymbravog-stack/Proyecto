"""Transformadores específicos por fuente de datos de accidentalidad.

Convierte los registros sin procesar (strings heterogéneos y con nulos)
en registros estructurados con tipos de datos nativos, normalización
geográfica y temporal, y tratamiento predecible de valores ausentes.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .cleaners import (
    clean_dane_code,
    clean_date_str,
    clean_int,
    clean_name,
    clean_text,
    extract_date_parts,
)

CURRENT_YEAR = datetime.now().year


def transform_runt_vehicle(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia y normaliza un registro del RUNT (Vehículos involucrados).

    Unidad de conteo: 1 vehículo involucrado por registro.
    La fecha en la fuente solo contiene mes y año ('MM/AAAA').
    """
    date_iso = clean_date_str(raw.get("fecha_accidente"))
    date_parts = extract_date_parts(date_iso)

    modelo = clean_int(raw.get("modelo_vehiculo"), min_val=1900, max_val=CURRENT_YEAR + 2)
    edad = clean_int(raw.get("edad_vehiculo"), min_val=0, max_val=150)

    # Si la edad es nula o inválida pero tenemos año de accidente y modelo, calcularla de forma predecible
    if edad is None and modelo and date_parts.get("anio"):
        calc_edad = date_parts["anio"] - modelo
        if 0 <= calc_edad <= 150:
            edad = calc_edad

    return {
        "marca_vehiculo": clean_name(raw.get("marca_vehiculo"), default="NO REPORTADO"),
        "modelo_vehiculo": modelo,
        "tipo_vehiculo": clean_name(raw.get("tipo_vehiculo"), default="NO REPORTADO"),
        "edad_vehiculo": edad,
        "fecha_accidente": date_iso or "",
        "anio": date_parts["anio"],
        "mes": date_parts["mes"],
        "gravedad_accidente": clean_name(raw.get("gravedad_accidente"), default="NO REPORTADO"),
        "departamento": clean_name(raw.get("departamento_accidente"), default="NO REPORTADO"),
        "municipio": clean_name(raw.get("municipio_accidente"), default="NO REPORTADO"),
        "autoridad_transito": clean_text(raw.get("autoridad_de_transito"), default="NO REPORTADO"),
        "cantidad_vehiculos": 1,
    }


def transform_police_fatality(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia y normaliza un registro de Homicidios en siniestros viales (DIJIN).

    Unidad de conteo: Víctimas (suma de 'cantidad').
    La fecha en la fuente llega como texto 'DD/MM/AAAA'.
    El 'codigo_dane' tiene 8 dígitos (ej. 19130000); los 5 primeros corresponden al municipio DIVIPOLA.
    """
    date_iso = clean_date_str(raw.get("fecha_hecho"))
    date_parts = extract_date_parts(date_iso)

    dane_raw = raw.get("codigo_dane")
    cod_depto = clean_dane_code(dane_raw, expected_digits=2)
    cod_muni = clean_dane_code(dane_raw, expected_digits=5)

    cantidad = clean_int(raw.get("cantidad"), default=1, min_val=0)
    if cantidad is None:
        cantidad = 1

    return {
        "departamento": clean_name(raw.get("departamento"), default="NO REPORTADO"),
        "municipio": clean_name(raw.get("municipio"), default="NO REPORTADO"),
        "codigo_dane_original": clean_text(dane_raw, default=""),
        "cod_depto": cod_depto,
        "cod_muni": cod_muni,
        "armas_medios": clean_name(raw.get("armas_medios"), default="NO REPORTADO"),
        "fecha_hecho": date_iso or "",
        "anio": date_parts["anio"],
        "mes": date_parts["mes"],
        "dia": date_parts["dia"],
        "genero": clean_name(raw.get("genero"), default="NO REPORTADO"),
        "grupo_etario": clean_name(raw.get("grupo_etar_o"), default="NO REPORTADO"),
        "conducta": clean_text(raw.get("descripci_n_conducta"), default="HOMICIDIO CULPOSO"),
        "cantidad": cantidad,
    }


def transform_police_injury(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia y normaliza un registro de Lesiones en accidentes de tránsito (Mindefensa).

    Unidad de conteo: Víctimas (suma de 'cantidad').
    La fecha en la fuente llega en formato ISO 'AAAA-MM-DDT00:00:00.000'.
    """
    date_iso = clean_date_str(raw.get("fecha_hecho"))
    date_parts = extract_date_parts(date_iso)

    cod_depto = clean_dane_code(raw.get("cod_depto"), expected_digits=2)
    cod_muni = clean_dane_code(raw.get("cod_muni"), expected_digits=5)

    cantidad = clean_int(raw.get("cantidad"), default=1, min_val=0)
    if cantidad is None:
        cantidad = 1

    return {
        "fecha_hecho": date_iso or "",
        "anio": date_parts["anio"],
        "mes": date_parts["mes"],
        "dia": date_parts["dia"],
        "cod_depto": cod_depto,
        "departamento": clean_name(raw.get("departamento"), default="NO REPORTADO"),
        "cod_muni": cod_muni,
        "municipio": clean_name(raw.get("municipio"), default="NO REPORTADO"),
        "cantidad": cantidad,
    }


TRANSFORMERS = {
    "runt_vehicles": transform_runt_vehicle,
    "police_fatalities": transform_police_fatality,
    "police_injuries": transform_police_injury,
}


def clean_record(dataset_key: str, raw_record: Any) -> Optional[Dict[str, Any]]:
    """Transforma un registro individual de acuerdo al catálogo de la fuente."""
    if not isinstance(raw_record, dict):
        return None

    transformer = TRANSFORMERS.get(dataset_key)
    if not transformer:
        # Si la fuente no tiene transformador específico, retornar limpieza genérica
        return {k: clean_text(v) for k, v in raw_record.items()}

    return transformer(raw_record)


def clean_records(dataset_key: str, raw_records: List[Any]) -> List[Dict[str, Any]]:
    """Transforma una lista de registros asegurando que ninguno provoque errores bloqueantes."""
    cleaned = []
    for item in raw_records:
        rec = clean_record(dataset_key, item)
        if rec is not None:
            cleaned.append(rec)
    return cleaned
