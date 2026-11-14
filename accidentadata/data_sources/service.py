"""Consulta de muestras de las fuentes registradas en el catálogo.

Este módulo une el catálogo con el cliente Socrata y convierte cualquier fallo
en un resultado que la interfaz puede mostrar sin interrumpir la aplicación.
"""

from dataclasses import dataclass, field

from .catalog import DATASETS
from .socrata_client import SocrataClient, SocrataError

DEFAULT_SAMPLE_SIZE = 10
MAX_SAMPLE_SIZE = 50


class UnknownDatasetError(ValueError):
    pass


@dataclass
class SampleResult:
    key: str
    dataset: dict
    records: list = field(default_factory=list)
    columns: list = field(default_factory=list)
    error: str = ""

    @property
    def is_empty(self):
        return not self.error and not self.records


def get_dataset(key):
    try:
        return DATASETS[key]
    except KeyError:
        raise UnknownDatasetError(
            "La fuente solicitada no existe en el catálogo."
        ) from None


def fetch_sample(key, limit=DEFAULT_SAMPLE_SIZE, client=None):
    """Devuelve una muestra de registros reales de la fuente indicada.

    Lanza UnknownDatasetError si la clave no está en el catálogo. Los errores
    de red o de formato de la API se devuelven dentro del resultado.
    """
    dataset = get_dataset(key)
    limit = max(1, min(int(limit), MAX_SAMPLE_SIZE))
    client = client or SocrataClient(timeout=15)

    try:
        records = client.fetch(dataset["dataset_id"], limit=limit)
    except SocrataError as error:
        return SampleResult(key=key, dataset=dataset, error=str(error))

    records = [record for record in records if isinstance(record, dict)]
    columns = [name for name in dataset["fields"] if any(name in r for r in records)]
    if records and not columns:
        # La API cambió los nombres de los campos: se muestran tal como llegan.
        columns = sorted({name for record in records for name in record})
    rows = [[record.get(name, "") for name in columns] for record in records]

    return SampleResult(key=key, dataset=dataset, records=rows, columns=columns)
