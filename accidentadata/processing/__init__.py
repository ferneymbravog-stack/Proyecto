"""Paquete de procesamiento y limpieza de datos para AccidentaData."""

from .cleaners import (
    clean_dane_code,
    clean_date_str,
    clean_int,
    clean_name,
    clean_text,
    extract_date_parts,
)
from .service import (
    ProcessedSampleResult,
    QualityStats,
    calculate_stats,
    fetch_processed_sample,
    process_records,
)
from .statistics import (
    BreakdownGroup,
    CategoryStat,
    StatisticalSummary,
    build_statistical_summary,
)
from .transformers import (
    clean_record,
    clean_records,
    transform_police_fatality,
    transform_police_injury,
    transform_runt_vehicle,
)

__all__ = [
    "clean_text",
    "clean_name",
    "clean_int",
    "clean_date_str",
    "extract_date_parts",
    "clean_dane_code",
    "transform_runt_vehicle",
    "transform_police_fatality",
    "transform_police_injury",
    "clean_record",
    "clean_records",
    "ProcessedSampleResult",
    "QualityStats",
    "calculate_stats",
    "process_records",
    "fetch_processed_sample",
    "CategoryStat",
    "BreakdownGroup",
    "StatisticalSummary",
    "build_statistical_summary",
]
