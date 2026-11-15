"""Construcción de consultas SoQL seguras a partir de criterios validados.

Solo se incluyen en la consulta valores que provienen de listas cerradas
(departamentos, años, opciones de cada filtro) o texto que pasó por una lista
blanca de caracteres. Así ningún dato escrito por el usuario puede alterar la
estructura de la consulta.
"""

import re
from dataclasses import dataclass, field

from .config import DEPARTMENTS, SEARCH_CONFIG, department_value, strip_accents

MUNICIPALITY_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .\-]{2,40}$")
VOWELS = re.compile(r"[AEIOU]")


class InvalidCriteriaError(ValueError):
    pass


@dataclass
class SearchCriteria:
    departamento: str = ""
    municipio: str = ""
    anio: int = None
    extras: dict = field(default_factory=dict)

    @property
    def is_empty(self):
        return not (self.departamento or self.municipio or self.anio or any(self.extras.values()))


def quote(value):
    """Literal de texto SoQL con comillas simples escapadas."""
    return "'" + str(value).replace("'", "''") + "'"


def municipality_like(text):
    """Patrón LIKE por prefijo que no distingue mayúsculas ni tildes.

    Cada vocal se reemplaza por '_' (comodín de un carácter), de modo que
    "cajibio" encuentra "Cajibío". Una ñ escrita por el usuario también se
    vuelve comodín; una n escrita en lugar de ñ no encuentra la ñ.
    """
    cleaned = " ".join(text.split())
    if not MUNICIPALITY_PATTERN.match(cleaned):
        raise InvalidCriteriaError(
            "El municipio solo puede tener letras, espacios, puntos o guiones (2 a 40 caracteres)."
        )
    upper = cleaned.upper().replace("Ñ", "_")
    return VOWELS.sub("_", strip_accents(upper)) + "%"


def year_clause(config, year):
    date_field = config["date_field"]
    if config["date_format"] == "iso":
        return (
            f"{date_field} between '{year:04d}-01-01T00:00:00' "
            f"and '{year:04d}-12-31T23:59:59'"
        )
    # MM/AAAA y DD/MM/AAAA terminan en "/AAAA".
    return f"{date_field} like '%/{year:04d}'"


def build_where(dataset_key, criteria):
    """Devuelve la cláusula $where o una cadena vacía si no hay filtros."""
    config = SEARCH_CONFIG[dataset_key]
    clauses = []

    if criteria.departamento:
        if criteria.departamento not in DEPARTMENTS:
            raise InvalidCriteriaError("El departamento seleccionado no es válido.")
        value = department_value(dataset_key, criteria.departamento)
        clauses.append(f"{config['department_field']} = {quote(value)}")

    if criteria.municipio:
        pattern = municipality_like(criteria.municipio)
        clauses.append(f"upper({config['municipality_field']}) like {quote(pattern)}")

    if criteria.anio:
        first, last = config["years"]
        if not isinstance(criteria.anio, int) or not first <= criteria.anio <= last:
            raise InvalidCriteriaError(f"El año debe estar entre {first} y {last}.")
        clauses.append(year_clause(config, criteria.anio))

    for name, value in criteria.extras.items():
        if not value:
            continue
        options = config["extra_filters"].get(name)
        if options is None or value not in options["choices"]:
            raise InvalidCriteriaError("Uno de los filtros tiene un valor no válido.")
        clauses.append(f"{name} = {quote(value)}")

    return " AND ".join(clauses)


def count_select(dataset_key):
    """$select para contar filas y, si aplica, sumar la unidad de conteo."""
    metric_field = SEARCH_CONFIG[dataset_key]["metric_field"]
    if metric_field:
        # '::number' porque en homicidios 'cantidad' se publica como texto.
        return f"count(*) as filas, sum({metric_field}::number) as total"
    return "count(*) as filas"
