"""Búsqueda paginada sobre las fuentes del catálogo.

Hace dos consultas a la API: una cuenta todas las coincidencias en la fuente
completa (no solo en la página) y otra trae la página de resultados, que se
procesa con el pipeline de AD-03 para mostrarla normalizada.
"""

import math
from dataclasses import dataclass, field

from accidentadata.data_sources.service import get_dataset
from accidentadata.data_sources.socrata_client import SocrataClient, SocrataError
from accidentadata.processing.service import process_records

from .config import SEARCH_CONFIG
from .query import build_where, count_select

PAGE_SIZE = 20


@dataclass
class SearchResult:
    key: str
    dataset: dict
    where: str = ""
    columns: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    total_rows: int = 0
    metric_total: int = 0
    metric_label: str = ""
    page: int = 1
    pages: int = 0
    error: str = ""

    @property
    def has_results(self):
        return not self.error and self.total_rows > 0

    @property
    def no_matches(self):
        return not self.error and self.total_rows == 0

    @property
    def first_row(self):
        return (self.page - 1) * PAGE_SIZE + 1 if self.rows else 0

    @property
    def last_row(self):
        return self.first_row + len(self.rows) - 1 if self.rows else 0


def _to_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def search(dataset_key, criteria, page=1, client=None):
    """Ejecuta la búsqueda. Lanza InvalidCriteriaError si los criterios no son válidos.

    Los errores de la API se devuelven en el resultado, sin interrumpir la aplicación.
    """
    dataset = get_dataset(dataset_key)
    config = SEARCH_CONFIG[dataset_key]
    where = build_where(dataset_key, criteria)
    client = client or SocrataClient(timeout=15)
    result = SearchResult(
        key=dataset_key,
        dataset=dataset,
        where=where,
        metric_label=config["metric_label"],
    )

    count_filters = {"$select": count_select(dataset_key)}
    if where:
        count_filters["$where"] = where

    try:
        summary = client.fetch(dataset["dataset_id"], limit=1, filters=count_filters)
        summary = summary[0] if summary else {}
        result.total_rows = _to_int(summary.get("filas"))
        result.metric_total = (
            _to_int(summary.get("total")) if config["metric_field"] else result.total_rows
        )

        if result.total_rows == 0:
            return result

        result.pages = math.ceil(result.total_rows / PAGE_SIZE)
        result.page = min(max(1, page), result.pages)

        page_filters = {"$order": ":id"}
        if where:
            page_filters["$where"] = where
        records = client.fetch(
            dataset["dataset_id"],
            limit=PAGE_SIZE,
            offset=(result.page - 1) * PAGE_SIZE,
            filters=page_filters,
        )
    except SocrataError as error:
        result.error = str(error)
        return result

    processed = process_records(dataset_key, records, dataset=dataset)
    result.columns = processed.columns
    result.rows = processed.table_rows
    return result
