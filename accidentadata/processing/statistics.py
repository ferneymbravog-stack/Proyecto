"""Cálculos y agrupaciones estadísticas a partir de registros normalizados.

Construye indicadores descriptivos reales (sin cifras de ejemplo) respetando
la unidad de conteo oficial, el periodo observado y las variables disponibles
en cada fuente del catálogo.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class CategoryStat:
    label: str
    count: int
    records_count: int
    percentage: float
    context: str = ""


@dataclass
class BreakdownGroup:
    key: str
    title: str
    unit: str
    description: str
    items: List[CategoryStat] = field(default_factory=list)
    total_categories: int = 0
    has_unreported: bool = False


@dataclass
class StatisticalSummary:
    dataset_key: str
    dataset_name: str
    publisher: str
    is_empty: bool
    total_records: int = 0
    total_metric: int = 0
    unit_label: str = "Registros"
    unit_singular: str = "registro"
    unit_plural: str = "registros"
    avg_metric_per_record: float = 0.0
    period_start: str = ""
    period_end: str = ""
    period_label: str = "Sin registros disponibles"
    valid_dates_count: int = 0
    unique_departments: int = 0
    unique_municipalities: int = 0
    top_department: Optional[CategoryStat] = None
    top_municipality: Optional[CategoryStat] = None
    avg_vehicle_age: Optional[float] = None
    vehicle_age_count: int = 0
    breakdowns: List[BreakdownGroup] = field(default_factory=list)
    empty_message: str = ""
    context_note: str = ""


_UNIT_CONFIG = {
    "runt_vehicles": {
        "label": "Vehículos involucrados",
        "singular": "vehículo involucrado",
        "plural": "vehículos involucrados",
        "metric_field": "cantidad_vehiculos",
        "default_metric": 1,
        "date_field": "fecha_accidente",
    },
    "police_fatalities": {
        "label": "Víctimas fallecidas",
        "singular": "víctima",
        "plural": "víctimas",
        "metric_field": "cantidad",
        "default_metric": 0,
        "date_field": "fecha_hecho",
    },
    "police_injuries": {
        "label": "Víctimas lesionadas",
        "singular": "víctima",
        "plural": "víctimas",
        "metric_field": "cantidad",
        "default_metric": 0,
        "date_field": "fecha_hecho",
    },
}


def _record_metric(record: Dict[str, Any], key: str) -> int:
    cfg = _UNIT_CONFIG.get(key)
    if not cfg:
        return 1
    value = record.get(cfg["metric_field"], cfg["default_metric"])
    if isinstance(value, (int, float)):
        return int(value)
    return cfg["default_metric"]


def _build_category_breakdown(
    records: List[Dict[str, Any]],
    key: str,
    field_name: str,
    group_key: str,
    title: str,
    unit_plural: str,
    description: str,
    total_metric: int,
    top_n: int = 5,
) -> BreakdownGroup:
    counts: Dict[str, int] = defaultdict(int)
    row_counts: Dict[str, int] = defaultdict(int)
    has_unreported = False

    for rec in records:
        raw_val = rec.get(field_name)
        label = str(raw_val).strip() if raw_val not in (None, "") else "NO REPORTADO"
        if label == "NO REPORTADO":
            has_unreported = True
        counts[label] += _record_metric(rec, key)
        row_counts[label] += 1

    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    items = [
        CategoryStat(
            label=label,
            count=count,
            records_count=row_counts[label],
            percentage=round((count / total_metric) * 100, 1) if total_metric > 0 else 0.0,
        )
        for label, count in sorted_items[:top_n]
    ]

    return BreakdownGroup(
        key=group_key,
        title=title,
        unit=unit_plural,
        description=description,
        items=items,
        total_categories=len(sorted_items),
        has_unreported=has_unreported,
    )


def _build_municipality_breakdown(
    records: List[Dict[str, Any]],
    key: str,
    unit_plural: str,
    total_metric: int,
    top_n: int = 5,
) -> BreakdownGroup:
    counts: Dict[Tuple[str, str], int] = defaultdict(int)
    row_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    has_unreported = False

    for rec in records:
        muni = str(rec.get("municipio") or "NO REPORTADO").strip() or "NO REPORTADO"
        depto = str(rec.get("departamento") or "NO REPORTADO").strip() or "NO REPORTADO"
        if muni == "NO REPORTADO":
            has_unreported = True
            depto_ctx = ""
        else:
            depto_ctx = "" if depto == "NO REPORTADO" else depto

        bucket = (muni, depto_ctx)
        counts[bucket] += _record_metric(rec, key)
        row_counts[bucket] += 1

    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0][0], item[0][1]))
    items = [
        CategoryStat(
            label=muni,
            count=count,
            records_count=row_counts[(muni, depto_ctx)],
            percentage=round((count / total_metric) * 100, 1) if total_metric > 0 else 0.0,
            context=depto_ctx,
        )
        for (muni, depto_ctx), count in sorted_items[:top_n]
    ]

    return BreakdownGroup(
        key="municipalities",
        title="Municipios con mayor concentración",
        unit=unit_plural,
        description="Distribución por municipio según los registros consultados.",
        items=items,
        total_categories=len(sorted_items),
        has_unreported=has_unreported,
    )


def _build_year_breakdown(
    records: List[Dict[str, Any]],
    key: str,
    unit_plural: str,
    total_metric: int,
) -> BreakdownGroup:
    counts: Dict[str, int] = defaultdict(int)
    row_counts: Dict[str, int] = defaultdict(int)
    has_unreported = False

    for rec in records:
        anio = rec.get("anio")
        if isinstance(anio, int):
            label = str(anio)
        else:
            label = "Sin fecha"
            has_unreported = True
        counts[label] += _record_metric(rec, key)
        row_counts[label] += 1

    def _year_sort_key(item: Tuple[str, int]) -> Tuple[int, int]:
        label = item[0]
        if label.isdigit():
            return (0, int(label))
        return (1, 0)

    sorted_items = sorted(counts.items(), key=_year_sort_key)
    items = [
        CategoryStat(
            label=label,
            count=count,
            records_count=row_counts[label],
            percentage=round((count / total_metric) * 100, 1) if total_metric > 0 else 0.0,
        )
        for label, count in sorted_items
    ]

    return BreakdownGroup(
        key="years",
        title="Distribución por año",
        unit=unit_plural,
        description="Agrupación cronológica según la fecha normalizada del registro.",
        items=items,
        total_categories=len(sorted_items),
        has_unreported=has_unreported,
    )


def build_statistical_summary(
    key: str,
    cleaned_records: List[Dict[str, Any]],
    dataset: Optional[dict] = None,
) -> StatisticalSummary:
    """Genera un resumen estadístico completo a partir de registros normalizados."""
    dataset = dataset or {}
    dataset_name = dataset.get("name", key)
    publisher = dataset.get("publisher", "Fuente oficial")

    cfg = _UNIT_CONFIG.get(
        key,
        {
            "label": "Registros",
            "singular": "registro",
            "plural": "registros",
            "metric_field": None,
            "default_metric": 1,
            "date_field": "fecha_hecho",
        },
    )

    if not cleaned_records:
        return StatisticalSummary(
            dataset_key=key,
            dataset_name=dataset_name,
            publisher=publisher,
            is_empty=True,
            unit_label=cfg["label"],
            unit_singular=cfg["singular"],
            unit_plural=cfg["plural"],
            period_label="Sin registros disponibles",
            empty_message=(
                "No hay registros disponibles en la consulta actual para calcular "
                "indicadores estadísticos."
            ),
            context_note=dataset.get("count_unit", ""),
        )

    total_records = len(cleaned_records)
    total_metric = sum(_record_metric(r, key) for r in cleaned_records)
    avg_metric = round(total_metric / total_records, 2) if total_records > 0 else 0.0

    # Periodo observado en los registros reales
    date_field = cfg["date_field"]
    valid_dates = sorted(
        str(r.get(date_field)).strip()
        for r in cleaned_records
        if r.get(date_field)
    )
    valid_dates_count = len(valid_dates)
    if valid_dates:
        period_start = valid_dates[0]
        period_end = valid_dates[-1]
        period_label = (
            period_start if period_start == period_end else f"{period_start} a {period_end}"
        )
    else:
        period_start = ""
        period_end = ""
        period_label = "Sin fechas válidas en la muestra"

    # Cobertura geográfica reportada
    unique_deptos = {
        str(r.get("departamento")).strip()
        for r in cleaned_records
        if r.get("departamento") and r.get("departamento") != "NO REPORTADO"
    }
    unique_munis = {
        (str(r.get("municipio")).strip(), str(r.get("departamento") or "").strip())
        for r in cleaned_records
        if r.get("municipio") and r.get("municipio") != "NO REPORTADO"
    }

    dept_group = _build_category_breakdown(
        cleaned_records,
        key=key,
        field_name="departamento",
        group_key="departments",
        title="Departamentos con mayor concentración",
        unit_plural=cfg["plural"],
        description="Agrupación por departamento reportado en la muestra.",
        total_metric=total_metric,
        top_n=5,
    )
    muni_group = _build_municipality_breakdown(
        cleaned_records,
        key=key,
        unit_plural=cfg["plural"],
        total_metric=total_metric,
        top_n=5,
    )
    year_group = _build_year_breakdown(
        cleaned_records,
        key=key,
        unit_plural=cfg["plural"],
        total_metric=total_metric,
    )

    top_department = next(
        (item for item in dept_group.items if item.label != "NO REPORTADO"),
        dept_group.items[0] if dept_group.items else None,
    )
    top_municipality = next(
        (item for item in muni_group.items if item.label != "NO REPORTADO"),
        muni_group.items[0] if muni_group.items else None,
    )

    breakdowns: List[BreakdownGroup] = [dept_group, muni_group, year_group]

    avg_vehicle_age: Optional[float] = None
    vehicle_age_count = 0

    if key == "runt_vehicles":
        ages = [
            r["edad_vehiculo"]
            for r in cleaned_records
            if isinstance(r.get("edad_vehiculo"), int)
        ]
        if ages:
            vehicle_age_count = len(ages)
            avg_vehicle_age = round(sum(ages) / vehicle_age_count, 1)

        breakdowns.append(
            _build_category_breakdown(
                cleaned_records,
                key=key,
                field_name="gravedad_accidente",
                group_key="severity",
                title="Distribución por gravedad",
                unit_plural=cfg["plural"],
                description="Clasificación oficial del siniestro en el RUNT.",
                total_metric=total_metric,
                top_n=5,
            )
        )
        breakdowns.append(
            _build_category_breakdown(
                cleaned_records,
                key=key,
                field_name="tipo_vehiculo",
                group_key="vehicle_types",
                title="Tipos de vehículo más frecuentes",
                unit_plural=cfg["plural"],
                description="Categorías de vehículo registradas en la muestra.",
                total_metric=total_metric,
                top_n=5,
            )
        )
    elif key == "police_fatalities":
        breakdowns.append(
            _build_category_breakdown(
                cleaned_records,
                key=key,
                field_name="genero",
                group_key="gender",
                title="Distribución por género",
                unit_plural=cfg["plural"],
                description="Víctimas agrupadas según el género reportado.",
                total_metric=total_metric,
                top_n=5,
            )
        )
        breakdowns.append(
            _build_category_breakdown(
                cleaned_records,
                key=key,
                field_name="grupo_etario",
                group_key="age_groups",
                title="Distribución por grupo etario",
                unit_plural=cfg["plural"],
                description="Víctimas agrupadas según su rango de edad.",
                total_metric=total_metric,
                top_n=5,
            )
        )
        breakdowns.append(
            _build_category_breakdown(
                cleaned_records,
                key=key,
                field_name="armas_medios",
                group_key="weapons",
                title="Medio o vehículo asociado",
                unit_plural=cfg["plural"],
                description="Elemento reportado por la Policía Nacional en el hecho.",
                total_metric=total_metric,
                top_n=5,
            )
        )

    context_note = (
        f"Indicadores calculados sobre {total_records} registros reales consultados "
        f"({total_metric} {cfg['plural']}). {dataset.get('count_unit', '')}"
    ).strip()

    return StatisticalSummary(
        dataset_key=key,
        dataset_name=dataset_name,
        publisher=publisher,
        is_empty=False,
        total_records=total_records,
        total_metric=total_metric,
        unit_label=cfg["label"],
        unit_singular=cfg["singular"],
        unit_plural=cfg["plural"],
        avg_metric_per_record=avg_metric,
        period_start=period_start,
        period_end=period_end,
        period_label=period_label,
        valid_dates_count=valid_dates_count,
        unique_departments=len(unique_deptos),
        unique_municipalities=len(unique_munis),
        top_department=top_department,
        top_municipality=top_municipality,
        avg_vehicle_age=avg_vehicle_age,
        vehicle_age_count=vehicle_age_count,
        breakdowns=breakdowns,
        context_note=context_note,
    )
