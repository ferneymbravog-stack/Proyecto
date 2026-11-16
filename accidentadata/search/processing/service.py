"""Servicio reutilizable para procesar, limpiar y resumir registros de accidentalidad.

Integra el cliente Socrata con los transformadores específicos y provee
resultados listos para ser consumidos por vistas, filtros y paneles de estadísticas.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import (
    DEFAULT_SAMPLE_SIZE,
    MAX_SAMPLE_SIZE,
    UnknownDatasetError,
    get_dataset,
)
from accidentadata.data_sources.socrata_client import SocrataClient, SocrataError

from .statistics import StatisticalSummary, build_statistical_summary
from .transformers import clean_records


@dataclass
class QualityStats:
    total_records: int = 0
    total_metric: int = 0
    metric_label: str = "Registros"
    valid_dates_count: int = 0
    complete_geo_count: int = 0
    missing_values_handled: int = 0


@dataclass
class ProcessedSampleResult:
    key: str
    dataset: dict
    raw_records: list = field(default_factory=list)
    records: list = field(default_factory=list)
    table_rows: list = field(default_factory=list)
    columns: list = field(default_factory=list)
    stats: QualityStats = field(default_factory=QualityStats)
    summary: Optional[StatisticalSummary] = None
    error: str = ""

    @property
    def is_empty(self) -> bool:
        return not self.error and not self.records


def calculate_stats(key: str, cleaned_records: List[Dict[str, Any]]) -> QualityStats:
    """Calcula métricas de calidad y totales de acuerdo a la unidad de conteo oficial."""
    stats = QualityStats(total_records=len(cleaned_records))

    if key == "runt_vehicles":
        stats.metric_label = "Vehículos involucrados"
        stats.total_metric = sum(r.get("cantidad_vehiculos", 1) for r in cleaned_records)
    elif key in ("police_fatalities", "police_injuries"):
        stats.metric_label = "Víctimas reportadas"
        stats.total_metric = sum(r.get("cantidad", 0) for r in cleaned_records)
    else:
        stats.total_metric = len(cleaned_records)

    # Conteo de calidad
    for r in cleaned_records:
        # Fechas válidas
        date_val = r.get("fecha_accidente") or r.get("fecha_hecho")
        if date_val:
            stats.valid_dates_count += 1

        # Ubicación completa
        depto = r.get("departamento")
        muni = r.get("municipio")
        if depto and depto != "NO REPORTADO" and muni and muni != "NO REPORTADO":
            stats.complete_geo_count += 1

        # Conteo de campos donde se imputó valor por defecto predecible
        for val in r.values():
            if val in ("NO REPORTADO", None, ""):
                stats.missing_values_handled += 1

    return stats


def process_records(key: str, raw_records: List[Any], dataset: Optional[dict] = None) -> ProcessedSampleResult:
    """Procesa y normaliza registros sin realizar llamadas de red."""
    dataset = dataset or get_dataset(key)
    dict_records = [r for r in raw_records if isinstance(r, dict)]

    if not dict_records:
        return ProcessedSampleResult(
            key=key,
            dataset=dataset,
            raw_records=dict_records,
            records=[],
            columns=[],
            table_rows=[],
            stats=QualityStats(),
            summary=build_statistical_summary(key, [], dataset=dataset),
        )

    cleaned = clean_records(key, dict_records)
    stats = calculate_stats(key, cleaned)
    summary = build_statistical_summary(key, cleaned, dataset=dataset)

    # Definir columnas de la tabla procesada en un orden claro y legible
    if cleaned:
        columns = list(cleaned[0].keys())
    else:
        columns = []

    # Generar filas para visualización en tabla (con None mostrado como '—')
    table_rows = []
    for r in cleaned:
        row = [r.get(col) if r.get(col) is not None else "—" for col in columns]
        table_rows.append(row)

    return ProcessedSampleResult(
        key=key,
        dataset=dataset,
        raw_records=dict_records,
        records=cleaned,
        table_rows=table_rows,
        columns=columns,
        stats=stats,
        summary=summary,
    )


def fetch_processed_sample(
    key: str, limit: int = DEFAULT_SAMPLE_SIZE, client: Optional[SocrataClient] = None
) -> ProcessedSampleResult:
    """Consulta una muestra real desde la API y aplica el procesamiento y limpieza.

    Maneja errores de red devolviendo el resultado con el mensaje descriptivo
    sin lanzar excepciones bloqueantes.
    """
    dataset = get_dataset(key)
    limit = max(1, min(int(limit), MAX_SAMPLE_SIZE))
    client = client or SocrataClient(timeout=15)

    try:
        raw_records = client.fetch(dataset["dataset_id"], limit=limit)
    except SocrataError as error:
        return ProcessedSampleResult(
            key=key,
            dataset=dataset,
            error=str(error),
            stats=QualityStats(),
            summary=build_statistical_summary(key, [], dataset=dataset),
        )

    return process_records(key, raw_records, dataset=dataset)
